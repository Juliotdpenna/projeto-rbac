import pytest

from models.grupo import Grupo
from models.role import Role
from models.permissao import Permissao
from models.usuario import Usuario


@pytest.fixture
def ambiente_rbac():
    role_ti = Role(
        1,
        "ROLE_ANALISTA_TI",
        "Permissões para Analistas de TI",
        True
    )

    permissao_crm = Permissao(
        1,
        "VISUALIZAR_CRM",
        "Permite visualizar informações do CRM",
        True
    )

    role_ti.adicionar_permissao(permissao_crm)

    usuario_joao = Usuario(
        1,
        "João",
        "123456",
        "TI",
        "Analista de TI",
        True,
        role_ti
    )

    return usuario_joao, role_ti, permissao_crm


def test_usuario_ativo_pode_acessar_permissao_ativa(ambiente_rbac):
    usuario, role, permissao = ambiente_rbac

    assert usuario.pode_acessar(permissao) is True


def test_usuario_desativado_nao_pode_acessar_permissao_ativa(ambiente_rbac):
    usuario, role, permissao = ambiente_rbac

    usuario.desativar()

    assert usuario.pode_acessar(permissao) is False


def test_usuario_nao_pode_acessar_com_role_desativada(ambiente_rbac):
    usuario, role, permissao = ambiente_rbac

    role.desativar()

    assert usuario.pode_acessar(permissao) is False


def test_usuario_nao_pode_acessar_permissao_fora_da_role(ambiente_rbac):
    usuario, role, permissao = ambiente_rbac

    permissao_financeiro = Permissao(
        2,
        "ACESSAR_FINANCEIRO",
        "Permite visualizar informações financeiras",
        True
    )

    assert usuario.pode_acessar(permissao_financeiro) is False

def test_usuario_nao_pode_acessar_permissao_desativada(ambiente_rbac):
    usuario, role, permissao = ambiente_rbac

    permissao.desativar()

    assert usuario.pode_acessar(permissao) is False


def test_usuario_alterar_role(ambiente_rbac):
    usuario, role_atual, permissao = ambiente_rbac

    role_gerente = Role(
        2,
        "ROLE_GERENTE_TI",
        "Permissões para Gerentes de TI",
        True
    )

    usuario.alterar_role(role_gerente)

    assert usuario.role is role_gerente


def test_usuario_nao_acessa_permissao_que_nao_existe_na_nova_role(ambiente_rbac):
    usuario, role_atual, permissao_crm = ambiente_rbac

    permissao_editar = Permissao(
        2,
        "EDITAR_CRM",
        "Permite editar informações do CRM",
        True
    )

    role_gerente = Role(
        2,
        "ROLE_GERENTE_TI",
        "Permissões para Gerentes de TI",
        True
    )

    usuario.alterar_role(role_gerente)

    assert usuario.pode_acessar(permissao_editar) is False

def test_usuario_nao_altera_role_para_role_desativada(ambiente_rbac):
    usuario, role_atual, _ = ambiente_rbac

    role_desativada = Role(
        2,
        "ROLE_GERENTE_TI",
        "Permissões para Gerentes de TI",
        False
    )

    usuario.alterar_role(role_desativada)

    assert usuario.role is role_atual

def test_usuario_acessa_permissao_recebida_por_grupo(ambiente_rbac):
    usuario, _, _ = ambiente_rbac

    permissao = Permissao(2, "CONSULTAR_CRM", "Consultar CRM", True)
    role = Role(2, "ROLE_ANALISTA", "Role de analista", True)
    role.adicionar_permissao(permissao)

    grupo = Grupo(1, "EQUIPE_TI", "Equipe de TI", True)
    grupo.adicionar_role(role)
    grupo.adicionar_usuario(usuario)

    assert usuario.pode_acessar(permissao) is True


def test_usuario_nao_acessa_por_grupo_desativado(ambiente_rbac):
    usuario, _, _ = ambiente_rbac

    permissao = Permissao(2, "CONSULTAR_CRM", "Consultar CRM", True)
    role = Role(2, "ROLE_ANALISTA", "Role de analista", True)
    role.adicionar_permissao(permissao)

    grupo = Grupo(1, "EQUIPE_TI", "Equipe de TI", True)
    grupo.adicionar_role(role)
    grupo.adicionar_usuario(usuario)
    grupo.status = False

    assert usuario.pode_acessar(permissao) is False


def test_usuario_mantem_acesso_direto_com_grupo_desativado(ambiente_rbac):
    usuario, role_direta, _ = ambiente_rbac

    permissao = Permissao(2, "CONSULTAR_CRM", "Consultar CRM", True)
    role_direta.adicionar_permissao(permissao)

    grupo = Grupo(1, "EQUIPE_TI", "Equipe de TI", True)
    grupo.adicionar_role(role_direta)
    grupo.adicionar_usuario(usuario)
    grupo.status = False

    assert usuario.pode_acessar(permissao) is True
