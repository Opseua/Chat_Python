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
