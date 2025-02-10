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

# IMPORTAR 'export.py'
from export import infGlobal
from export import errAll
from export import logConsole

# BIBLIOTECAS: NATIVAS
import os

try:
    # BIBLIOTECAS: NATIVAS
    json = infGlobal["json"]

    # BIBLIOTECAS: NECESSÁRIO INSTALAR → pip install brotli mitmproxy
    from openai import OpenAI

    # VARIÁVEIS [https://cas.zukijourney.com/]
    apiZukijourneyBaseUrl = infGlobal["apiZukijourneyBaseUrl"]
    apiZukijourneyApiKey = infGlobal["apiZukijourneyApiKey"]
    apiNagaBaseUrl = infGlobal["apiNagaBaseUrl"]
    apiNagaApiKey = infGlobal["apiNagaApiKey"]
    apiShardBaseUrl = infGlobal["apiShardBaseUrl"]
    apiShardApiKey = infGlobal["apiShardApiKey"]
    apiFresedgptBaseUrl = infGlobal["apiFresedgptBaseUrl"]
    apiFresedgptApiKey = infGlobal["apiFresedgptApiKey"]
    apiZanityAiBaseUrl = infGlobal["apiZanityAiBaseUrl"]
    apiZanityAiApiKey = infGlobal["apiZanityAiApiKey"]
    apiWebraftAiBaseUrl = infGlobal["apiWebraftAiBaseUrl"]
    apiWebraftAiApiKey = infGlobal["apiWebraftAiApiKey"]

    # ------------------------------------------------------ OPENAI ------------------------------------------------------------
    # CLIENT

    # [Zukijourney] → 'zukijourney'
    clientZukijourney = OpenAI(
        base_url=apiZukijourneyBaseUrl, api_key=apiZukijourneyApiKey
    )

    # [Naga] → 'naga'
    clientNaga = OpenAI(base_url=apiNagaBaseUrl, api_key=apiNagaApiKey)

    # [Shard] → 'shard'
    clientShard = OpenAI(base_url=apiShardBaseUrl, api_key=apiShardApiKey)

    # [Fresedgpt] → 'fresedgpt'
    clientFresedgpt = OpenAI(base_url=apiFresedgptBaseUrl, api_key=apiFresedgptApiKey)

    # [ZanityAI] → 'zanityAi'
    clientZanityAi = OpenAI(base_url=apiZanityAiBaseUrl, api_key=apiZanityAiApiKey)

    # [WebraftAI] → 'webraftAi'
    clientWebraftAi = OpenAI(base_url=apiWebraftAiBaseUrl, api_key=apiWebraftAiApiKey)

    printMsg = "RODANDO → CLIENTE API"
    logConsole(printMsg)
    print(printMsg)

    # ENVIAR MENSAGEM
    async def messageSendOpenAi(inf):
        model = inf["model"]
        messagePrompt = json.loads(inf["messagePrompt"])
        provider = inf["provider"]
        response = None
        try:
            if provider == "zukijourney":
                response = clientZukijourney.chat.completions.create(
                    model=model,
                    messages=messagePrompt,
                )
            elif provider == "naga":
                response = clientNaga.chat.completions.create(
                    model=model,
                    messages=messagePrompt,
                )
            elif provider == "shard":
                response = clientShard.chat.completions.create(
                    model=model,
                    messages=messagePrompt,
                )
            elif provider == "fresedgpt":
                response = clientFresedgpt.chat.completions.create(
                    model=model,
                    messages=messagePrompt,
                )
            elif provider == "zanityAi":
                response = clientZanityAi.chat.completions.create(
                    model=model,
                    messages=messagePrompt,
                )
            elif provider == "webraftAi":
                response = clientWebraftAi.chat.completions.create(
                    model=model,
                    messages=messagePrompt,
                )

        except Exception as e:
            errAll(e)
            print(str(e))

        if response:
            # RESPOSTA RECEBIDA
            response = response.choices[0].message.content
        else:
            # RESPOSTA NÃO RECEBIDA
            response = False

        return response

except Exception as exceptErr:
    errAll(exceptErr)
    print("CÓDIGO INTEIRO [messageSendOpenAi]", exceptErr)
    os._exit(1)
