# entrega-2-
# Entrega 2: Hash e autenticação segura

Projeto Integrador de Segurança da Informação (Unit, ADS).
Integrantes: Vinicius , Jose Ramon , Felisberto Freire
Docente: Profa. Ana Carla do Nascimento Santos

## Problema
Uma aplicação precisa cadastrar usuários sem armazenar senhas em texto puro

## Solução
Cadastro e login em Python usando **Argon2id** (biblioteca `argon2-cffi`) e banco
**SQLite**. O banco guarda apenas o hash da senha. A comparação no login é feita
pela própria biblioteca (`PasswordHasher.verify`).

## Arquivos
| Arquivo | Função |
|---|---|
| `usuarios.py` | Banco, cadastro (`cadastrar`) e login (`login`) |
| `app.py` | Programa de linha de comando com menu de cadastro e login |
| `test_usuarios.py` | Testes automatizados (pytest) |
| `mostrar_banco.py` | Mostra o que está gravado no banco (evidência) |
| `demo_sha256.py` | Compara a velocidade do SHA-256 com a do Argon2id |
## Por que SHA-256 isolado não é adequado para senhas
-  Foi feito para calcular hashes de dados com
  eficiência. Hardware de ataque (GPUs) testa bilhões de hashes por segundo, e
  isso torna a adivinhação de senhas barata.
- Sem salt, a mesma senha gera sempre o mesmo hash. Isso permite tabelas
  pré-calculadas (rainbow tables) e revela quem usa a mesma senha.
- Não tem custo ajustável. Não há como deixá-lo mais lento conforme o
  hardware evolui.
- Argon2idé lento e consome memória de forma configurável, o que encarece
  cada tentativa do atacante, e já traz salt e parâmetros no formato do hash.

O script `demo_sha256.py` mede essa diferença de tempo.
|