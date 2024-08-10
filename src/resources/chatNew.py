# {
#     "action": "messageSend",
#     "model": "gpt-4o", // → OU SEM A CHAVE
#     "message": "Qual a idade de Saturno?"
# }

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

from chatHistoryJson import historyGet, historySet


def chatNew(inf):
    chatId = inf["chatId"]
    origin = inf["origin"]
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
        "origin": origin,
        "model": model,
        "chatId": chatId,
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
    chats.append(chatNewInf)
    retHistoryGet["chats"] = chats
    historySet(retHistoryGet)
