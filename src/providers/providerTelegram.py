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

try:
    # BIBLIOTECAS: NATIVAS
    asyncio = infGlobal["asyncio"]
    re = infGlobal["re"]
    datetime = infGlobal["datetime"]

    # BIBLIOTECAS: NECESSÁRIO INSTALAR → pip install brotli mitmproxy
    from telethon import TelegramClient, events

    # VARIÁVEIS
    telegramApiId = infGlobal["telegramApiId"]
    telegramApiHash = infGlobal["telegramApiHash"]
    telegramChatName = infGlobal["telegramChatName"]
    clientTelegram = TelegramClient("logs/session", telegramApiId, telegramApiHash)

    # ------------------------------------------------------ TELEGRAM ------------------------------------------------------------
    # CLIENT
    async def runClient():
        await clientTelegram.start()
        logConsole({"e": e, "txt": "RODANDO → CLIENTE TELEGRAM"})

    # INICIAR
    loop = asyncio.get_event_loop()
    loop.run_until_complete(runClient())

    messageId, messageContent, messageTimestamp, isMonitoring = None, "", None, False
    awaitForMessage = ["🤖️", "Reset successfully!", "Upload successfully!"]

    # EVENTO: MENSAGEM RECEBIDA
    @clientTelegram.on(events.NewMessage(from_users=telegramChatName))
    async def handler(event):
        global messageId, messageContent, messageTimestamp, isMonitoring
        if not isMonitoring:
            return
        messageId, messageContent = event.message.id, event.message.text
        messageTimestamp = datetime.now()
        logConsole({"e": e, "txt": f"MENSAGEM RECEBIDA: {messageContent}"})

    # EVENTO: MENSAGEM EDITADA
    @clientTelegram.on(events.MessageEdited(from_users=telegramChatName))
    async def handlerMessageEdited(edited_event):
        global messageId, messageContent, messageTimestamp, isMonitoring
        if not isMonitoring:
            return
        if edited_event.message.id == messageId:
            messageContent, messageTimestamp = edited_event.message.text, datetime.now()
            includesBotEmoji = "NÃO"
            if awaitForMessage[0] in messageContent:
                includesBotEmoji = "SIM"
            msg = {
                "e": e,
                "txt": f"MENSAGEM ALTERADA: {awaitForMessage[0]} [{includesBotEmoji}]",
            }
            logConsole(msg)

    # '/reset' + APAGAR MENSAGENS
    async def messagesReset():
        await clientTelegram.send_message(telegramChatName, "/reset")
        await asyncio.sleep(2)
        async for message in clientTelegram.iter_messages(telegramChatName):
            await message.delete()

    # ----------------------------------------------------------------------------------------------------------------------------

    # ENVIAR MENSAGEM
    async def providerTelegram(inf):
        global messageId, messageContent, messageTimestamp, isMonitoring
        content = ""
        if inf["messagePrompt"] == "reset":
            # RESETAR BOT E LIMPAR CONVERSA
            asyncio.create_task(messagesReset())
            return "COMANDO: reset"
        if inf["messageFile"] is None:
            # MENSAGEM: TEXTO
            logConsole({"e": e, "txt": "OK providerTelegram"})
            await clientTelegram.send_message(telegramChatName, inf["messagePrompt"])
        elif inf["messageFile"]:
            # MENSAGEM: ARQUIVO
            await clientTelegram.send_file(telegramChatName, inf["messageFile"])
        else:
            content = "TIPO NÃO IDENTIFICADO"
            return content
        isMonitoring = True
        start_wait_time = datetime.now()
        try:
            while True:
                if (datetime.now() - start_wait_time).total_seconds() > 60:
                    isMonitoring = False
                    logConsole({"e": e, "txt": "MENSAGEM NÃO RECEBIDA"})
                    messageId, messageContent, messageTimestamp = None, "", None
                    return False
                await asyncio.sleep(1.5)
                if messageContent and any(
                    item in messageContent for item in awaitForMessage
                ):
                    start_time = datetime.now()
                    while messageContent and any(
                        item in messageContent for item in awaitForMessage
                    ):
                        await asyncio.sleep(1)
                        if (datetime.now() - start_time).total_seconds() > 1:
                            isMonitoring = False
                            logConsole({"e": e, "txt": "# MENSAGEM COMPLETA #"})
                            messageContent = re.sub(
                                r".*\n\n", "", messageContent, count=1
                            )
                            messageContentKeep = messageContent
                            messageId, messageContent, messageTimestamp = None, "", None
                            return messageContentKeep
        except asyncio.CancelledError:
            isMonitoring = False
            # RESETAR VARIÁVEIS
            messageId, messageContent, messageTimestamp = None, "", None
            return False

except Exception as exceptErr:
    errAll({"e": e, "err": exceptErr, "msg": f"CÓDIGO INTEIRO\n{str(exceptErr)}"})
