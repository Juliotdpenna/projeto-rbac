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
