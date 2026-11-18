import sqlite3
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError


ph = PasswordHasher(time_cost=3, memory_cost=65536, parallelism=4)
_HASH_FALSO = ph.hash("brasil")  


def conectar(caminho="usuarios.db"):
    con = sqlite3.connect(caminho)
    con.execute(
        """CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            senha_hash TEXT NOT NULL)"""
    )
    return con


def cadastrar(con, email, senha):
    email = email.strip().lower()
    if len(senha) < 8:
        raise ValueError("A senha deve ter pelo menos 8 caracteres")
    try:
        con.execute(
            "INSERT INTO usuarios (email, senha_hash) VALUES (?, ?)",
            (email, ph.hash(senha)),
        )
        con.commit()
    except sqlite3.IntegrityError:
        raise ValueError("E-mail já cadastrado")


def login(con, email, senha):
    email = email.strip().lower()
    linha = con.execute(
        "SELECT senha_hash FROM usuarios WHERE email = ?", (email,)
    ).fetchone()
    if linha is None:
        try:
            ph.verify(_HASH_FALSO, senha)
        except VerifyMismatchError:
            pass
        return False
    try:
        ph.verify(linha[0], senha)  # comparação segura feita pela biblioteca
    except VerifyMismatchError:
        return False
    if ph.check_needs_rehash(linha[0]):  # atualiza se os parâmetros mudarem
        con.execute(
            "UPDATE usuarios SET senha_hash = ? WHERE email = ?",
            (ph.hash(senha), email),
        )
        con.commit()
    return True