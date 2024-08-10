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
# ERRO DE IMPORT 'datetime'
# pylint: disable=E1101

from chatHistoryJson import historyGet


def chatHistory(inf):
    model = inf["model"]
    includesInMessages = inf["includesInMessages"]

    if includesInMessages is None:
        includesInMessages = []

    retHistoryGet = historyGet()
    chats = retHistoryGet["chats"]

    if model and model != "*":
        chats = [chat for chat in chats if chat["model"] == model]

    # APENAS OS 10 ÚLTIMOS CHATS (COM CONVERSAS RECENTES)
    historyLast = sorted(chats, key=lambda x: x["timestampEdit"], reverse=True)[:10]

    # PEGAR HISTÓRICO
    for chat in historyLast:
        messages = chat["messages"]
        if len(messages) > 2:
            # APENAS AS 2 ÚLTIMAS MENSAGENS (USER+ASSISTANT)
            messages = messages[-2:]
        # INCLUIR APENAS AS CHAVES INFORMADAS
        filtered_messages = []
        for message in messages:
            filtered_message = {
                key: message[key] for key in includesInMessages if key in message
            }
            filtered_messages.append(filtered_message)
        chat["messages"] = filtered_messages

    # RETURN
    if not historyLast:
        return {
            "ret": False,
            "msg": "CHAT [HISTORYCHAT]: ERRO | NAO ENCONTRADO 'model'",
        }

    return {
        "ret": True,
        "msg": "CHAT [HISTORYCHAT]: OK",
        "res": historyLast,
    }
