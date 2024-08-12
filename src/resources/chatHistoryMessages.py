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
# ERRO DE IMPORT 'datetime'
# pylint: disable=E1101

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
                    key: message[key] for key in includesInMessages if key in message
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
