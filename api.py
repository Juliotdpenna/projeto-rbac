import sqlite3

from fastapi import FastAPI, HTTPException, Depends, Request
from pydantic import BaseModel, Field, field_validator
from fastapi.middleware.cors import CORSMiddleware
from utils.rate_limiting import verificar_limite, registrar_tentativa_falha
from utils.logs import logger

from utils.seguranca import (
    verificar_senha,
    gerar_hash_senha,
)
from utils.autenticacao import (
    criar_access_token,
    TEMPO_EXPIRACAO_MINUTOS,
    obter_usuario_atual,
    exigir_permissao,
)
from database.repositorio import (
    atualizar_usuario,
    cadastrar_usuario,
    consultar_usuarios,
    desativar_usuario,
    reativar_usuario,
    cadastrar_role,
    consultar_roles,
    cadastrar_permissao,
    consultar_permissoes,
    associar_permissao_role,
    cadastrar_grupo,
    consultar_grupos,
    associar_usuario_grupo,
    associar_role_grupo,
    consultar_usuario_login,
    desativar_permissao,
    atualizar_role,
    desativar_role,
    reativar_role,
    desassociar_permissao_role,
    atualizar_permissao,
    reativar_permissao,
    atualizar_grupo,
    desativar_grupo,
    reativar_grupo,
    desassociar_usuario_grupo,
    desassociar_role_grupo,
)
from models.usuario import Usuario
from models.role import Role
from models.permissao import Permissao
from models.grupo import Grupo

app = FastAPI(
    title="Plataforma RBAC",
    description="API de gerenciamento de controle de acesso baseado em funções",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class UsuarioCriacao(BaseModel):
    nome: str
    matricula: str
    departamento: str
    cargo: str
    senha: str = Field(min_length=12, max_length=128)

    @field_validator("nome", "matricula", "departamento", "cargo")
    @classmethod
    def validar_campos_obrigatorios(cls, valor):
        valor = valor.strip()

        if not valor:
            raise ValueError("Este campo não pode ficar vazio.")

        return valor

class UsuarioAtualizacao(BaseModel):
    nome: str
    matricula: str
    departamento: str
    cargo: str

    @field_validator("nome", "matricula", "departamento", "cargo")
    @classmethod
    def validar_campos_obrigatorios(cls, valor):
        valor = valor.strip()

        if not valor:
            raise ValueError("Este campo não pode ficar vazio.")

        return valor

class RoleEntrada(BaseModel):
    nome: str
    descricao: str

    @field_validator("nome", "descricao")
    @classmethod
    def validar_campos_obrigatorios(cls, valor):
        valor = valor.strip()

        if not valor:
            raise ValueError("Este campo não pode ficar vazio.")

        return valor

class RoleAtualizacao(BaseModel):
    nome: str
    descricao: str

    @field_validator("nome", "descricao")
    @classmethod
    def validar_campos_obrigatorios(cls, valor):
        valor = valor.strip()

        if not valor:
            raise ValueError("Este campo não pode ficar vazio.")

        return valor

class PermissaoEntrada(BaseModel):
    nome: str
    descricao: str
    status: bool

    @field_validator("nome", "descricao")
    @classmethod
    def validar_campos_obrigatorios(cls, valor):
        valor = valor.strip()

        if not valor:
            raise ValueError("Este campo não pode ficar vazio.")

        return valor

class PermissaoAtualizacao(BaseModel):
    nome: str
    descricao: str

    @field_validator("nome", "descricao")
    @classmethod
    def validar_campos_obrigatorios(cls, valor):
        valor = valor.strip()

        if not valor:
            raise ValueError("Este campo não pode ficar vazio.")

        return valor

class LoginEntrada(BaseModel):
    matricula: str = Field(min_length=1)
    senha: str = Field(min_length=1)

    @field_validator("matricula")
    @classmethod
    def validar_matricula(cls, valor):
        valor = valor.strip()

        if not valor:
            raise ValueError("A matrícula não pode ficar vazia.")

        return valor

class GrupoEntrada(BaseModel):
    nome: str = Field(min_length=1)
    descricao: str = Field(min_length=1)
    status: bool

    @field_validator("nome", "descricao")
    @classmethod
    def validar_campos_obrigatorios(cls, valor):
        valor = valor.strip()

        if not valor:
            raise ValueError("Este campo não pode ficar vazio.")

        return valor

class GrupoAtualizacao(BaseModel):
    nome: str
    descricao: str

    @field_validator("nome", "descricao")
    @classmethod
    def validar_campos_obrigatorios(cls, valor):
        valor = valor.strip()

        if not valor:
            raise ValueError("Este campo não pode ficar vazio.")

        return valor

@app.get("/")
def inicio():
    return {"mensagem": "API RBAC funcionando"}


@app.get("/usuarios")
def listar_usuarios(
    usuario_autenticado=Depends(exigir_permissao("VISUALIZAR_USUARIOS"))
):
    try:
        usuarios = consultar_usuarios()

        return [
            {
                "id": usuario.id,
                "nome": usuario.nome,
                "matricula": usuario.matricula,
                "departamento": usuario.departamento,
                "cargo": usuario.cargo,
                "status": usuario.status,
                "roles": [
                    {
                        "id": role.id,
                        "nome": role.nome,
                    }
                    for role in usuario.roles_diretas
                ],
            }
            for usuario in usuarios
        ]

    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Erro interno ao consultar usuários.",
    )

