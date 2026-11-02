from models.grupo import Grupo
from models.role import Role
from models.permissao import Permissao
from models.usuario import Usuario


def criar_usuario():
    role = Role(1, "ROLE_TI", "Role de TI", True)

    return Usuario(
        1,
        "João",
        "123456",
        "TI",
        "Analista de TI",
        True,
        role
    )


def test_adicionar_usuario_ao_grupo():
    usuario = criar_usuario()
    grupo = Grupo(1, "EQUIPE_TI", "Equipe de TI", True)

    grupo.adicionar_usuario(usuario)

    assert usuario in grupo.usuarios
    assert grupo in usuario.grupos


def test_nao_adicionar_usuario_duplicado():
    usuario = criar_usuario()
    grupo = Grupo(1, "EQUIPE_TI", "Equipe de TI", True)

    grupo.adicionar_usuario(usuario)
    grupo.adicionar_usuario(usuario)

    assert grupo.usuarios.count(usuario) == 1
    assert usuario.grupos.count(grupo) == 1


def test_remover_usuario_do_grupo():
    usuario = criar_usuario()
    grupo = Grupo(1, "EQUIPE_TI", "Equipe de TI", True)

    grupo.adicionar_usuario(usuario)
    grupo.remover_usuario(usuario)

    assert usuario not in grupo.usuarios
    assert grupo not in usuario.grupos


def test_grupo_desativado_nao_adiciona_usuario():
    usuario = criar_usuario()
    grupo = Grupo(1, "EQUIPE_TI", "Equipe de TI", False)

    grupo.adicionar_usuario(usuario)

    assert usuario not in grupo.usuarios
    assert grupo not in usuario.grupos


def test_grupo_nao_adiciona_usuario_desativado():
    usuario = criar_usuario()
    usuario.desativar()
    grupo = Grupo(1, "EQUIPE_TI", "Equipe de TI", True)

    grupo.adicionar_usuario(usuario)

    assert usuario not in grupo.usuarios
    assert grupo not in usuario.grupos


def test_adicionar_role_ao_grupo():
    grupo = Grupo(1, "EQUIPE_TI", "Equipe de TI", True)
    role = Role(2, "ROLE_ANALISTA", "Role de analista", True)

    grupo.adicionar_role(role)

    assert role in grupo.roles


def test_nao_adicionar_role_duplicada_ao_grupo():
    grupo = Grupo(1, "EQUIPE_TI", "Equipe de TI", True)
    role = Role(2, "ROLE_ANALISTA", "Role de analista", True)

    grupo.adicionar_role(role)
    grupo.adicionar_role(role)

    assert grupo.roles.count(role) == 1


def test_grupo_nao_adiciona_role_desativada():
    grupo = Grupo(1, "EQUIPE_TI", "Equipe de TI", True)
    role = Role(2, "ROLE_ANALISTA", "Role de analista", False)

    grupo.adicionar_role(role)

    assert role not in grupo.roles


def test_remover_role_do_grupo():
    grupo = Grupo(1, "EQUIPE_TI", "Equipe de TI", True)
    role = Role(2, "ROLE_ANALISTA", "Role de analista", True)

    grupo.adicionar_role(role)
    grupo.remover_role(role)

    assert role not in grupo.roles


def test_usuario_mantem_acesso_direto_apos_sair_do_grupo():
    usuario = criar_usuario()
    role_direta = usuario.roles_diretas[0]

    permissao = Permissao(
        1, "CONSULTAR_CRM", "Consultar CRM", True
    )
    role_direta.adicionar_permissao(permissao)

    grupo = Grupo(1, "EQUIPE_TI", "Equipe de TI", True)
    grupo.adicionar_role(role_direta)
    grupo.adicionar_usuario(usuario)

    grupo.remover_usuario(usuario)

    assert usuario.pode_acessar(permissao) is True


def test_usuario_mantem_acesso_por_outro_grupo():
    usuario = criar_usuario()

    permissao = Permissao(
        1, "CONSULTAR_CRM", "Consultar CRM", True
    )
    role = Role(2, "ROLE_ANALISTA", "Role de analista", True)
    role.adicionar_permissao(permissao)

    grupo_a = Grupo(1, "EQUIPE_TI_A", "Equipe de TI A", True)
    grupo_b = Grupo(2, "EQUIPE_TI_B", "Equipe de TI B", True)

    grupo_a.adicionar_role(role)
    grupo_b.adicionar_role(role)

    grupo_a.adicionar_usuario(usuario)
    grupo_b.adicionar_usuario(usuario)

    grupo_a.remover_usuario(usuario)

    assert usuario.pode_acessar(permissao) is True


def test_usuario_mantem_acesso_por_outro_grupo_apos_remover_role():
    usuario = criar_usuario()

    permissao = Permissao(
        1, "CONSULTAR_CRM", "Consultar CRM", True
    )

    role = Role(2, "ROLE_ANALISTA", "Role de analista", True)
    role.adicionar_permissao(permissao)

    grupo_a = Grupo(1, "EQUIPE_TI_A", "Equipe de TI A", True)
    grupo_b = Grupo(2, "EQUIPE_TI_B", "Equipe de TI B", True)

    grupo_a.adicionar_role(role)
    grupo_b.adicionar_role(role)

    grupo_a.adicionar_usuario(usuario)
    grupo_b.adicionar_usuario(usuario)

    grupo_a.remover_role(role)

    assert usuario.pode_acessar(permissao) is True
