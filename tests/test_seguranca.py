from utils.seguranca import gerar_hash_senha, verificar_senha

def test_gerar_hash_argon2id():
    senha = "SenhaTeste!123"

    hash_senha = gerar_hash_senha(senha)

    assert hash_senha.startswith("$argon2id$")


def test_verificar_senha_correta():
    senha = "SenhaTeste!123"

    hash_senha = gerar_hash_senha(senha)

    assert verificar_senha(senha, hash_senha) is True


def test_rejeitar_senha_incorreta():
    senha = "SenhaTeste!123"

    hash_senha = gerar_hash_senha(senha)

    assert verificar_senha("SenhaErrada", hash_senha) is False

import pytest


def test_rejeitar_senha_vazia():
    with pytest.raises(ValueError):
        gerar_hash_senha("")


def test_rejeitar_hash_invalido():
    assert verificar_senha("SenhaTeste!123", "hash_invalido") is False