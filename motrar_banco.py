import sqlite3

con = sqlite3.connect("usuarios.db")
for id_, email, hash_ in con.execute("SELECT id, email, senha_hash FROM usuarios"):
    print(id_, email, hash_)