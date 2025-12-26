# ARQUIVO ATUAL
e = __file__

try:
    # BIBLIOTECAS: NATIVAS
    json = infGlobal["json"]
    os = infGlobal["os"]

    pathChats = "logs/chats.json"

    def historyGet():
        if not os.path.exists(pathChats):
            historySet({"chats": []})
            return {"chats": []}
        with open(pathChats, "r", encoding="utf-8") as file:
            return json.load(file)

    def historySet(inf):
        # SALVAR NO ARQUIVO
        with open(pathChats, "w", encoding="utf-8") as file:
            json.dump(inf, file, ensure_ascii=False, indent=4)

except Exception as exceptErr:
    errAll({"e": e, "err": exceptErr, "txt": f"CÓDIGO INTEIRO\n{str(exceptErr)}"})
