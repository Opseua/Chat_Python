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

from historyJson import historyGet


def historyMessages(inf):
    """IGNORE"""
    chatId = inf["chatId"]
    includesInMessages = inf["includesInMessages"]

    retHistoryGet = historyGet()
    chats = retHistoryGet["chats"]
    messagesRes = {
        "timestampCreate": False,
        "timestampEdit": False,
        "model": False,
        "chatId": False,
        "messages": [],
    }

    # PEGAR HISTÓRICO
    for chat in chats:
        if chat["chatId"] == chatId:
            messages = chat["messages"]
            # ADICIONAR INFORMAÇÕES DA MENSAGEM
            messagesRes["timestampCreate"] = chat["timestampCreate"]
            messagesRes["timestampEdit"] = chat["timestampEdit"]
            messagesRes["model"] = chat["model"]
            messagesRes["chatId"] = chat["chatId"]
            # INCLUIR APENAS AS CHAVES INFORMADAS
            for message in messages:
                filtered_message = {
                    key: message[key] for key in includesInMessages if key in message
                }
                messagesRes["messages"].append(filtered_message)

    # RETURN
    if not messagesRes["messages"]:
        return {
            "ret": False,
            "msg": "CHAT [HISTORYMESSAGES]: ERRO | NAO ENCONTRADO 'chatId'",
        }

    return {
        "ret": True,
        "msg": "CHAT [HISTORYMESSAGES]: OK",
        "res": [messagesRes],
    }