@app.get("/usuarios/{usuario_id}")
def consultar_usuario_por_id(
    usuario_id: int,
    usuario_autenticado=Depends(exigir_permissao("VISUALIZAR_USUARIOS"))
):
    usuarios = consultar_usuarios()

    for usuario in usuarios:
        if usuario.id == usuario_id:
            return {
                "id": usuario.id,
                "nome": usuario.nome,
                "matricula": usuario.matricula,
                "departamento": usuario.departamento,
                "cargo": usuario.cargo,
                "status": usuario.status,
                "roles": [
                    {
                        "id": role.id,
                        "nome": role.nome,
                    }
                    for role in usuario.roles_diretas
                ],
            }

    raise HTTPException(
        status_code=404,
        detail="Usuário não encontrado.",
    )

@app.post("/usuarios", status_code=201)
def criar_usuario(
    dados: UsuarioCriacao,
    usuario_autenticado=Depends(exigir_permissao("CADASTRAR_USUARIOS"))
):
    usuario = Usuario(
        None,  # ID será gerado automaticamente pelo banco de dados
        dados.nome,
        dados.matricula,
        dados.departamento,
        dados.cargo,
        True,
        None,
    )

    usuario.senha_hash = gerar_hash_senha(dados.senha)

    try:
        cadastrar_usuario(usuario)
        logger.info(
            "USUARIO_CRIADO | Admin_ID=%s | Usuario_ID=%s",
            usuario_autenticado.id,
            usuario.id
        )

    except sqlite3.IntegrityError:
        raise HTTPException(
            status_code=409,
            detail="Matrícula já cadastrada.",
        )

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Erro interno ao cadastrar usuário.",
        )

    return {
        "mensagem": "Usuário cadastrado com sucesso.",
        "id": usuario.id,
    }

@app.put("/usuarios/{usuario_id}")
def atualizar_usuario_api(
    usuario_id: int,
    dados: UsuarioAtualizacao,
    usuario_autenticado=Depends(exigir_permissao("EDITAR_USUARIOS"))
):
    usuario_existente = next(
        (u for u in consultar_usuarios() if u.id == usuario_id),
        None,
    )

    if usuario_existente is None:
        raise HTTPException(
            status_code=404,
            detail="Usuário não encontrado.",
        )

    usuario_existente.nome = dados.nome
    usuario_existente.matricula = dados.matricula
    usuario_existente.departamento = dados.departamento
    usuario_existente.cargo = dados.cargo

    try:
        atualizar_usuario(usuario_existente)
        logger.info(
            "USUARIO_ATUALIZADO | Admin_ID=%s | Usuario_ID=%s",
            usuario_autenticado.id,
            usuario_existente.id
        )

    except sqlite3.IntegrityError:
        raise HTTPException(
            status_code=409,
            detail="A matrícula informada já está cadastrada.",
        )

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Erro interno ao atualizar usuário.",
        )

    return {
        "mensagem": "Usuário atualizado com sucesso.",
        "id": usuario_existente.id,
    }

