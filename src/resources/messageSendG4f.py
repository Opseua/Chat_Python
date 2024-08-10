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

# IMPORTAR 'export.py'
from export import infGlobal
from export import errAll

# BIBLIOTECAS: NATIVAS
import os

try:
    # BIBLIOTECAS: NATIVAS
    sys = infGlobal["sys"]
    time = infGlobal["time"]
    json = infGlobal["json"]
    threading = infGlobal["threading"]
    signal = infGlobal["signal"]

    # BIBLIOTECAS: NECESSÁRIO INSTALAR → pip install brotli mitmproxy
    from g4f.client import Client
    from g4f.gui import run_gui

    # VARIÁVEIS
    portG4fFrontEnd = infGlobal["portG4fFrontEnd"]

    # ------------------------------------------------------ G4F ------------------------------------------------------------
    # CLIENT
    client = Client()

    def run_gui_thread():
        run_gui(port=portG4fFrontEnd)

    # INICIAR
    gui_thread = threading.Thread(target=run_gui_thread, daemon=True)
    gui_thread.start()

    def stopCode(sig, frame):
        sys.exit(0)

    signal.signal(signal.SIGINT, stopCode)
    time.sleep(2)
    # LIMPAR CONSOLE
    os.system("cls")
    print("RODANDO → CLIENTE/GUI G4F")

    # ENVIAR MENSAGEM: G4F
    async def messageSendG4f(inf):
        model = inf["model"]
        messagePrompt = json.loads(inf["messagePrompt"])
        try:
            response = client.chat.completions.create(
                model=model, messages=messagePrompt
            )
        except Exception as e:
            print(str(e))

        if response:
            # RESPOSTA RECEBIDA
            response = response.choices[0].message.content
        else:
            # RESPOSTA NÃO RECEBIDA
            response = False

        return response

except Exception as exceptErr:
    errAll(exceptErr)
    print("CÓDIGO INTEIRO [messageSendG4f]")
    os._exit(1)

# {
#     "action": "historyChat",
#     "model": "*",
#     "includesInMessages": [
#         "role",
#         "content",
#         //"timestampCreate",
#         "x"
#     ]
# }

# {
#     "action": "historyMessages",
#     "chatId": "2024_08_03-19.17.50.609-DGW",
#     "includesInMessages": [
#         "role",
#          "content",
#         //"timestampCreate",
#         "x"
#     ]
# }

# {
#     "action": "messageSend",
#     "chatIdA": "2024_08_03-19.17.50.609-DGW",
#     "messagePrompt": "Qual a cor do céu?",
#     "messageFile": true,
#     "x": "x"
# }

# {
#     "action": "historyDelete",
#     "chatId": "2024_08_03-20.04.16.664-NQF",
#     "qtdDeleteMessages": 999,
#     "x": "x"
# }
