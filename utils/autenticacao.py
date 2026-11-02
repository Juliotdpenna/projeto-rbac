import os
from datetime import datetime, timedelta, timezone

import jwt
from dotenv import load_dotenv
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from database.repositorio import (
    consultar_permissoes,
    consultar_usuarios,
)

load_dotenv()  # Carrega as variáveis de ambiente do arquivo .env

ALGORITHM = "HS256"
TEMPO_EXPIRACAO_MINUTOS = 15

bearer_scheme = HTTPBearer(auto_error=False)

def obter_chave_secreta() -> str:
    chave = os.getenv("JWT_SECRET_KEY")

    if not chave:
        raise RuntimeError(
            "A variável de ambiente JWT_SECRET_KEY não foi configurada."
        )

    return chave

def criar_access_token(usuario_id: int) -> str:
    agora = datetime.now(timezone.utc)

    payload = {
        "sub": str(usuario_id),
        "iat": agora,
        "exp": agora + timedelta(minutes=TEMPO_EXPIRACAO_MINUTOS),
    }

    token = jwt.encode(
        payload,
        obter_chave_secreta(),
        algorithm=ALGORITHM,
    )

    return token

def decodificar_access_token(token: str) -> dict | None:
    try:
        payload = jwt.decode(
            token,
            obter_chave_secreta(),
            algorithms=[ALGORITHM],
            options={
                "require": ["sub", "iat", "exp"]
            },
        )

        return payload

    except jwt.InvalidTokenError:
        return None

def obter_usuario_atual(
    credenciais: HTTPAuthorizationCredentials = Depends(bearer_scheme),
):
    if credenciais is None:
        raise HTTPException(
            status_code=401,
            detail="Autenticação necessária.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    payload = decodificar_access_token(credenciais.credentials)

    if payload is None:
        raise HTTPException(
            status_code=401,
            detail="Token inválido ou expirado.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    usuario_id = payload.get("sub")

    if not usuario_id or not usuario_id.isdigit():
        raise HTTPException(
            status_code=401,
            detail="Token inválido.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    usuarios = consultar_usuarios()

    usuario = next(
        (u for u in usuarios if u.id == int(usuario_id)),
        None,
    )

    if usuario is None or not usuario.status:
        raise HTTPException(
            status_code=401,
            detail="Usuário inexistente ou desativado.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return usuario

def exigir_permissao(nome_permissao: str):
    def verificar_permissao(
        usuario=Depends(obter_usuario_atual)
    ):
        permissoes = consultar_permissoes()

        permissao = next(
            (
                p for p in permissoes
                if p.nome == nome_permissao
            ),
            None,
        )

        if permissao is None or not permissao.status:
            raise HTTPException(
                status_code=403,
                detail="Permissão inexistente ou desativada.",
            )

        if not usuario.pode_acessar(permissao):
            raise HTTPException(
                status_code=403,
                detail="Você não possui permissão para esta operação.",
            )

        return usuario

    return verificar_permissao