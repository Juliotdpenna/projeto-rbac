
from models.role import Role
from models.permissao import Permissao
from models.usuario import Usuario


# =========================
# FUNÇÕES DE CONSULTA
# =========================

def consultar_usuarios(usuarios):
    if not usuarios:
        print("Não existem usuários cadastrados.")
        return

    for usuario in usuarios:
        print(f"Nome: {usuario.nome}")
        print(f"Matrícula: {usuario.matricula}")
        print(f"Departamento: {usuario.departamento}")
        print(f"Cargo: {usuario.cargo}")
        print(f"Role: {usuario.role.nome}")
        print(f"Status: {usuario.status}")
        print("--------------------")


def consultar_roles(roles):
    if not roles:
        print("Não existem Roles cadastradas.")
        return

    for role in roles:
        print(f"Nome: {role.nome}")
        print(f"Descrição: {role.descricao}")
        print(f"Status: {role.status}")
        print("--------------------")


def consultar_permissoes(permissoes):
    if not permissoes:
        print("Não existem permissões cadastradas.")
        return

    for permissao in permissoes:
        print(f"Nome: {permissao.nome}")
        print(f"Descrição: {permissao.descricao}")
        print(f"Status: {permissao.status}")
        print("--------------------")


# =========================
# CRIAÇÃO DOS OBJETOS
# =========================

role_ti = Role(
    1,
    "ROLE_ANALISTA_TI",
    "Permissões para Analistas de TI",
    True
)

role_gerente = Role(
    2,
    "ROLE_GERENTE_TI",
    "Permissões para Gerentes de TI",
    True
)

roles = [role_ti, role_gerente]


permissao_crm = Permissao(
    1,
    "VISUALIZAR_CRM",
    "Permite visualizar informações do CRM",
    True
)

permissao_editar = Permissao(
    2,
    "EDITAR_CRM",
    "Permite editar informações do CRM",
    True
)

permissoes = [permissao_crm, permissao_editar]


# Associação inicial das permissões às Roles
role_ti.adicionar_permissao(permissao_crm)
role_ti.adicionar_permissao(permissao_editar)

role_gerente.adicionar_permissao(permissao_crm)


# Criação do usuário
usuario_joao = Usuario(
    1,
    "João",
    "123456",
    "TI",
    "Analista de TI",
    True,
    role_ti
)

usuarios = [usuario_joao]


# =========================
# MENU PRINCIPAL
# =========================

while True:
    print("\n=== MENU RBAC ===")
    print("1. Consultar usuários")
    print("2. Consultar Roles")
    print("3. Consultar permissões")
    print("0. Sair")

    opcao = input("Escolha uma opção: ")

    if opcao == "1":
        consultar_usuarios(usuarios)

    elif opcao == "2":
        consultar_roles(roles)

    elif opcao == "3":
        consultar_permissoes(permissoes)

    elif opcao == "0":
        print("Encerrando o sistema.")
        break

    else:
        print("Opção inválida.")