@app.delete("/usuarios/{usuario_id}")
def excluir_usuario(
    usuario_id: int,
    usuario_autenticado=Depends(exigir_permissao("DESATIVAR_USUARIOS"))
):
    try:
        desativar_usuario(usuario_id)
        logger.info(
            "USUARIO_DESATIVADO | Admin_ID=%s | Usuario_ID=%s",
            usuario_autenticado.id,
            usuario_id
        )
    except ValueError:
        raise HTTPException(
            status_code=404,
            detail="Usuário não encontrado ou já desativado.",
        )
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Erro interno ao desativar usuário.",
        )

    return {
        "mensagem": "Usuário desativado com sucesso.",
        "id": usuario_id,
    }

@app.patch("/usuarios/{usuario_id}/reativar")
def reativar_usuario_api(
    usuario_id: int,
    usuario_autenticado=Depends(exigir_permissao("DESATIVAR_USUARIOS"))
):
    try:
        reativar_usuario(usuario_id)
        logger.info(
            "USUARIO_REATIVADO | Admin_ID=%s | Usuario_ID=%s",
            usuario_autenticado.id,
            usuario_id
        )
    except ValueError:
        raise HTTPException(
            status_code=404,
            detail="Usuário não encontrado ou já ativo.",
        )
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Erro interno ao reativar usuário.",
        )

    return {
        "mensagem": "Usuário reativado com sucesso.",
        "id": usuario_id,
    }

@app.get("/roles")
def listar_roles(
    usuario_autenticado=Depends(exigir_permissao("VISUALIZAR_ROLES"))
):
    roles = consultar_roles()

    return [
        {
            "id": role.id,
            "nome": role.nome,
            "descricao": role.descricao,
            "status": role.status,
            "permissoes": [
                {
                    "id": permissao.id,
                    "nome": permissao.nome,
                }
                for permissao in role.permissoes
            ],
        }
        for role in roles
    ]

@app.post("/roles", status_code=201)
def criar_role(
    dados: RoleEntrada,
    usuario_autenticado=Depends(exigir_permissao("GERENCIAR_ROLES"))
):
    role = Role(
        None,  # ID será gerado automaticamente pelo banco de dados
        dados.nome,
        dados.descricao,
        True,  # Nova role começa ativa
    )

    try:
        cadastrar_role(role)
        logger.info(
            "ROLE_CRIADA | Admin_ID=%s | Role_ID=%s",
            usuario_autenticado.id,
            role.id
        )
    except sqlite3.IntegrityError:
        raise HTTPException(
            status_code=409,
            detail="ID ou nome da Role já cadastrado, ou dados inválidos.",
        )
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Erro interno ao cadastrar Role.",
        )

    return {
        "mensagem": "Role cadastrada com sucesso.",
        "id": role.id,
    }


@app.get("/permissoes")
def listar_permissoes(
    usuario_autenticado=Depends(exigir_permissao("VISUALIZAR_PERMISSOES"))
):
    permissoes = consultar_permissoes()

    return [
        {
            "id": permissao.id,
            "nome": permissao.nome,
            "descricao": permissao.descricao,
            "status": permissao.status,
        }
        for permissao in permissoes
    ]

@app.post("/permissoes", status_code=201)
def criar_permissao(
    dados: PermissaoEntrada,
    usuario_autenticado=Depends(exigir_permissao("GERENCIAR_PERMISSOES"))
):
    permissao = Permissao(
        None,  # ID será gerado automaticamente pelo banco de dados
        dados.nome,
        dados.descricao,
        dados.status,
    )

    try:
        cadastrar_permissao(permissao)
        logger.info(
            "PERMISSAO_CRIADA | Admin_ID=%s | Permissao_ID=%s",
            usuario_autenticado.id,
            permissao.id
        )
    except sqlite3.IntegrityError:
        raise HTTPException(
            status_code=409,
            detail="ID ou nome da permissão já cadastrado, ou dados inválidos.",
        )
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Erro interno ao cadastrar permissão.",
        )

    return {
        "mensagem": "Permissão cadastrada com sucesso.",
        "id": permissao.id,
    }

