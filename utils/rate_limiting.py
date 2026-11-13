import time
from threading import Lock

LIMITE_TENTATIVAS = 5
JANELA_TEMPO = 60

tentativas_login = {}
lock = Lock()


def verificar_limite(ip: str) -> bool:
    agora = time.monotonic()

    with lock:
        # Remove tentativas antigas de todos os IPs.
        for endereco in list(tentativas_login):
            tentativas_login[endereco] = [
                tentativa
                for tentativa in tentativas_login[endereco]
                if agora - tentativa < JANELA_TEMPO
            ]

            if not tentativas_login[endereco]:
                del tentativas_login[endereco]

        tentativas = tentativas_login.get(ip, [])

        return len(tentativas) < LIMITE_TENTATIVAS


def registrar_tentativa_falha(ip: str):
    agora = time.monotonic()

    with lock:
        tentativas_login.setdefault(ip, []).append(agora)