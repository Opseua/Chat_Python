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
    # BIBLIOTECAS: NATIVAS
    sys = infGlobal["sys"]
    time = infGlobal["time"]
    json = infGlobal["json"]
    threading = infGlobal["threading"]
    signal = infGlobal["signal"]
    datetime = infGlobal["datetime"]
    os = infGlobal["os"]

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
    msg = {
        "e": e,
        "txt": "RODANDO → CLIENTE G4F [frontEnd/backEnd]",
    }
    logConsole(msg)

    # ENVIAR MENSAGEM
    async def providerG4f(inf):
        model = inf["model"]
        messagePrompt = json.loads(inf["messagePrompt"])
        response = None
        try:
            msg = {
                "e": e,
                "txt": "OK providerG4f",
            }
            logConsole(msg)
            response = client.chat.completions.create(
                model=model, messages=messagePrompt
            )
        except Exception as exceptErr:
            errAll(
                {
                    "e": e,
                    "err": exceptErr,
                    "msg": "providerG4f: ERRO | ENVIAR MENSAGEM",
                }
            )

        if response:
            # RESPOSTA RECEBIDA
            response = response.choices[0].message.content
        else:
            # RESPOSTA NÃO RECEBIDA
            response = False

        return response

except Exception as exceptErr:
    errAll({"e": e, "err": exceptErr, "msg": f"CÓDIGO INTEIRO\n{str(exceptErr)}"})