@app.delete("/permissoes/{permissao_id}")
def excluir_permissao(
    permissao_id: int,
    usuario_autenticado=Depends(
        exigir_permissao("GERENCIAR_PERMISSOES")
    )
):
    try:
        desativar_permissao(permissao_id)
        logger.info(
            "PERMISSAO_DESATIVADA | Admin_ID=%s | Permissao_ID=%s",
            usuario_autenticado.id,
            permissao_id
        )

    except ValueError:
        raise HTTPException(
            status_code=404,
            detail="Permissão não encontrada ou já desativada.",
        )

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Erro interno ao desativar permissão.",
        )

    return {
        "mensagem": "Permissão desativada com sucesso.",
        "id": permissao_id,
    }

@app.put("/permissoes/{permissao_id}")
def atualizar_permissao_api(
    permissao_id: int,
    dados: PermissaoAtualizacao,
    usuario_autenticado=Depends(
        exigir_permissao("GERENCIAR_PERMISSOES")
    )
):
    permissao_existente = next(
        (p for p in consultar_permissoes() if p.id == permissao_id),
        None,
    )

    if permissao_existente is None:
        raise HTTPException(
            status_code=404,
            detail="Permissão não encontrada.",
        )

    permissao_existente.nome = dados.nome
    permissao_existente.descricao = dados.descricao

    try:
        atualizar_permissao(permissao_existente)
        logger.info(
            "PERMISSAO_ATUALIZADA | Admin_ID=%s | Permissao_ID=%s",
            usuario_autenticado.id,
            permissao_id
        )

    except sqlite3.IntegrityError:
        raise HTTPException(
            status_code=409,
            detail="Já existe uma permissão com o nome informado.",
        )

    except ValueError:
        raise HTTPException(
            status_code=404,
            detail="Permissão não encontrada.",
        )

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Erro interno ao atualizar permissão.",
        )

    return {
        "mensagem": "Permissão atualizada com sucesso.",
        "id": permissao_id,
    }

@app.patch("/permissoes/{permissao_id}/reativar")
def reativar_permissao_api(
    permissao_id: int,
    usuario_autenticado=Depends(
        exigir_permissao("GERENCIAR_PERMISSOES")
    )
):
    try:
        reativar_permissao(permissao_id)
        logger.info(
            "PERMISSAO_REATIVADA | Admin_ID=%s | Permissao_ID=%s",
            usuario_autenticado.id,
            permissao_id
        )

    except ValueError:
        raise HTTPException(
            status_code=404,
            detail="Permissão não encontrada ou já ativa.",
        )

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Erro interno ao reativar permissão.",
        )

    return {
        "mensagem": "Permissão reativada com sucesso.",
        "id": permissao_id,
    }

@app.post("/roles/{role_id}/permissoes/{permissao_id}")
def associar_permissao_a_role(
    role_id: int,
    permissao_id: int,
    usuario_autenticado=Depends(exigir_permissao("GERENCIAR_ROLES"))
):

    try:
        associar_permissao_role(role_id, permissao_id)
        logger.info(
            "PERMISSAO_ASSOCIADA_ROLE | Admin_ID=%s | Role_ID=%s | Permissao_ID=%s",
            usuario_autenticado.id,
            role_id,
            permissao_id
        )
    except sqlite3.IntegrityError:
        raise HTTPException(
            status_code=409,
            detail="Associação já existente ou dados inválidos.",
        )
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Erro interno ao associar permissão à Role.",
        )

    return {
        "mensagem": "Permissão associada à Role com sucesso.",
        "role_id": role_id,
        "permissao_id": permissao_id,
    }

