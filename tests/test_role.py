
from models.role import Role
from models.permissao import Permissao


def test_role_nao_adiciona_permissao_desativada():
    role = Role(
        1,
        "ROLE_ANALISTA_TI",
        "Permissões para Analistas de TI",
        True
    )

    permissao = Permissao(
        1,
        "EDITAR_CRM",
        "Permite editar informações do CRM",
        False
    )

    role.adicionar_permissao(permissao)

    assert permissao not in role.permissoes

def test_role_nao_adiciona_mesma_permissao_duas_vezes():
    role = Role(
        1,
        "ROLE_ANALISTA_TI",
        "Permissões para Analistas de TI",
        True
    )

    permissao = Permissao(
        1,
        "VISUALIZAR_CRM",
        "Permite visualizar informações do CRM",
        True
    )

    role.adicionar_permissao(permissao)
    role.adicionar_permissao(permissao)

    assert len(role.permissoes) == 1


def test_role_remove_permissao_existente():
    role = Role(
        1,
        "ROLE_ANALISTA_TI",
        "Permissões para Analistas de TI",
        True
    )

    permissao = Permissao(
        1,
        "VISUALIZAR_CRM",
        "Permite visualizar informações do CRM",
        True
    )

    role.adicionar_permissao(permissao)
    role.remover_permissao(permissao)

    assert len(role.permissoes) == 0


def test_role_nao_remove_permissao_inexistente():
    role = Role(
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

    permissao_financeiro = Permissao(
        2,
        "ACESSAR_FINANCEIRO",
        "Permite acessar informações financeiras",
        True
    )

    role.adicionar_permissao(permissao_crm)
    role.remover_permissao(permissao_financeiro)

    assert len(role.permissoes) == 1
    assert permissao_crm in role.permissoes


def test_role_ativar_role_desativada():
    role = Role(
        1,
        "ROLE_ANALISTA_TI",
        "Permissões para Analistas de TI",
        False
    )

    role.ativar()

    assert role.status is True


def test_role_desativar_role_ativa():
    role = Role(
        1,
        "ROLE_ANALISTA_TI",
        "Permissões para Analistas de TI",
        True
    )

    role.desativar()

    assert role.status is False


def test_role_desativar_role_ja_desativada():
    role = Role(
        1,
        "ROLE_ANALISTA_TI",
        "Permissões para Analistas de TI",
        False
    )

    role.desativar()

    assert role.status is False


def test_role_exibe_mensagem_ao_desativar_role_ja_desativada(capsys):
    role = Role(
        1,
        "ROLE_ANALISTA_TI",
        "Permissões para Analistas de TI",
        False
    )

    role.desativar()

    resultado = capsys.readouterr()

    assert "A Role já está desativada." in resultado.out
