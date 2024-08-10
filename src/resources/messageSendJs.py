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
from export import api

# BIBLIOTECAS: NATIVAS
import os

try:
    # BIBLIOTECAS: NATIVAS
    json = infGlobal["json"]

    # VARIÁVEIS
    securityPass = infGlobal["securityPass"]
    hostPortLocJs = infGlobal["hostPortLocJs"]

    # ------------------------------------------------------ JS [NODEJS] ------------------------------------------------------------

    # ENVIAR MENSAGEM:
    async def messageSendJs(inf):
        messagePrompt = inf["messagePrompt"]
        inf = {
            "url": hostPortLocJs,
            "method": "POST",
            "headers": {"Content-Type": "application/json", "raw": "True"},
            "body": {
                "fun": [
                    {
                        "securityPass": securityPass,
                        "retInf": True,
                        "name": "chat",
                        "par": {
                            "provider": "gitHub",
                            "input": messagePrompt,
                        },
                    }
                ]
            },
        }
        response = None
        try:
            retApi = await api(inf)
            if retApi.get("ret"):
                response = retApi.get("res", {}).get("body", None)
        except Exception as e:
            print(str(e))

        return response

except Exception as exceptErr:
    errAll(exceptErr)
    print("CÓDIGO INTEIRO [messageSendJs]", exceptErr)
    os._exit(1)