@app.get("/roles/{role_id}/permissoes")
def listar_permissoes_da_role(
    role_id: int,
    usuario_autenticado=Depends(exigir_permissao("VISUALIZAR_ROLES"))
):
    roles = consultar_roles()

    role = next(
        (r for r in roles if r.id == role_id),
        None,
    )

    if role is None:
        raise HTTPException(
            status_code=404,
            detail="Role não encontrada.",
        )

    return [
        {
            "id": permissao.id,
            "nome": permissao.nome,
            "descricao": permissao.descricao,
            "status": permissao.status,
        }
        for permissao in role.permissoes
    ]


@app.put("/roles/{role_id}")
def atualizar_role_api(
    role_id: int,
    dados: RoleAtualizacao,
    usuario_autenticado=Depends(exigir_permissao("GERENCIAR_ROLES"))
):
    role_existente = next(
        (r for r in consultar_roles() if r.id == role_id),
        None,
    )

    if role_existente is None:
        raise HTTPException(
            status_code=404,
            detail="Role não encontrada.",
        )

    role_existente.nome = dados.nome
    role_existente.descricao = dados.descricao

    try:
        atualizar_role(role_existente)
        logger.info(
            "ROLE_ATUALIZADA | Admin_ID=%s | Role_ID=%s",
            usuario_autenticado.id,
            role_id
        )

    except sqlite3.IntegrityError:
        raise HTTPException(
            status_code=409,
            detail="Já existe uma Role com os dados informados.",
        )

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Erro interno ao atualizar Role.",
        )

    return {
        "mensagem": "Role atualizada com sucesso.",
        "id": role_id,
    }


@app.delete("/roles/{role_id}")
def desativar_role_api(
    role_id: int,
    usuario_autenticado=Depends(exigir_permissao("GERENCIAR_ROLES"))
):
    try:
        desativar_role(role_id)
        logger.info(
            "ROLE_DESATIVADA | Admin_ID=%s | Role_ID=%s",
            usuario_autenticado.id,
            role_id
        )

    except ValueError:
        raise HTTPException(
            status_code=404,
            detail="Role não encontrada ou já desativada.",
        )

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Erro interno ao desativar Role.",
        )

    return {
        "mensagem": "Role desativada com sucesso.",
        "id": role_id,
    }


@app.patch("/roles/{role_id}/reativar")
def reativar_role_api(
    role_id: int,
    usuario_autenticado=Depends(exigir_permissao("GERENCIAR_ROLES"))
):
    try:
        reativar_role(role_id)
        logger.info(
            "ROLE_REATIVADA | Admin_ID=%s | Role_ID=%s",
            usuario_autenticado.id,
            role_id
        )

    except ValueError:
        raise HTTPException(
            status_code=404,
            detail="Role não encontrada ou já ativa.",
        )

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Erro interno ao reativar Role.",
        )

    return {
        "mensagem": "Role reativada com sucesso.",
        "id": role_id,
    }


@app.delete("/roles/{role_id}/permissoes/{permissao_id}")
def remover_permissao_da_role(
    role_id: int,
    permissao_id: int,
    usuario_autenticado=Depends(exigir_permissao("GERENCIAR_ROLES"))
):
    try:
        desassociar_permissao_role(role_id, permissao_id)
        logger.info(
            "PERMISSAO_REMOVIDA_ROLE | Admin_ID=%s | Role_ID=%s | Permissao_ID=%s",
            usuario_autenticado.id,
            role_id,
            permissao_id
        )

    except ValueError:
        raise HTTPException(
            status_code=404,
            detail="Associação entre Role e permissão não encontrada.",
        )

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Erro interno ao remover permissão da Role.",
        )

    return {
        "mensagem": "Permissão removida da Role com sucesso.",
        "role_id": role_id,
        "permissao_id": permissao_id,
    }

