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
    asyncio = infGlobal["asyncio"]
    re = infGlobal["re"]
    datetime = infGlobal["datetime"]

    # BIBLIOTECAS: NECESSÁRIO INSTALAR → pip install brotli mitmproxy
    from telethon import TelegramClient, events

    # VARIÁVEIS
    telegramApiId = "20633867"
    telegramApiHash = "f66a6c85c9b735acfe67c38ee8fdcb43"
    telegramChatName = "chatgpt68_bot"
    telegramClient = TelegramClient("log/session", telegramApiId, telegramApiHash)

    # ------------------------------------------------------ TELEGRAM ------------------------------------------------------------
    # CLIENT
    async def runClient():
        await telegramClient.start()
        print("RODANDO → CLIENTE TELEGRAM")

    # INICIAR
    loop = asyncio.get_event_loop()
    loop.run_until_complete(runClient())

    messageId, messageContent, messageTimestamp, isMonitoring = None, "", None, False
    awaitForMessage = ["🤖️", "Reset successfully!", "Upload successfully!"]

    # EVENTO: MENSAGEM RECEBIDA
    @telegramClient.on(events.NewMessage(from_users=telegramChatName))
    async def handler(event):
        global messageId, messageContent, messageTimestamp, isMonitoring
        if not isMonitoring:
            return
        messageId, messageContent = event.message.id, event.message.text
        messageTimestamp = datetime.now()
        print(f"MENSAGEM RECEBIDA: {messageContent}")

    # EVENTO: MENSAGEM EDITADA
    @telegramClient.on(events.MessageEdited(from_users=telegramChatName))
    async def handlerMessageEdited(edited_event):
        global messageId, messageContent, messageTimestamp, isMonitoring
        if not isMonitoring:
            return
        if edited_event.message.id == messageId:
            messageContent, messageTimestamp = edited_event.message.text, datetime.now()
            includesBotEmoji = "NÃO"
            if awaitForMessage[0] in messageContent:
                includesBotEmoji = "SIM"
            print(f"MENSAGEM ALTERADA: {awaitForMessage[0]} [{includesBotEmoji}]")

    # '/reset' + APAGAR MENSAGENS
    async def messagesReset():
        await telegramClient.send_message(telegramChatName, "/reset")
        await asyncio.sleep(2)
        async for message in telegramClient.iter_messages(telegramChatName):
            await message.delete()

    # ----------------------------------------------------------------------------------------------------------------------------

    # ENVIAR MENSAGEM: TELEGRAM
    async def messageSendTelegram(inf):
        global messageId, messageContent, messageTimestamp, isMonitoring
        content = ""
        if inf["messagePrompt"] == "reset":
            # RESETAR BOT E LIMPAR CONVERSA
            asyncio.create_task(messagesReset())
            return "COMANDO: reset"
        if inf["messageFile"] is None:
            # MENSAGEM: TEXTO
            await telegramClient.send_message(telegramChatName, inf["messagePrompt"])
        elif inf["messageFile"]:
            # MENSAGEM: ARQUIVO
            await telegramClient.send_file(telegramChatName, inf["messageFile"])
        else:
            content = "TIPO NÃO IDENTIFICADO"
            return content
        isMonitoring = True
        start_wait_time = datetime.now()
        try:
            while True:
                if (datetime.now() - start_wait_time).total_seconds() > 60:
                    isMonitoring = False
                    print("MENSAGEM NÃO RECEBIDA")
                    messageId, messageContent, messageTimestamp = None, "", None
                    return False
                await asyncio.sleep(1)
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
                            print("# MENSAGEM COMPLETA #")
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
    errAll(exceptErr)
    print("CÓDIGO INTEIRO")
    os._exit(1)


# {
#     "action": "historyChat",
#     "model": "*",
#     "includesInMessages": [
#         "role",
#         "content",
#         //"timestampCreate",
#         "x"
#     ]
# }

# {
#     "action": "historyMessages",
#     "chatId": "2024_08_03-19.17.50.609-DGW",
#     "includesInMessages": [
#         "role",
#          "content",
#         //"timestampCreate",
#         "x"
#     ]
# }

# {
#     "action": "messageSend",
#     "chatIdA": "2024_08_03-19.17.50.609-DGW",
#     "messagePrompt": "Qual a cor do céu?",
#     "messageFile": true,
#     "x": "x"
# }

# {
#     "action": "historyDelete",
#     "chatId": "2024_08_03-20.04.16.664-NQF",
#     "qtdDeleteMessages": 999,
#     "x": "x"
# }
