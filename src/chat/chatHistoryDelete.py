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
e = __file__

try:
    # FUNÇÕES DE ARQUIVOS
    from chatHistoryJson import historyGet, historySet

    def chatHistoryDelete(inf):
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

except Exception as exceptErr:
    errAll({"e": e, "err": exceptErr, "txt": f"CÓDIGO INTEIRO\n{str(exceptErr)}"})
