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
# ERRO DE IMPORT EM OUTRA PASTA
# pylint: disable=E0401
# ERRO DE IMPORT ANTES DE USAR A VARIÁVEL
# pylint: disable=C0413

# BIBLIOTECAS: NATIVAS
from http.server import BaseHTTPRequestHandler, HTTPServer
import asyncio, sys, os, logging, random, string, json
from datetime import datetime

# BIBLIOTECAS: NECESSÁRIO INSTALAR → pip install brotli mitmproxy
from g4f.client import Client

# FUNÇÕES DE ARQUIVOS
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "resources")))
from chatNew import chatNew
from chatAddMessage import chatAddMessage
from historyChat import historyChat
from historyMessages import historyMessages
from historyDelete import historyDelete

try:
    # OCULTAR CONSOLE DE ERROS G4F
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    # INICIAR O SERVIDOR G4F
    client = Client()


    # REQUISIÇÕES 
    def request(data):
        """IGNORE"""
        try:
            data = json.loads(data)
        except Exception:
            infBody = {"ret": False, "msg": "CHAT: ERRO | JSON INVALIDO"}
            return json.dumps(infBody), 200

        # DEFINIR 'action'
        action = data.get("action")
        if action is None or action == "":
            infBody = {"ret": False, "msg": "CHAT: ERRO | INFORMAR O 'action'"}
            return json.dumps(infBody), 200

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
                return json.dumps(infBody), 200

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
                    return json.dumps(messagesToAssistant), 200
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
                return json.dumps(infBody), 200
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
                return json.dumps(infBody), 200
            else:
                # BOT: RESPOSTA NÃO RECEBIDA
                infBody = {
                    "ret": False,
                    "msg": "CHAT [MESSAGESEND]: ERRO | BOT NÃO RESPONDEU",
                }
                return json.dumps(infBody), 200

        # ACTION: HISTÓRICO DE CHATS
        elif action == "historyChat":
            infHistoryChat = {"model": model, "includesInMessages": includesInMessages}
            retHistoryChat = historyChat(infHistoryChat)
            return json.dumps(retHistoryChat), 200

        # ACTION: HISTÓRICO DE MENSAGENS
        elif action == "historyMessages":
            infHistoryChat = {"chatId": chatId, "includesInMessages": includesInMessages}
            retHistoryMessages = historyMessages(infHistoryChat)
            return json.dumps(retHistoryMessages), 200

        # ACTION: DELETAR MENSAGENS DO CHAT
        elif action == "historyDelete":
            infHistoryDelete = {"chatId": chatId, "qtdDeleteMessages": qtdDeleteMessages}
            retHistoryDelete = historyDelete(infHistoryDelete)
            return json.dumps(retHistoryDelete), 200

        # ACTION: NÃO IDENTIFICADA
        else:
            infBody = {"ret": False, "msg": "CHAT: ERRO | NÃO IDENTIFICADO 'action'"}
            return json.dumps(infBody), 200



# ------------------------------------------ SERVIDOR HTTP ------------------------------------------
    class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
        def _set_headers(self, status_code=200):
            self.send_response(status_code)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
        def do_POST(self):
            if self.path == "/chat":
                response_body, status_code = request(self.rfile.read(int(self.headers['Content-Length'])).decode('utf-8'))
                self._set_headers(status_code)
                self.wfile.write(response_body.encode('utf-8'))
        def log_message(self, format, *args):
            pass
    def serverRun():
        logging.getLogger('http.server').setLevel(logging.CRITICAL)
        os.system("cls")
        port=8890
        print(f'RODANDO NA PORTA: {port}')
        HTTPServer(('', port), SimpleHTTPRequestHandler).serve_forever()

    # #### INICIAR SERVIDOR
    if __name__ == "__main__":
        serverRun()



except Exception:
    print('ERRO GERAL PYTHON')
    os._exit(1)
