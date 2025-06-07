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
# ERRO IGNORAR ERROS DO CTRL + C
# pylint: disable=W1514
# ERRO 'sig' e 'frame'
# pylint: disable=W0613
# pylint: disable=W0101

# ARQUIVO ATUAL
e = __file__
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
    from chatHistoryDelete import chatHistoryDelete
    from chatHistoryMessages import chatHistoryMessages
    from chatHistory import chatHistory
    from chatAddMessage import chatAddMessage
    from chatNew import chatNew
    from providersSend import providersSend

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
        res = json.dumps(res, ensure_ascii=False)
        return web.Response(text=res, status=200, content_type="application/json")

    # SERVER HTTP: REQUEST
    async def httpRequest(request):
        data = await request.text()
        try:
            data = json.loads(data)
        except Exception:
            return httpResponse({"msg": "CHAT: ERRO | JSON INVALIDO"})
        timestampUser = int(datetime.now().timestamp())

        # DEFINIR 'action'
        action = data.get("action", None)
        if not action:
            return httpResponse({"msg": "CHAT: ERRO | INFORMAR O 'action'"})

        # DEFINIR 'providers' | 'messagePrompt' | 'messageFile' | 'chatId' | 'includesInMessages' | 'qtdDeleteMessages'
        providers = data.get("provider", [])
        if providers and isinstance(providers, str):
            providers = [providers]
        model = data.get("model", None)
        messagePrompt = data.get("messagePrompt", None)
        messageFile = data.get("messageFile", None)
        chatId = data.get("chatId", None)
        includesInMessages = data.get("includesInMessages", [])
        qtdDeleteMessages = data.get("qtdDeleteMessages", 0)

        if all(p != "telegram" for p in providers):
            messageFile = None

        # -------------------------------------------------------------------------------------------------------------

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
            if messageFile is None:
                # [TEXTO] →→→→→→→→→→→→→→→→→→→→→→→→→ { "HISTORICO_TEXTO" + "PROMPT_TEXTO" }
                messagesToAssistant.append(
                    {"role": "user", "content": messagePromptKeep}
                )
                messagePrompt = json.dumps(messagesToAssistant, ensure_ascii=False)
            if messageFile:
                if messageFile is True:
                    #  [ARQUIVO + TEXTO] →→→→→→→→→→→→→→→ HISTORICO_ARQUIVO + PROMPT_TEXTO
                    messageFile = "logs/CONTENT.txt"
                    with open(messageFile, "w", encoding="utf-8") as arquivo:
                        arquivo.write(
                            json.dumps(messagesToAssistant, ensure_ascii=False)
                        )
                else:
                    #  →→→→→→→→→→→→→→→ ARQUIVO + PROMPT_TEXTO
                    pass

            # ENVIAR MENSAGEM
            retMessageSend = {"ret": False}

            ############################################################################################################################################

            if not providers:
                infBody = {
                    "msg": "CHAT [MESSAGESEND]: ERRO | INFORMAR O 'provider' [string ou array]"
                }
                return httpResponse(infBody)
            else:
                # ENVIAR MENSAGEM PARA VÁRIOS BOTS E PEGAR A PRIMEIRA RESPOSTA
                infProvidersSend = {
                    "providers": providers,
                    "model": model,
                    "messagePrompt": messagePrompt,
                    "messageFile": messageFile,
                }
                retMessageSend = await providersSend(infProvidersSend)

                print(retMessageSend)
                sys.exit("Finalizando o script de propósito")

                msg = {
                    "txt": f"*** RECEBIDO *** [{retMessageSend['provider']}] ([{retMessageSend['model']}])",
                    "e": e,
                }
                logConsole(msg)

            ############################################################################################################################################

            # BOT: RESPOSTA RECEBIDA
            if retMessageSend["ret"]:
                infChat = {
                    "chatNew": isNewChat,
                    "chatId": chatId,
                    "provider": retMessageSend["provider"],
                    "model": retMessageSend["model"],
                    "timestampUser": timestampUser,
                    "timestampAssistant": int(datetime.now().timestamp()),
                    "message": messagePromptKeep,
                    "response": retMessageSend["res"],
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
                        "provider": retMessageSend["provider"],
                        "model": retMessageSend["model"],
                        "response": retMessageSend["res"],
                    },
                }
            else:
                infBody = {"ret": False, "msg": retMessageSend["msg"]}
            return httpResponse(infBody)
        #
        # -------------------------------------------------------------------------------------------------------------
        #
        # →→→ ACTION: HISTÓRICO DE CHATS
        elif action == "historyChat":
            infHistoryChat = {
                "provider": provider,
                "includesInMessages": includesInMessages,
            }
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
    errAll({"e": e, "err": exceptErr, "txt": f"CÓDIGO INTEIRO\n{str(exceptErr)}"})
