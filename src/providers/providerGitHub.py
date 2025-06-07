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
    json = infGlobal["json"]
    datetime = infGlobal["datetime"]
    os = infGlobal["os"]

    # BIBLIOTECAS: NECESSÁRIO INSTALAR → pip install brotli mitmproxy
    from openai import OpenAI

    # VARIÁVEIS
    apiZukijourneyBaseUrl = infGlobal["apiZukijourneyBaseUrl"]
    apiZukijourneyApiKey = infGlobal["apiZukijourneyApiKey"]
    apiNagaBaseUrl = infGlobal["apiNagaBaseUrl"]
    apiNagaApiKey = infGlobal["apiNagaApiKey"]
    apiFresedgptBaseUrl = infGlobal["apiFresedgptBaseUrl"]
    apiFresedgptApiKey = infGlobal["apiFresedgptApiKey"]
    apiZanityAiBaseUrl = infGlobal["apiZanityAiBaseUrl"]
    apiZanityAiApiKey = infGlobal["apiZanityAiApiKey"]
    apiWebraftAiBaseUrl = infGlobal["apiWebraftAiBaseUrl"]
    apiWebraftAiApiKey = infGlobal["apiWebraftAiApiKey"]

    # MODELOS
    models = f"{projectPath}/src/providers/models"

    # [zukijourney]
    pathZukijourney = f"{models}/zukijourney.json"
    with open(pathZukijourney, "r", encoding="utf-8") as f:
        data = json.load(f)
    modelsZukijourney = [
        {"id": m["id"], "owned_by": m["owned_by"], "is_free": m["is_free"]}
        for m in data.get("data", [])
        if m.get("is_free")
    ]
    with open(pathZukijourney, "w", encoding="utf-8") as f:
        json.dump({"data": modelsZukijourney}, f, ensure_ascii=False, indent=4)

    # [naga]
    pathNaga = f"{models}/naga.json"
    with open(pathNaga, "r", encoding="utf-8") as f:
        data = json.load(f)
    modelsNaga = [{"id": m["id"]} for m in data.get("data", [])]

    # ------------------------------------------------------ OPENAI ------------------------------------------------------------
    # CLIENT

    # [Zukijourney] → 'zukijourney'
    clientZukijourney = OpenAI(
        base_url=apiZukijourneyBaseUrl, api_key=apiZukijourneyApiKey
    )

    # [Naga] → 'naga'
    clientNaga = OpenAI(base_url=apiNagaBaseUrl, api_key=apiNagaApiKey)

    # [Fresedgpt] → 'fresedgpt'
    clientFresedgpt = OpenAI(base_url=apiFresedgptBaseUrl, api_key=apiFresedgptApiKey)

    # [ZanityAI] → 'zanityAi'
    clientZanityAi = OpenAI(base_url=apiZanityAiBaseUrl, api_key=apiZanityAiApiKey)

    # [WebraftAI] → 'webraftAi'
    clientWebraftAi = OpenAI(base_url=apiWebraftAiBaseUrl, api_key=apiWebraftAiApiKey)
    msg = {
        "e": e,
        "txt": "RODANDO → CLIENTE API",
    }
    logConsole(msg)

    # ENVIAR MENSAGEM
    async def providerGitHub(inf):
        provider = inf["provider"]
        response = None
        try:
            logConsole({"e": e, "txt": "OK providerGitHub"})
            clients = {
                "zukijourney": clientZukijourney,
                "naga": clientNaga,
                "fresedgpt": clientFresedgpt,
                "zanityAi": clientZanityAi,
                "webraftAi": clientWebraftAi,
            }
            if provider in clients:
                response = clients[provider].chat.completions.create(
                    model=inf["model"],
                    messages=json.loads(inf["messagePrompt"]),
                )
        except Exception as exceptErr:
            return {
                "ret": False,
                "msg": f"providerGitHub: ERRO | AO ENVIAR MENSAGEM [{exceptErr}]",
            }

        if response:
            # RESPOSTA RECEBIDA
            return {
                "ret": True,
                "msg": "providerGitHub: OK",
                "res": response.choices[0].message.content,
            }
        else:
            # RESPOSTA NÃO RECEBIDA
            return {
                "ret": False,
                "msg": "providerGitHub: ERRO | RESPOSTA NÃO RECEBIDA",
            }

except Exception as exceptErr:
    errAll({"e": e, "err": exceptErr, "txt": f"CÓDIGO INTEIRO\n{str(exceptErr)}"})
