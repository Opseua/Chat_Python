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
# pylint: disable=W0622
# pylint: disable=C0410
# pylint: disable=C0114
# pylint: disable=C0116
# ERRO DE IMPORT EM OUTRA PASTA
# pylint: disable=E0401
# ERRO DE IMPORT ANTES DE USAR A VARIÁVEL
# pylint: disable=C0413
# pylint: disable=C0411
# ERRO DE IMPORT 'datetime'
# pylint: disable=E1101

# IMPORTAR 'export.py'
from export import infGlobal
from export import errAll

# BIBLIOTECAS: NATIVAS
import os

try:
    # BIBLIOTECAS: NATIVAS
    sys = infGlobal["sys"]
    json = infGlobal["json"]
    asyncio = infGlobal["asyncio"]
    random = infGlobal["random"]
    string = infGlobal["string"]
    datetime = infGlobal["datetime"]

    # BIBLIOTECAS: NECESSÁRIO INSTALAR → pip install brotli mitmproxy
    web = infGlobal["web"]

    # FUNÇÕES DE ARQUIVOS
    sys.path.append(
        os.path.abspath(os.path.join(os.path.dirname(__file__), "resourcesNew"))
    )
    from chatHistoryDelete import chatHistoryDelete
    from chatHistoryMessages import chatHistoryMessages
    from chatHistory import chatHistory
    from chatAddMessage import chatAddMessage
    from chatNew import chatNew
    from messageSendG4f import messageSendG4f
    from messageSendTelegram import messageSendTelegram

    # SERVER HTTP: RESPONSE
    def httpResponse(text):
        ret, msg = False, False
        if "ret" in text and text["ret"]:
            ret = True
        if "msg" in text:
            msg = text["msg"]
        res = {"ret": ret, "msg": msg}
        if "res" in text:
            res["res"] = text["res"]
        res = json.dumps(res)
        return web.Response(text=res, status=200, content_type="application/json")

    # SERVER HTTP: REQUEST
    async def httpRequest(request):
        data = await request.text()
        try:
            data = json.loads(data)
        except Exception:
            return httpResponse({"msg": "CHAT: ERRO | JSON INVALIDO"})
        # print("REQUISICAO RECEBIDA")
        timestampUser = int(datetime.now().timestamp())

        # DEFINIR 'action'
        action = data.get("action")
        if action is None or action == "":
            return httpResponse({"msg": "CHAT: ERRO | INFORMAR O 'action'"})

        # DEFINIR 'origin'
        origin = data.get("origin")
        if origin is None or origin == "":
            origin = None

        # DEFINIR 'model'
        model = data.get("model")
        if model is None or model == "":
            model = "gpt-3.5-turbo"

        # DEFINIR 'messagePrompt'
        messagePrompt = data.get("messagePrompt")
        if messagePrompt is None or messagePrompt == "":
            messagePrompt = None

        # DEFINIR 'messageFile'
        messageFile = data.get("messageFile")
        if messageFile is None or messageFile == "" or messageFile is False:
            messageFile = None

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

        # retMessageSend = await messageSendG4f("AAA")
        # return httpResponse({"msg": retMessageSend})

        # →→→ ACTION: ENVIAR MENSAGEM
        if action == "messageSend":
            if messagePrompt is None:
                infBody = {
                    "msg": "CHAT [MESSAGESEND]: ERRO | INFORMAR O 'messagePrompt'"
                }
                return httpResponse(infBody)
            # ID: GERAR
            isNewChat, messagesToAssistant = False, []
            if chatId is None:
                # ID INFORMADO [NÃO]
                letras = "".join(random.choices(string.ascii_uppercase, k=3))
                now = datetime.now().strftime("%Y_%m_%d-%H.%M.%S.%f")[:-3]
                isNewChat, chatId = True, f"{now}-{letras}"
            else:
                # ID INFORMADO [SIM]
                messagesToAssistant = chatHistoryMessages(
                    {"chatId": chatId, "includesInMessages": ["role", "content"]}
                )
                if not messagesToAssistant["ret"]:
                    return httpResponse(messagesToAssistant)
                messagesToAssistant = messagesToAssistant["res"][0]["messages"]

            # DEFINIR PROMPT
            messagePromptKeep = messagePrompt
            # --- [TEXTO]
            if messageFile is None:
                # →→→→→→→→→→→→→→→→→→→→→→→→→ { "HISTORICO_TEXTO" + "PROMPT_TEXTO" }
                messagesToAssistant.append(
                    {"role": "user", "content": messagePromptKeep}
                )
                messagePrompt = json.dumps(messagesToAssistant, ensure_ascii=False)
            # --- [ARQUIVO + TEXTO]
            if messageFile:
                if messageFile is True:
                    #  →→→→→→→→→→→→→→→ HISTORICO_ARQUIVO + PROMPT_TEXTO
                    messageFile = "log/CONTENT.txt"
                    with open(messageFile, "w", encoding="utf-8") as arquivo:
                        arquivo.write(
                            json.dumps(messagesToAssistant, ensure_ascii=False)
                        )
                else:
                    #  →→→→→→→→→→→→→→→ ARQUIVO + PROMPT_TEXTO
                    pass

            # ENVIAR MENSAGEM
            retMessageSend = None
            if origin == "telegram":
                # *** TELEGRAN
                retMessageSend = await messageSendTelegram(
                    {"messagePrompt": messagePrompt, "messageFile": messageFile}
                )
                # PROSSEGUIR COM O ARQUIVO
                if messageFile:
                    retMessageSend = await messageSendTelegram(
                        {"messagePrompt": messagePrompt, "messageFile": None}
                    )
                # RESETAR E LIMPAR CONVERSA
                asyncio.create_task(
                    messageSendTelegram({"messagePrompt": "reset", "messageFile": None})
                )

            elif origin == "g4f":
                # *** G4F
                retMessageSend = await messageSendG4f(
                    {"model": model, "messagePrompt": messagePrompt}
                )
            else:
                infBody = {"msg": "CHAT [MESSAGESEND]: ERRO | INFORMAR O 'origin'"}
                return httpResponse(infBody)

            # BOT: RESPOSTA RECEBIDA
            if retMessageSend:
                infChat = {
                    "chatNew": isNewChat,
                    "chatId": chatId,
                    "origin": origin,
                    "model": model,
                    "timestampUser": timestampUser,
                    "timestampAssistant": int(datetime.now().timestamp()),
                    "message": messagePromptKeep,
                    "response": retMessageSend,
                }
                if isNewChat:
                    # CHAT: CRIAR NOVO
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
                        "origin": origin,
                        "model": model,
                        "response": retMessageSend,
                    },
                }
                return httpResponse(infBody)
            else:
                infBody = {"msg": "CHAT [MESSAGESEND]: ERRO | RESPOSTA NAO RECEBIDA"}
                return httpResponse(infBody)

        # →→→ ACTION: HISTÓRICO DE CHATS
        elif action == "historyChat":
            infHistoryChat = {"model": model, "includesInMessages": includesInMessages}
            return httpResponse(chatHistory(infHistoryChat))

        # →→→ ACTION: HISTÓRICO DE MENSAGENS
        elif action == "historyMessages":
            infHistoryChat = {
                "chatId": chatId,
                "includesInMessages": includesInMessages,
            }
            return httpResponse(chatHistoryMessages(infHistoryChat))

        # ACTION: DELETAR MENSAGENS DO CHAT
        elif action == "historyDelete":
            infHistoryDelete = {
                "chatId": chatId,
                "qtdDeleteMessages": qtdDeleteMessages,
            }
            return httpResponse(chatHistoryDelete(infHistoryDelete))

        # ACTION: NÃO IDENTIFICADA
        else:
            return httpResponse({"msg": "CHAT: ERRO | NÃO IDENTIFICADO 'action'"})

except Exception as exceptErr:
    errAll(exceptErr)
    print("CÓDIGO INTEIRO [httpRequest]")
    os._exit(1)
