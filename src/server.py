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

# BIBLIOTECAS: NATIVAS
import os, sys, builtins

# LIMPAR CONSOLE (MANTER NO INÍCIO) | IGNORAR ERROS DO CTRL + C
os.system("cls")
sys.stderr = open(os.devnull, "w")

# PATH DO PROJETO
project = "Chat_Python"
projectPath = os.path.abspath(__file__).split(project)[0] + project
builtins.projectPath = projectPath.replace("\\", "/")

# PATHS DE ARQUIVOS '.py'
sys.path.append(f"{projectPath}/src/chat")
sys.path.append(f"{projectPath}/src/providers")
sys.path.append(f"{projectPath}/src/resources")
from export import errAll

try:
    # BIBLIOTECAS: NATIVAS
    asyncio = infGlobal["asyncio"]
    aiohttp_cors = infGlobal["aiohttp_cors"]

    # BIBLIOTECAS: NECESSÁRIO INSTALAR → pip install asyncio aiohttp_cors aiohttp httpx -U g4f[all] telethon openai
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
        logConsole(
            {"e": e, "txt": f"RODANDO → SERVIDOR HTTP NA PORTA: {portServerHttp}"}
        )
        # MANTER EM EXECUÇÃO
        while True:
            await asyncio.sleep(3600)

    # INICIAR ARQUIVO E SERVIDOR
    if __name__ == "__main__":
        loop = asyncio.get_event_loop()
        loop.run_until_complete(serverRun())

except Exception as exceptErr:
    errAll({"e": e, "err": exceptErr, "txt": f"CÓDIGO INTEIRO\n{str(exceptErr)}"})


#           ---------------- NagaAI* ----------------
# *** GPT ***
# SIM - 03/min | 100/day → gpt-4o-mini
# SIM - 03/min | 200/day → gpt-3.5-turbo

# *** GEMINI ***
# SIM - 02/min | 025/day → gemini-2.0-flash-thinking-exp
# SIM - 02/min | 025/day → gemini-2.0-flash-exp
# SIM - 02/min | 025/day → gemini-exp
# SIM - 02/min | 025/day → gemini-1.5-pro
# SIM - 02/min | 025/day → gemini-1.5-flash

# *** LLAMA ***
# 03/min | 100/day → LLAMA-3.3-70B-INSTRUCT
# 03/min | 100/day → LLAMA-3.2-90B-VISION-INSTRUCT
# 03/min | 100/day → LLAMA-3.2-11B-VISION-INSTRUCT
# 03/min | 100/day → LLAMA-3.2-3B-INSTRUCT
# 03/min | 100/day → LLAMA-3.2-1B-INSTRUCT
# 03/min | 100/day → LLAMA-3.1-405B-INSTRUCT
# 03/min | 100/day → LLAMA-3.1-70B-INSTRUCT
# 03/min | 100/day → LLAMA-3-70B-INSTRUCT
# 03/min | 200/day → LLAMA-3.1-8B-INSTRUCT
# 03/min | 200/day → LLAMA-3-8B-INSTRUCT

# *** CLAUDE ***
# SIM - 02/min | 050/day → CLAUDE-3-HAIKU-20240307

# *** MIXTRAL ***
# 03/min | 200/day → MIXTRAL-8X7B-INSTRUCT
# 03/min | 100/day → MIXTRAL-8X22B-INSTRUCT

# ** DEEPSEEK ***
# NAO - 03/min | 100/day → DEEPSEEK-REASONER
# NAO - 03/min | 100/day → DEEPSEEK-CHAT
