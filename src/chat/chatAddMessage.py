# ARQUIVO ATUAL
e = __file__

try:
    # FUNÇÕES DE ARQUIVOS
    from chatHistoryJson import historyGet, historySet

    def chatAddMessage(inf):
        chatId = inf["chatId"]
        provider = inf["provider"]
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
                    {
                        "timestampCreate": timestampUser,
                        "role": "user",
                        "content": message,
                    }
                )
                chat["messages"].append(
                    {
                        "timestampCreate": timestampAssistant,
                        "role": "assistant",
                        "content": response,
                    }
                )
                chat["timestampEdit"] = timestampAssistant
                chat["provider"] = provider
                chat["model"] = model
                break

        # ACIONAR CONVERSA AO HISTÓRICO
        retHistoryGet["chats"] = chats
        historySet(retHistoryGet)

except Exception as exceptErr:
    errAll({"e": e, "err": exceptErr, "txt": f"CÓDIGO INTEIRO\n{str(exceptErr)}"})
