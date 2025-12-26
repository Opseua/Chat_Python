# ARQUIVO ATUAL
e = __file__

try:
    # FUNÇÕES DE ARQUIVOS
    from chatHistoryJson import historyGet, historySet

    def chatNew(inf):
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

        # INF DA NOVA CONVERSA
        chatNewInf = {
            "timestampCreate": timestampUser,
            "timestampEdit": timestampAssistant,
            "chatId": chatId,
            "provider": provider,
            "model": model,
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
        chats.insert(0, chatNewInf)  # ADICIONAR NO INÍCIO
        # chats.append(chatNewInf)  # ADICIONAR NO FIM
        retHistoryGet["chats"] = chats
        historySet(retHistoryGet)

except Exception as exceptErr:
    errAll({"e": e, "err": exceptErr, "txt": f"CÓDIGO INTEIRO\n{str(exceptErr)}"})
