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
import os, sys, asyncio, random, string, json, re
from datetime import datetime
import aiohttp_cors

# BIBLIOTECAS: NECESSÁRIO INSTALAR → pip install brotli mitmproxy
from aiohttp import web

# VARIÁVEIS
fileChrome_Extension = os.getenv("fileChrome_Extension").replace(r"\\", "/")
fullPathJson, config = (os.path.abspath(f"{fileChrome_Extension}/src/config.json"), "")
with open(fullPathJson, "r", encoding="utf-8") as file:
    config = json.load(file)
port = config["chatPython"]["port"]
telegramApiId = config["chatPython"]["telegramApiId"]
telegramApiHash = config["chatPython"]["telegramApiHash"]
telegramChatName = config["chatPython"]["telegramChatName"]

# EXPORTAR GLOBALMENTE
infGlobal = {
    "asyncio": asyncio,
    "sys": sys,
    "os": os,
    "random": random,
    "string": string,
    "json": json,
    "re": re,
    "datetime": datetime,
    "aiohttp_cors": aiohttp_cors,
    "x": "x",
    "web": web,
    "x1": "x",
    "port": port,
    "telegramApiId": telegramApiId,
    "telegramApiHash": telegramApiHash,
    "telegramChatName": telegramChatName,
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
