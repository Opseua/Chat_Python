"""IGNORE"""

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

import json
import os

pathChats = "log/chats.json"


def historyGet():
    """IGNORE"""
    if not os.path.exists(pathChats):
        historySet({"chats": []})
        return {"chats": []}
    with open(pathChats, "r", encoding="utf-8") as file:
        return json.load(file)


def historySet(inf):
    """IGNORE"""
    # SALVAR NO ARQUIVO
    with open(pathChats, "w", encoding="utf-8") as file:
        json.dump(inf, file, ensure_ascii=False, indent=4)
