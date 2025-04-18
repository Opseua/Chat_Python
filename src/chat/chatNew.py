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
    errAll({"e": e, "err": exceptErr, "msg": f"CÓDIGO INTEIRO\n{str(exceptErr)}"})
