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

# BIBLIOTECAS: NATIVAS
import os, sys, time, asyncio, random, string, json, re, threading, signal, httpx
from datetime import datetime
import aiohttp_cors


# BIBLIOTECAS: NECESSÁRIO INSTALAR → pip install brotli mitmproxy
from aiohttp import web

# VARIÁVEIS
fileChrome_Extension = os.getenv("fileChrome_Extension").replace(r"\\", "/")
fullPathJson, config = (os.path.abspath(f"{fileChrome_Extension}/src/config.json"), "")
with open(fullPathJson, "r", encoding="utf-8") as file:
    config = json.load(file)

# EXPORTAR GLOBALMENTE
infGlobal = {
    "asyncio": asyncio,
    "sys": sys,
    "time": time,
    "os": os,
    "random": random,
    "string": string,
    "json": json,
    "re": re,
    "threading": threading,
    "signal": signal,
    "httpx": httpx,
    "datetime": datetime,
    "aiohttp_cors": aiohttp_cors,
    "x": "x",
    "web": web,
    "x1": "x",
    "securityPass": config["webSocket"]["securityPass"],
    "hostPortLocJs": config["chatPython"]["hostPortLocJs"],
    "portServerHttp": config["chatPython"]["portServerHttp"],
    "portG4fFrontEnd": config["chatPython"]["portG4fFrontEnd"],
    "telegramApiId": config["chatPython"]["telegramApiId"],
    "telegramApiHash": config["chatPython"]["telegramApiHash"],
    "telegramChatName": config["chatPython"]["telegramChatName"],
    "openAiZukiJourneyBaseUrl": config["chatPython"]["openAiZukiJourneyBaseUrl"],
    "openAiZukiJourneyApiKey": config["chatPython"]["openAiZukiJourneyApiKey"],
    "openAiNagaBaseUrl": config["chatPython"]["openAiNagaBaseUrl"],
    "openAiNagaApiKey": config["chatPython"]["openAiNagaApiKey"],
}


# REGISTRAR ERROS
def errAll(exceptErr):
    dateNow = datetime.now()
    dateNowMon = f"MES_{dateNow.strftime('%m')}_{dateNow.strftime('%b').upper()}"
    dateNowDay = f"DIA_{dateNow.strftime('%d')}"
    dateNowHou = f"{dateNow.strftime('%H')}"
    dateNowMin = f"{dateNow.strftime('%M')}"
    dateNowSec = f"{dateNow.strftime('%S')}"
    dateNowMil = f"{dateNow.microsecond // 1000:03d}"
    fileName = f"log/Python/{dateNowMon}/{dateNowDay}/{dateNowHou}.{dateNowMin}.{dateNowSec}.{dateNowMil}_err.txt"
    os.makedirs(os.path.dirname(fileName), exist_ok=True)
    err = f"{str(exceptErr)}\n\n"
    with open(fileName, "a", encoding="utf-8") as file:
        file.write(err)


# ----------------------------------------------------------------------------------------------------------------------


# API
async def api(inf):
    ret = {"ret": False}
    e = inf.get("e", None)
    try:
        req = None
        resCode = None
        resHeaders = None
        resBody = None
        body = None
        reqOk = False
        reqE = None
        # HEADERS
        reqOpt = {
            "method": inf["method"],
            "headers": inf.get("headers", {}),
            # TEMPO LIMITE [PADRÃO 20 SEGUNDOS]
            "timeout": inf.get("max", 20),
        }
        # BODY
        if inf.get("body") and reqOpt["method"] in ["POST", "PUT"]:
            if "x-www-form-urlencoded" not in json.dumps(reqOpt["headers"]):
                # ###### → json/object | text
                body = (
                    json.dumps(inf["body"])
                    if isinstance(inf["body"], dict)
                    else inf["body"]
                )
            else:
                #  ###### → x-www-form-urlencoded
                if not isinstance(inf["body"], dict) or not inf["body"]:
                    ret["msg"] = (
                        "API: ERRO | 'body' NÃO É OBJETO [x-www-form-urlencoded]"
                    )
                    return ret
                body = "&".join(
                    [f"{key}={value}" for key, value in inf["body"].items()]
                )
        #  ################ PYTHON
        async with httpx.AsyncClient(timeout=reqOpt["timeout"]) as client:
            try:
                if body:
                    response = await client.request(
                        reqOpt["method"],
                        inf["url"],
                        data=body,
                        headers=reqOpt["headers"],
                    )
                else:
                    response = await client.request(
                        reqOpt["method"], inf["url"], headers=reqOpt["headers"]
                    )

                resCode = response.status_code
                resHeaders = dict(response.headers)
                resBody = response.text
                reqOk = True
            except httpx.RequestError as exc:
                reqE = exc
                if isinstance(exc, httpx.TimeoutException):
                    ret["msg"] = "API: ERRO | TEMPO MÁXIMO ATINGIDO"
            except Exception as exc:
                reqE = exc
        if not reqOk:
            ret["msg"] = ret.get(
                "msg", f"API: ERRO AO FAZER REQUISIÇÃO (NÃO NA FUNÇÃO)\n\n{reqE}"
            )
        else:
            ret["ret"] = True
            ret["msg"] = "API: OK"
            ret["res"] = {"code": resCode, "headers": resHeaders, "body": resBody}
    except Exception as catchErr:
        if not isinstance(catchErr, asyncio.TimeoutError):
            ret["msg"] = f"API: ERRO | {catchErr}"
    return ret


# ----------------------------------------------------------------------------------------------------------------------
