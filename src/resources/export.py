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
ee = __file__

# BIBLIOTECAS: NATIVAS
import os, sys, time, random, string, json, re, threading, signal, builtins
from datetime import datetime

# BIBLIOTECAS: NECESSÁRIO INSTALAR
import asyncio
import aiohttp_cors
from aiohttp import web
import httpx

# VARIÁVEIS
fileChrome_Extension = os.getenv("fileChrome_Extension").replace(r"\\", "/")

# CONFIG.json
fullPathJson, config = (os.path.abspath(f"{fileChrome_Extension}/src/config.json"), "")
with open(fullPathJson, "r", encoding="utf-8") as file:
    config = json.load(file)

# MASTER.json
fullPathMaster, master = (
    os.path.abspath(f"{fileChrome_Extension}/src/master.json"),
    "",
)
with open(fullPathMaster, "r", encoding="utf-8") as file:
    master = json.load(file)
config["master"] = master["master"]

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
    "master": config["master"],
    "hostPortLocJs": config["chatPython"]["hostPortLocJs"],
    "portServerHttp": config["chatPython"]["portServerHttp"],
    "portG4fFrontEnd": config["chatPython"]["portG4fFrontEnd"],
    "telegramApiId": config["chatPython"]["telegramApiId"],
    "telegramApiHash": config["chatPython"]["telegramApiHash"],
    "telegramChatName": config["chatPython"]["telegramChatName"],
    "apiZukijourneyBaseUrl": config["chatPython"]["apiZukijourneyBaseUrl"],
    "apiZukijourneyApiKey": config["chatPython"]["apiZukijourneyApiKey"],
    "apiNagaBaseUrl": config["chatPython"]["apiNagaBaseUrl"],
    "apiNagaApiKey": config["chatPython"]["apiNagaApiKey"],
    "apiFresedgptBaseUrl": config["chatPython"]["apiFresedgptBaseUrl"],
    "apiFresedgptApiKey": config["chatPython"]["apiFresedgptApiKey"],
    "apiZanityAiBaseUrl": config["chatPython"]["apiZanityAiBaseUrl"],
    "apiZanityAiApiKey": config["chatPython"]["apiZanityAiApiKey"],
    "apiWebraftAiBaseUrl": config["chatPython"]["apiWebraftAiBaseUrl"],
    "apiWebraftAiApiKey": config["chatPython"]["apiWebraftAiApiKey"],
}

# ----------------------------------------------------------------------------------------------------------------------

# DATEHOUR
dias_da_semana, meses = ["DOM", "SEG", "TER", "QUA", "QUI", "SEX", "SAB"], json.loads(
    '["JAN", "FEV", "MAR", "ABR", "MAI", "JUN", "JUL", "AGO", "SET", "OUT", "NOV", "DEZ"]'
)


def dateHour():
    agora = datetime.now()
    milissegundos = int(agora.strftime("%f")) // 1000
    tim = agora.strftime("%H%M%S") + agora.strftime("%f")[:4]
    timMil = tim + str(milissegundos).zfill(3)
    data_hora_formatada = {
        "day": agora.strftime("%d"),
        "mon": agora.strftime("%m"),
        "yea": agora.strftime("%Y"),
        "hou": agora.strftime("%H"),
        "hou12": agora.strftime("%I"),
        "houAmPm": agora.strftime("%p"),
        "min": agora.strftime("%M"),
        "sec": agora.strftime("%S"),
        "mil": str(milissegundos).zfill(3),
        "tim": tim[:10],
        "timMil": timMil[:13],
        "dayNam": dias_da_semana[agora.weekday()],
        "monNam": meses[agora.month - 1],
    }
    return {"ret": True, "msg": "DATE HOUR: OK", "res": data_hora_formatada}


# ----------------------------------------------------------------------------------------------------------------------


# REGISTRAR ERROS
def errAll(inf):
    e = inf.get("e", ee)
    txt = inf.get("txt", "")
    err = inf.get("err", "")
    retDateHour = dateHour()["res"]
    day = retDateHour["day"]
    mon = retDateHour["mon"]
    monNam = retDateHour["monNam"]
    hou = retDateHour["hou"]
    minOk = retDateHour["min"]
    sec = retDateHour["sec"]
    mil = retDateHour["mil"]
    dateNowMon = f"MES_{mon}_{monNam}"
    dateNowDay = f"DIA_{day}"
    fileName = (
        f"logs/Python/{dateNowMon}/{dateNowDay}/{hou}.{minOk}.{sec}.{mil}_err.txt"
    )
    os.makedirs(os.path.dirname(fileName), exist_ok=True)
    err = f"{str(err)}"
    with open(fileName, "a", encoding="utf-8") as file:
        file.write(err)
    logConsole({"e": e, "txt": txt})
    os._exit(1)


# ----------------------------------------------------------------------------------------------------------------------


# API
async def api(inf):
    ret = {"ret": False}
    try:
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


# LOGCONSOLE
def logConsole(inf):
    e = inf.get("e", "Desconhecido")
    msg = inf.get("msg", "")
    write = inf.get("write", True)
    timestamp = datetime.now().strftime("%d/%m %H:%M:%S.%f")[:-3]
    if isinstance(msg, dict) or isinstance(msg, list):
        msg = json.dumps(msg, indent=4)
    cores = {
        "amarelo": "\x1b[33m",
        "azul": "\x1b[34m",
        "verde": "\x1b[32m",
        "vermelho": "\x1b[31m",
        "reset": "\x1b[0m",
    }
    timestamp_formatted = f"{cores['verde']}{timestamp}{cores['reset']}"
    file_formatted = f"{cores['azul']}{os.path.basename(e)}{cores['reset']}"
    print(f"→ {timestamp_formatted} {file_formatted}\n{msg}\n")
    if write:
        retDateHour = dateHour()["res"]
        day = retDateHour["day"]
        mon = retDateHour["mon"]
        monNam = retDateHour["monNam"]
        hou = retDateHour["hou"]
        minOk = retDateHour["min"]
        sec = retDateHour["sec"]
        mil = retDateHour["mil"]
        dateNowMon = f"MES_{mon}_{monNam}"
        dateNowDay = f"DIA_{day}"
        if isinstance(msg, dict) or isinstance(msg, list):
            msg = json.dumps(msg, indent=4)
        dateInFile = f"→ {hou}:{minOk}:{sec}.{mil} {os.path.basename(e)}\n{str(msg)}"
        fileName = f"logs/Python/{dateNowMon}/{dateNowDay}/{hou}.00-{hou}.59_log.txt"
        os.makedirs(os.path.dirname(fileName), exist_ok=True)
        err = f"{dateInFile}\n\n"
        with open(fileName, "a", encoding="utf-8") as file:
            file.write(err)


# EXPORTAR GLOBALMENTE
builtins.infGlobal = infGlobal
builtins.dateHour = dateHour
builtins.errAll = errAll
builtins.api = api
builtins.logConsole = logConsole