@app.get("/grupos")
def listar_grupos(
    usuario_autenticado=Depends(exigir_permissao("VISUALIZAR_GRUPOS"))
):
    try:
        grupos = consultar_grupos()

        return [
            {
                "id": grupo.id,
                "nome": grupo.nome,
                "descricao": grupo.descricao,
                "status": grupo.status,
                "usuarios": [
                    {
                        "id": usuario.id,
                        "nome": usuario.nome,
                    }
                    for usuario in grupo.usuarios
                ],
                "roles": [
                    {
                        "id": role.id,
                        "nome": role.nome,
                    }
                    for role in grupo.roles
                ],
            }
            for grupo in grupos
        ]

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Erro interno ao consultar grupos.",
        )


@app.post("/grupos", status_code=201)
def criar_grupo(
    dados: GrupoEntrada,
    usuario_autenticado=Depends(exigir_permissao("GERENCIAR_GRUPOS"))
):
    grupo = Grupo(
        None,  # ID será gerado automaticamente pelo banco de dados
        dados.nome,
        dados.descricao,
        dados.status,
    )

    try:
        cadastrar_grupo(grupo)
        logger.info(
            "GRUPO_CRIADO | Admin_ID=%s | Grupo_ID=%s",
            usuario_autenticado.id,
            grupo.id
        )

    except sqlite3.IntegrityError:
        raise HTTPException(
            status_code=409,
            detail="ID ou nome do grupo já cadastrado, ou dados inválidos.",
        )

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Erro interno ao cadastrar grupo.",
        )

    return {
        "mensagem": "Grupo cadastrado com sucesso.",
        "id": grupo.id,
    }

@app.get("/grupos/{grupo_id}")
def consultar_grupo_por_id(
    grupo_id: int,
    usuario_autenticado=Depends(exigir_permissao("VISUALIZAR_GRUPOS"))
):
    grupos = consultar_grupos()

    grupo = next(
        (g for g in grupos if g.id == grupo_id),
        None,
    )

    if grupo is None:
        raise HTTPException(
            status_code=404,
            detail="Grupo não encontrado.",
        )

    return {
        "id": grupo.id,
        "nome": grupo.nome,
        "descricao": grupo.descricao,
        "status": grupo.status,
        "usuarios": [
            {"id": usuario.id, "nome": usuario.nome}
            for usuario in grupo.usuarios
        ],
        "roles": [
            {"id": role.id, "nome": role.nome}
            for role in grupo.roles
        ],
    }


@app.put("/grupos/{grupo_id}")
def atualizar_grupo_api(
    grupo_id: int,
    dados: GrupoAtualizacao,
    usuario_autenticado=Depends(
        exigir_permissao("GERENCIAR_GRUPOS")
    )
):
    grupo_existente = next(
        (g for g in consultar_grupos() if g.id == grupo_id),
        None,
    )

    if grupo_existente is None:
        raise HTTPException(
            status_code=404,
            detail="Grupo não encontrado.",
        )

    grupo_existente.nome = dados.nome
    grupo_existente.descricao = dados.descricao

    try:
        atualizar_grupo(grupo_existente)
        logger.info(
            "GRUPO_ATUALIZADO | Admin_ID=%s | Grupo_ID=%s",
            usuario_autenticado.id,
            grupo_id
        )

    except sqlite3.IntegrityError:
        raise HTTPException(
            status_code=409,
            detail="Já existe um grupo com o nome informado.",
        )

    except ValueError:
        raise HTTPException(
            status_code=404,
            detail="Grupo não encontrado.",
        )

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Erro interno ao atualizar grupo.",
        )

    return {
        "mensagem": "Grupo atualizado com sucesso.",
        "id": grupo_id,
    }


@app.delete("/grupos/{grupo_id}")
def desativar_grupo_api(
    grupo_id: int,
    usuario_autenticado=Depends(
        exigir_permissao("GERENCIAR_GRUPOS")
    )
):
    try:
        desativar_grupo(grupo_id)
        logger.info(
            "GRUPO_DESATIVADO | Admin_ID=%s | Grupo_ID=%s",
            usuario_autenticado.id,
            grupo_id
        )

    except ValueError:
        raise HTTPException(
            status_code=404,
            detail="Grupo não encontrado ou já desativado.",
        )

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Erro interno ao desativar grupo.",
        )

    return {
        "mensagem": "Grupo desativado com sucesso.",
        "id": grupo_id,
    }


