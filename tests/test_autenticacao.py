import pytest

from utils.autenticacao import (
    criar_access_token,
    decodificar_access_token,
)


def test_gerar_token():
    token = criar_access_token(1)

    assert isinstance(token, str)
    assert len(token) > 0


def test_validar_token():
    token = criar_access_token(1)

    payload = decodificar_access_token(token)

    assert payload is not None
    assert payload["sub"] == "1"
    assert "exp" in payload
    assert "iat" in payload


def test_rejeitar_token_invalido():
    payload = decodificar_access_token("token.invalido")

    assert payload is None
