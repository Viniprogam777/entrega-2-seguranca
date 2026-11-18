import pytest
from usuarios import conectar, cadastrar, login

SENHA = "brasileirao"


@pytest.fixture
def con():
    return conectar(":memory:")


def test_login_correto(con):
    cadastrar(con, "ana@email.com", SENHA)
    assert login(con, "ana@email.com", SENHA) is True


def test_login_senha_incorreta(con):
    cadastrar(con, "ana@email.com", SENHA)
    assert login(con, "ana@email.com", "ramon") is False


def test_usuario_inexistente(con):
    assert login(con, "ninguem@email.com", SENHA) is False


def test_senha_nao_fica_em_texto_puro(con):
    cadastrar(con, "ana@email.com", SENHA)
    salvo = con.execute("SELECT senha_hash FROM usuarios").fetchone()[0]
    assert SENHA not in salvo
    assert salvo.startswith("$argon2id$")


def test_mesma_senha_gera_hashes_diferentes(con):
    cadastrar(con, "a@email.com", SENHA)
    cadastrar(con, "b@email.com", SENHA)
    hashes = [l[0] for l in con.execute("SELECT senha_hash FROM usuarios")]
    assert hashes[0] != hashes[1]  


def test_email_duplicado(con):
    cadastrar(con, "ana@email.com", SENHA)
    with pytest.raises(ValueError):
        cadastrar(con, "ana@email.com", SENHA)


def test_senha_curta(con):
    with pytest.raises(ValueError):
        cadastrar(con, "ana@email.com", "123")