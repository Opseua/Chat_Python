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
    json = infGlobal["json"]

    # BIBLIOTECAS: NECESSÁRIO INSTALAR → pip install brotli mitmproxy
    from openai import OpenAI

    # VARIÁVEIS
    openAiZukiJourneyBaseUrl = infGlobal["openAiZukiJourneyBaseUrl"]
    openAiZukiJourneyApiKey = infGlobal["openAiZukiJourneyApiKey"]
    openAiNagaBaseUrl = infGlobal["openAiNagaBaseUrl"]
    openAiNagaApiKey = infGlobal["openAiNagaApiKey"]

    # ------------------------------------------------------ OPENAI ------------------------------------------------------------
    # CLIENT

    # [ZukiJourney]
    clientZukiJourney = OpenAI(
        base_url=openAiZukiJourneyBaseUrl, api_key=openAiZukiJourneyApiKey
    )

    # [Naga]
    clientNaga = OpenAI(base_url=openAiNagaBaseUrl, api_key=openAiNagaApiKey)

    print("RODANDO → CLIENTE OPENAI [ZukiJourney/Naga]")

    # ENVIAR MENSAGEM
    async def messageSendOpenAi(inf):
        model = inf["model"]
        messagePrompt = json.loads(inf["messagePrompt"])
        provider = inf["provider"]
        response = None
        try:
            if provider == "zukiJourney":
                response = clientZukiJourney.chat.completions.create(
                    model=model,
                    messages=messagePrompt,
                )
            elif provider == "naga":  # https://api.naga.ac/v1/limits
                response = clientNaga.chat.completions.create(
                    model=model,
                    messages=messagePrompt,
                )
        except Exception as e:
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
