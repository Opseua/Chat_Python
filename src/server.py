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

import sys, os, locale

# LIMPAR CONSOLE (MANTER NO INÍCIO)
os.system("cls")

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "resources")))
# IMPORTAR 'export.py'
from export import infGlobal
from export import errAll

# IGNORAR ERROS DO CTRL + C
sys.stderr = open(os.devnull, "w")

# FORMATAR DATA E HORA NO PADRÃO BRASILEIRO
locale.setlocale(locale.LC_TIME, "pt_BR")

try:
    # BIBLIOTECAS: NATIVAS
    asyncio = infGlobal["asyncio"]
    aiohttp_cors = infGlobal["aiohttp_cors"]

    # BIBLIOTECAS: NECESSÁRIO INSTALAR → pip install brotli mitmproxy
    web = infGlobal["web"]

    # VARIÁVEIS
    portServerHttp = infGlobal["portServerHttp"]

    # FUNÇÕES DE ARQUIVOS
    from httpRequest import httpRequest

    # SERVER HTTP
    async def serverRun():
        app = web.Application()
        app.router.add_post("/chat", httpRequest)
        cors = aiohttp_cors.setup(
            app,
            defaults={
                "*": aiohttp_cors.ResourceOptions(
                    allow_credentials=True,
                    expose_headers="*",
                    allow_headers="*",
                    allow_methods="*",
                )
            },
        )
        for route in list(app.router.routes()):
            cors.add(route)
        runner = web.AppRunner(app)
        await runner.setup()
        site = web.TCPSite(runner, port=portServerHttp)
        await site.start()
        print(f"RODANDO → SERVIDOR HTTP NA PORTA: {portServerHttp}")
        # MANTER EM EXECUÇÃO
        while True:
            await asyncio.sleep(3600)

    # INICIAR ARQUIVO E SERVIDOR
    if __name__ == "__main__":
        loop = asyncio.get_event_loop()
        loop.run_until_complete(serverRun())

except Exception as exceptErr:
    errAll(exceptErr)
    print("CÓDIGO INTEIRO [server]", exceptErr)
    os._exit(1)


# 8890 SERVER HTTP
# 8892 GF4 FRONT-END