@app.patch("/grupos/{grupo_id}/reativar")
def reativar_grupo_api(
    grupo_id: int,
    usuario_autenticado=Depends(
        exigir_permissao("GERENCIAR_GRUPOS")
    )
):
    try:
        reativar_grupo(grupo_id)
        logger.info(
            "GRUPO_REATIVADO | Admin_ID=%s | Grupo_ID=%s",
            usuario_autenticado.id,
            grupo_id
        )

    except ValueError:
        raise HTTPException(
            status_code=404,
            detail="Grupo não encontrado ou já ativo.",
        )

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Erro interno ao reativar grupo.",
        )

    return {
        "mensagem": "Grupo reativado com sucesso.",
        "id": grupo_id,
    }


@app.delete("/grupos/{grupo_id}/usuarios/{usuario_id}")
def remover_usuario_do_grupo(
    grupo_id: int,
    usuario_id: int,
    usuario_autenticado=Depends(
        exigir_permissao("GERENCIAR_GRUPOS")
    )
):
    try:
        desassociar_usuario_grupo(grupo_id, usuario_id)
        logger.info(
            "USUARIO_REMOVIDO_GRUPO | Admin_ID=%s | Grupo_ID=%s | Usuario_ID=%s",
            usuario_autenticado.id,
            grupo_id,
            usuario_id
        )

    except ValueError:
        raise HTTPException(
            status_code=404,
            detail="Associação entre grupo e usuário não encontrada.",
        )

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Erro interno ao remover usuário do grupo.",
        )

    return {
        "mensagem": "Usuário removido do grupo com sucesso.",
        "grupo_id": grupo_id,
        "usuario_id": usuario_id,
    }


@app.delete("/grupos/{grupo_id}/roles/{role_id}")
def remover_role_do_grupo(
    grupo_id: int,
    role_id: int,
    usuario_autenticado=Depends(
        exigir_permissao("GERENCIAR_GRUPOS")
    )
):
    try:
        desassociar_role_grupo(grupo_id, role_id)
        logger.info(
            "ROLE_REMOVIDA_GRUPO | Admin_ID=%s | Grupo_ID=%s | Role_ID=%s",
            usuario_autenticado.id,
            grupo_id,
            role_id
        )

    except ValueError:
        raise HTTPException(
            status_code=404,
            detail="Associação entre grupo e Role não encontrada.",
        )

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Erro interno ao remover Role do grupo.",
        )

    return {
        "mensagem": "Role removida do grupo com sucesso.",
        "grupo_id": grupo_id,
        "role_id": role_id,
    }


@app.post("/grupos/{grupo_id}/usuarios/{usuario_id}")
def adicionar_usuario_ao_grupo(
    grupo_id: int,
    usuario_id: int,
    usuario_autenticado=Depends(exigir_permissao("GERENCIAR_GRUPOS"))
):
    grupos = consultar_grupos()
    usuarios = consultar_usuarios()

    grupo = next((g for g in grupos if g.id == grupo_id), None)
    usuario_alvo = next((u for u in usuarios if u.id == usuario_id), None)

    if grupo is None:
        raise HTTPException(status_code=404, detail="Grupo não encontrado.")

    if usuario_alvo is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")

    if not grupo.status:
        raise HTTPException(status_code=409, detail="Grupo desativado.")

    if not usuario_alvo.status:
        raise HTTPException(status_code=409, detail="Usuário desativado.")

    if any(u.id == usuario_id for u in grupo.usuarios):
        raise HTTPException(status_code=409, detail="Usuário já pertence ao grupo.")

    try:
        associar_usuario_grupo(grupo_id, usuario_id)
        logger.info(
            "USUARIO_ASSOCIADO_GRUPO | Admin_ID=%s | Grupo_ID=%s | Usuario_ID=%s",
            usuario_autenticado.id,
            grupo_id,
            usuario_id
        )
    except sqlite3.IntegrityError:
        raise HTTPException(
            status_code=409,
            detail="Não foi possível realizar a associação.",
        )
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Erro interno ao associar usuário ao grupo.",
        )

    return {
        "mensagem": "Usuário associado ao grupo com sucesso.",
        "grupo_id": grupo_id,
        "usuario_id": usuario_id,
    }


