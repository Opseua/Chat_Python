"""IGNORE"""

# pylint: disable=C0103
# pylint: disable=C0301
# pylint: disable=W0621
# pylint: disable=W0718
# pylint: disable=R1732
# pylint: disable=R1702
# pylint: disable=R0914
# pylint: disable=R0915
# pylint: disable=R0912
# pylint: disable=W0602
# pylint: disable=W0603
# pylint: disable=C0115
# pylint: disable=R1710

# BIBLIOTECAS: NATIVAS
import asyncio
import sys
import os
from datetime import datetime
import logging
import random
import string

# BIBLIOTECAS: NECESSÁRIO INSTALAR → pip install brotli mitmproxy
from flask import Flask, request, jsonify
from g4f.client import Client

# FUNÇÕES DE ARQUIVOS
from chatNew import chatNew
from chatAddMessage import chatAddMessage
from historyChat import historyChat
from historyMessages import historyMessages
from historyDelete import historyDelete


# OCULTAR CONSOLE DE ERROS G4F
if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


# OCULTAR CONSOLE DO SERVIDOR
logging.getLogger("werkzeug").disabled = True

app = Flask(__name__)
client = Client()


@app.route("/chat", methods=["POST"])
def chat():
    """IGNORE"""
    try:
        data = request.json
    except Exception:
        infBody = {"ret": False, "msg": "CHAT: ERRO | JSON INVALIDO"}
        return jsonify(infBody), 200

    # DEFINIR 'action'
    action = data.get("action")
    if action is None or action == "":
        infBody = {"ret": False, "msg": "CHAT: ERRO | INFORMAR O 'action'"}
        return jsonify(infBody), 200

    # DEFINIR 'message'
    message = data.get("message")
    if message is None or message == "":
        message = None

    # DEFINIR 'model'
    model = data.get("model")
    if model is None or model == "":
        model = "gpt-3.5-turbo"

    # DEFINIR 'chatId'
    chatId = data.get("chatId")
    if chatId is None or chatId == "":
        chatId = None

    # DEFINIR 'includesInMessages'
    includesInMessages = data.get("includesInMessages")
    if includesInMessages is None or includesInMessages == "":
        includesInMessages = []

    # DEFINIR 'qtdDeleteMessages'
    qtdDeleteMessages = data.get("qtdDeleteMessages")
    if qtdDeleteMessages is None or qtdDeleteMessages == "":
        qtdDeleteMessages = 0

    # ACTION: ENVIAR MENSAGEM
    if action == "messageSend":
        message = data.get("message")
        if message is None:
            infBody = {
                "ret": False,
                "msg": "CHAT [MESSAGESEND]: ERRO | INFORMAR O 'message'",
            }
            return jsonify(infBody), 200

        isNewChat = False
        messagesToAssistant = []
        if chatId is None:
            # GERAR 'chatId' → ANO_MES_DIA-HOR.MIN.SEC.MIL-ABC
            letras = "".join(random.choices(string.ascii_uppercase, k=3))
            chatId = f"{datetime.now().strftime("%Y_%m_%d-%H.%M.%S.%f")[:-3]}-{letras}"
            isNewChat = True
        else:
            # ID DO CHAT NÃO EXISTE
            infHistoryChat = {
                "chatId": chatId,
                "includesInMessages": ["role", "content"],
            }
            messagesToAssistant = historyMessages(infHistoryChat)
            if not messagesToAssistant["ret"]:
                return jsonify(messagesToAssistant), 200
            messagesToAssistant = messagesToAssistant["res"][0]["messages"]

        # BOT: ENVIAR MENSAGEM
        messagesToAssistant.append({"role": "user", "content": message})
        timestampUser = int(datetime.now().timestamp())
        try:
            response = client.chat.completions.create(
                model=model, messages=messagesToAssistant
            )
        except Exception as e:
            print(str(e))
            infBody = {
                "ret": False,
                "msg": "CHAT [MESSAGESEND]: ERRO | INFORMAR O 'message'",
            }
            return jsonify(infBody), 200
        # BOT: RESPOSTA RECEBIDA
        if response:
            resposta = response.choices[0].message.content
            timestampAssistant = int(datetime.now().timestamp())
            # CHAT: CRIAR NOVO
            infChat = {
                "chatId": chatId,
                "model": model,
                "timestampUser": timestampUser,
                "timestampAssistant": timestampAssistant,
                "message": message,
                "response": resposta,
            }
            if isNewChat:
                chatNew(infChat)
            else:
                # CHAT: ADICIONAR AO EXISTENTE
                chatAddMessage(infChat)
            infBody = {
                "ret": True,
                "msg": "CHAT [MESSAGESEND]: OK",
                "res": {
                    "chatNew": isNewChat,
                    "chatId": chatId,
                    "model": model,
                    "response": resposta,
                },
            }
            return jsonify(infBody), 200
        else:
            # BOT: RESPOSTA NÃO RECEBIDA
            infBody = {
                "ret": False,
                "msg": "CHAT [MESSAGESEND]: ERRO | BOT NÃO RESPONDEU",
            }
            return jsonify(infBody), 200

    # ACTION: HISTÓRICO DE CHATS
    elif action == "historyChat":
        infHistoryChat = {"model": model, "includesInMessages": includesInMessages}
        retHistoryChat = historyChat(infHistoryChat)
        return jsonify(retHistoryChat), 200

    # ACTION: HISTÓRICO DE MENSAGENS
    elif action == "historyMessages":
        infHistoryChat = {"chatId": chatId, "includesInMessages": includesInMessages}
        retHistoryMessages = historyMessages(infHistoryChat)
        return jsonify(retHistoryMessages), 200

    # ACTION: DELETAR MENSAGENS DO CHAT
    elif action == "historyDelete":
        infHistoryDelete = {"chatId": chatId, "qtdDeleteMessages": qtdDeleteMessages}
        retHistoryDelete = historyDelete(infHistoryDelete)
        return jsonify(retHistoryDelete), 200

    # ACTION: NÃO IDENTIFICADA
    else:
        infBody = {"ret": False, "msg": "CHAT: ERRO | NÃO IDENTIFICADO 'action'"}
        return jsonify(infBody), 200


##### INICIAR SERVIDOR
if __name__ == "__main__":
    # LIMPAR CONSOLE
    os.system("cls")
    print("RODANDO NA PORTA")
    app.run(port=8890, debug=True)
