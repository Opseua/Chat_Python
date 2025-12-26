# ARQUIVO ATUAL
e = __file__

try:
    # BIBLIOTECAS: NATIVAS
    json = infGlobal["json"]
    httpx = infGlobal["httpx"]

    # VARIÁVEIS
    apiOpenAiBaseUrl = infGlobal["apiOpenAiBaseUrl"]
    apiOpenAiApiKey = infGlobal["apiOpenAiApiKey"]

    # ------------------------------------------------------ OPENAI ------------------------------------------------------------

    # ENVIAR MENSAGEM
    async def providerOpenAi(inf):
        model = inf["model"]
        response = None
        url = f"{apiOpenAiBaseUrl}/chat/completions"
        print(url)
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {apiOpenAiApiKey}",
        }
        try:
            logConsole({"e": e, "txt": "OK providerOpenAi"})

            retApi = await api(
                {
                    "e": e,
                    "method": "POST",
                    "url": url,
                    "headers": headers,
                    "body": {
                        "messages": inf["messagePrompt"],
                        "model": inf["model"],
                        "store": True,
                    },
                }
            )
            print(retApi, inf["model"])
            sys.exit("Finalizando o script de propósito")

            async with httpx.AsyncClient() as client:
                res = await client.post(
                    url,
                    headers=headers,
                    json={"model": model, "messages": json.loads(inf["messagePrompt"])},
                )
            print(">>> status_code:", res.status_code)  # para garantir que chegou aqui
            if res.status_code == 200:
                response = await res.json()
                print(">>> RESPOSTA OPENAI:", response)
            else:
                print(">>> ERRO NA REQUISIÇÃO:", await res.text())
        except Exception as exceptErr:
            print(">>> EXCEÇÃO CAPTURADA:", exceptErr)
            return {
                "ret": False,
                "msg": f"providerOpenAi: ERRO | AO ENVIAR MENSAGEM [{exceptErr}]",
            }

        if response:
            # RESPOSTA RECEBIDA
            return {
                "ret": True,
                "msg": "providerOpenAi: OK",
                "res": response["choices"][0]["message"]["content"],
            }
        else:
            # RESPOSTA NÃO RECEBIDA
            return {
                "ret": False,
                "msg": "providerOpenAi: ERRO | RESPOSTA NÃO RECEBIDA",
            }

except Exception as exceptErr:
    errAll({"e": e, "err": exceptErr, "txt": f"CÓDIGO INTEIRO\n{str(exceptErr)}"})