@app.post("/grupos/{grupo_id}/roles/{role_id}")
def adicionar_role_ao_grupo(
    grupo_id: int,
    role_id: int,
    usuario_autenticado=Depends(exigir_permissao("GERENCIAR_GRUPOS"))
):
    grupos = consultar_grupos()
    roles = consultar_roles()

    grupo = next((g for g in grupos if g.id == grupo_id), None)
    role = next((r for r in roles if r.id == role_id), None)

    if grupo is None:
        raise HTTPException(status_code=404, detail="Grupo não encontrado.")

    if role is None:
        raise HTTPException(status_code=404, detail="Role não encontrada.")

    if not grupo.status:
        raise HTTPException(status_code=409, detail="Grupo desativado.")

    if not role.status:
        raise HTTPException(status_code=409, detail="Role desativada.")

    if any(r.id == role_id for r in grupo.roles):
        raise HTTPException(status_code=409, detail="Role já pertence ao grupo.")

    try:
        associar_role_grupo(grupo_id, role_id)
        logger.info(
            "ROLE_ASSOCIADA_GRUPO | Admin_ID=%s | Grupo_ID=%s | Role_ID=%s",
            usuario_autenticado.id,
            grupo_id,
            role_id
        )
    except sqlite3.IntegrityError:
        raise HTTPException(
            status_code=409,
            detail="Não foi possível realizar a associação.",
        )
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Erro interno ao associar Role ao grupo.",
        )

    return {
        "mensagem": "Role associada ao grupo com sucesso.",
        "grupo_id": grupo_id,
        "role_id": role_id,
    }

@app.post("/auth/login")
def realizar_login(dados: LoginEntrada, request: Request):
    ip = request.client.host if request.client else "desconhecido"

    if not verificar_limite(ip):
        logger.warning(
            "LOGIN_BLOQUEADO | IP=%s",
            ip
        )
        raise HTTPException(
            status_code=429,
            detail="Muitas tentativas de login. Aguarde 1 minuto."
        )

    registro = consultar_usuario_login(dados.matricula)

    if registro is None:
        registrar_tentativa_falha(ip)
        logger.warning(
            "LOGIN_FALHA | Motivo=Usuario_nao_encontrado | IP=%s",
            ip
        )
        raise HTTPException(
            status_code=401,
            detail="Matrícula ou senha inválida."
        )

    usuario_id, _, status, senha_hash = registro

    if not status or not senha_hash:
        registrar_tentativa_falha(ip)
        logger.warning(
            "LOGIN_FALHA | Usuario_ID=%s | Motivo=Usuario_inativo_ou_sem_hash | IP=%s",
            usuario_id,
            ip
        )
        raise HTTPException(
            status_code=401,
            detail="Matrícula ou senha inválida."
        )

    if not verificar_senha(dados.senha, senha_hash):
        registrar_tentativa_falha(ip)
        logger.warning(
            "LOGIN_FALHA | Usuario_ID=%s | Motivo=Senha_invalida | IP=%s",
            usuario_id,
            ip
        )
        raise HTTPException(
            status_code=401,
            detail="Matrícula ou senha inválida."
        )

    token = criar_access_token(usuario_id)

    logger.info(
        "LOGIN_SUCESSO | Usuario_ID=%s | IP=%s",
        usuario_id,
        ip
    )

    return {
        "access_token": token,
        "token_type": "bearer",
        "expires_in": TEMPO_EXPIRACAO_MINUTOS * 60
    }

@app.get("/auth/me")
def consultar_usuario_autenticado(
    usuario_autenticado=Depends(obter_usuario_atual)
):
    return {
        "id": usuario_autenticado.id,
        "nome": usuario_autenticado.nome,
        "matricula": usuario_autenticado.matricula,
        "departamento": usuario_autenticado.departamento,
        "cargo": usuario_autenticado.cargo,
        "status": usuario_autenticado.status
    }