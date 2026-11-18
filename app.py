from getpass import getpass
from usuarios import conectar, cadastrar, login

con = conectar()
while True:
    print("\n1 - Cadastrar\n2 - Login\n0 - Sair")
    op = input("Escolha: ")
    if op == "0":
        break
    if op not in ("1", "2"):
        continue
    email = input("E-mail: ")
    senha = getpass("Senha (não aparece enquanto digita): ")
    if op == "1":
        try:
            cadastrar(con, email, senha)
            print("Cadastro realizado.")
        except ValueError as erro:
            print("Erro:", erro)
    else:
        print("Login OK" if login(con, email, senha) else "E-mail ou senha incorretos")