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


def chatAddMessage(inf):
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

    for chat in chats:
        if chat["chatId"] == chatId:
            chat["messages"].append(
                {"timestampCreate": timestampUser, "role": "user", "content": message}
            )
            chat["messages"].append(
                {
                    "timestampCreate": timestampAssistant,
                    "role": "assistant",
                    "content": response,
                }
            )
            chat["timestampEdit"] = timestampAssistant
            chat["model"] = model
            break

    # ACIONAR CONVERSA AO HISTÓRICO
    retHistoryGet["chats"] = chats
    historySet(retHistoryGet)
