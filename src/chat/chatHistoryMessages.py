# ARQUIVO ATUAL
e = __file__

try:
    # FUNÇÕES DE ARQUIVOS
    from chatHistoryDelete import historyGet

    def chatHistoryMessages(inf):
        chatId = inf["chatId"]
        includesInMessages = inf["includesInMessages"]

        retHistoryGet = historyGet()
        chats = retHistoryGet["chats"]

        messagesRes = {
            "timestampCreate": False,
            "timestampEdit": False,
            "chatId": False,
            "provider": False,
            "model": False,
            "messages": [],
        }

        # PEGAR HISTÓRICO
        for chat in chats:
            if chat["chatId"] == chatId:
                # ADICIONAR INFORMAÇÕES DA MENSAGEM
                messagesRes["timestampCreate"] = chat["timestampCreate"]
                messagesRes["timestampEdit"] = chat["timestampEdit"]
                messagesRes["chatId"] = chat["chatId"]
                messagesRes["provider"] = chat["provider"]
                messagesRes["model"] = chat["model"]
                messages = chat["messages"]

                # INCLUIR APENAS AS CHAVES INFORMADAS
                for message in messages:
                    filtered_message = {
                        key: message[key]
                        for key in includesInMessages
                        if key in message
                    }
                    messagesRes["messages"].append(filtered_message)

        # RETURN
        if not messagesRes["messages"]:
            return {
                "ret": False,
                "msg": "CHAT [HISTORYMESSAGES]: ERRO | NAO ENCONTRADO 'chatId'",
            }

        # Criar o resultado final garantindo a ordem das chaves
        result = {
            "ret": True,
            "msg": "CHAT [HISTORYMESSAGES]: OK",
            "res": [
                {
                    "timestampCreate": messagesRes["timestampCreate"],
                    "timestampEdit": messagesRes["timestampEdit"],
                    "chatId": messagesRes["chatId"],
                    "provider": messagesRes["provider"],
                    "model": messagesRes["model"],
                    "messages": messagesRes["messages"],
                }
            ],
        }

        return result

except Exception as exceptErr:
    errAll({"e": e, "err": exceptErr, "txt": f"CÓDIGO INTEIRO\n{str(exceptErr)}"})
