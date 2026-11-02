import sqlite3
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
CAMINHO_BANCO = BASE_DIR / "rbac.db"


def conectar(caminho_banco=None):
    caminho = caminho_banco or CAMINHO_BANCO

    conexao = sqlite3.connect(caminho)
    conexao.execute("PRAGMA foreign_keys = ON")

    return conexao
