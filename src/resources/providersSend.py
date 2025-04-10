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
    datetime = infGlobal["datetime"]

    # FUNÇÕES DE ARQUIVOS
    from providerG4f import providerG4f
    from providerGitHub import providerGitHub
    from providerTelegram import providerTelegram

    async def multipleProvidersSend(inf):
        provider = inf["provider"]
        model = inf["model"]
        messagePrompt = inf["messagePrompt"]
        messageFile = inf["messageFile"]
        msg = {
            "e": e,
            "txt": f"ENVIANDO PARA → {provider}",
        }
        logConsole(msg)
        retMessageSend = None
        if provider == "telegram":
            # *** TELEGRAN [gpt-4o]
            retMessageSend = await providerTelegram(
                {"messagePrompt": messagePrompt, "messageFile": messageFile}
            )
            if messageFile:
                # PROSSEGUIR COM O ARQUIVO
                retMessageSend = await providerTelegram(
                    {"messagePrompt": messagePrompt, "messageFile": None}
                )
            # RESETAR E LIMPAR CONVERSA
            asyncio.create_task(
                providerTelegram({"messagePrompt": "reset", "messageFile": None})
            )
        elif provider == "g4f":
            # *** G4F [gpt-4o]
            model = model or "gpt-4o-mini"
            retMessageSend = await g4f({"model": model, "messagePrompt": messagePrompt})
        elif provider in ["zukijourney", "naga", "fresedgpt", "zanityAi", "webraftAi"]:
            # *** GitHub [multiplos]
            model = model or "gpt-4o-mini"
            retMessageSend = await providerGitHub(
                {"model": model, "messagePrompt": messagePrompt, "provider": provider}
            )
        return {
            "ret": retMessageSend["ret"],
            "msg": retMessageSend["msg"],
            "provider": retMessageSend["provider"],
            "model": retMessageSend["model"],
            "res": retMessageSend["res"],
        }

    async def providersSend(inf):
        # ENVIAR MENSAGEM PARA VÁRIOS BOTS SIMULTANEAMENTE
        tasks = {
            asyncio.create_task(
                multipleProvidersSend(
                    {
                        "provider": provider,
                        "model": inf["model"],
                        "messagePrompt": inf["messagePrompt"],
                        "messageFile": inf["messageFile"],
                    }
                )
            ): provider
            for provider in inf["providers"]
        }
        done, pending = await asyncio.wait(
            tasks.keys(), return_when=asyncio.FIRST_COMPLETED
        )
        first_response = None
        for task in done:
            first_response = task.result()
            if first_response:
                # PEGAR A PRIMEIRA RESPOSTA
                break
        for task in pending:
            # ENCERRAR OUTROS BOT's
            msg = {
                "e": e,
                "txt": f"ENCERRANDO {tasks[task]}",
            }
            logConsole(msg)
            task.cancel()

        # Aguarda o cancelamento das pendentes
        for task in pending:
            try:
                await task
            except asyncio.CancelledError:
                pass

        # RETORNAR A PRIMEIRA RESPOSTA
        return first_response

except Exception as exceptErr:
    errAll({"e": e, "err": exceptErr, "msg": f"CÓDIGO INTEIRO\n{str(exceptErr)}"})
