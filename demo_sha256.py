import hashlib, time
from argon2 import PasswordHasher

senha = b"SenhaForte123"
print("SHA-256 duas vezes:", hashlib.sha256(senha).hexdigest() == hashlib.sha256(senha).hexdigest())

t = time.perf_counter()
for _ in range(100_000):
    hashlib.sha256(senha).hexdigest()
print(f"SHA-256: 100.000 hashes em {time.perf_counter() - t:.3f} s")

t = time.perf_counter()
PasswordHasher(time_cost=3, memory_cost=65536, parallelism=4).hash("SenhaForte123")
print(f"Argon2id: 1 hash em {time.perf_counter() - t:.3f} s")