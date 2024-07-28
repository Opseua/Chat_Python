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

from historyJson import historyGet, historySet


def chatNew(inf):
    """IGNORE"""
    chatId = inf["chatId"]
    model = inf["model"]
    timestampUser = inf["timestampUser"]
    timestampAssistant = inf["timestampAssistant"]
    message = inf["message"]
    response = inf["response"]

    # LER HISTÓRICO
    retHistoryGet = historyGet()
    chats = retHistoryGet["chats"]

    # INF DA NOVA CONVERSA
    chatNewInf = {
        "timestampCreate": timestampUser,
        "timestampEdit": timestampAssistant,
        "model": model,
        "chatId": chatId,
        "messages": [
            {"timestampCreate": timestampUser, "role": "user", "content": message},
            {
                "timestampCreate": timestampAssistant,
                "role": "assistant",
                "content": response,
            },
        ],
    }

    # ACIONAR CONVERSA AO HISTÓRICO
    chats.append(chatNewInf)
    retHistoryGet["chats"] = chats
    historySet(retHistoryGet)
