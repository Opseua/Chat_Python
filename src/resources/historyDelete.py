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


def historyDelete(inf):
    """IGNORE"""
    chatId = inf["chatId"]
    qtdDeleteMessages = inf["qtdDeleteMessages"]

    if qtdDeleteMessages == 0:
        return {
            "ret": False,
            "msg": "CHAT [HISTORYDELETE]: ERRO | INFORMAR O 'qtdDeleteMessages'",
        }

    if qtdDeleteMessages == "*":
        qtdDeleteMessages = 999

    retHistoryGet = historyGet()
    chats = retHistoryGet["chats"]

    # PROCURAR O CHAT PELO 'chatId'
    for i, chat in enumerate(chats):
        if chat["chatId"] == chatId:
            # REMOVER MENSAGENS (A PARTIR DA ÚLTIMA)
            if qtdDeleteMessages >= len(chat["messages"]):
                # EXCLUIR O CHAT (QUANDO NECESSÁRIO)
                del chats[i]
            else:
                chat["messages"] = chat["messages"][:-qtdDeleteMessages]
                # ATUALIZAR TIMESTAMP DA ÚLTIMA EDIÇÃO
                chat["timestampEdit"] = chat["messages"][-1]["timestampCreate"]

            # ATUALIZAR HISTÓRICO
            historySet({"chats": chats})
            return {
                "ret": True,
                "msg": "CHAT [HISTORYDELETE]: OK",
            }

    return {
        "ret": False,
        "msg": "CHAT [HISTORYDELETE]: ERRO | NAO ENCONTRADO 'chatId'",
    }
