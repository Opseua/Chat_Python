# ARQUIVO ATUAL
e = __file__

try:
    # FUNÇÕES DE ARQUIVOS
    from chatHistoryJson import historyGet

    def chatHistory(inf):
        provider = inf["provider"]
        includesInMessages = inf["includesInMessages"]

        if includesInMessages is None:
            includesInMessages = []

        retHistoryGet = historyGet()
        chats = retHistoryGet["chats"]

        if provider and provider != "*":
            chats = [chat for chat in chats if chat["provider"] == provider]

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
                "msg": "CHAT [HISTORYCHAT]: ERRO | NAO ENCONTRADO 'provider'",
            }

        return {
            "ret": True,
            "msg": "CHAT [HISTORYCHAT]: OK",
            "res": historyLast,
        }

except Exception as exceptErr:
    errAll({"e": e, "err": exceptErr, "txt": f"CÓDIGO INTEIRO\n{str(exceptErr)}"})
