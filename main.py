from models.role import Role
from models.permissao import Permissao
from models.usuario import Usuario

def consultar_usuarios(usuarios):
    if not usuarios:
        print("Não existem usuários cadastrados.")
    else:
        for usuario in usuarios:
            print(f"Nome: {usuario.nome}")
            print(f"Matrícula: {usuario.matricula}")
            print(f"Departamento: {usuario.departamento}")
            print(f"Cargo: {usuario.cargo}")
            print("--------------------")

def consultar_roles(roles):
    if not roles:
        print("Não existem Roles cadastradas.")
    else:
        for role in roles:
            print(f"Nome: {role.nome}")
            print(f"Descrição: {role.descricao}")
            print(f"Status: {role.status}")
            print("--------------------")

def consultar_permissoes(permissoes):
    if not permissoes:
        print("Não existem permissões cadastradas.")
    else:
        for permissao in permissoes:
            print(f"Nome: {permissao.nome}")
            print(f"Descrição: {permissao.descricao}")
            print(f"Status: {permissao.status}")
            print("--------------------")

role_ti = Role(
    1,
    "ROLE_ANALISTA_TI",
    "Permissoes para Analistas de TI",
    True
)

usuario_joao = Usuario(
    1,
    "João",
    "123456",
    "TI",
    "Analista de TI",
    True,
    role_ti
)

role_gerente = Role(
    2,
    "ROLE_GERENTE_TI",
    "Permissoes para Gerentes de TI",
    True
)

roles = [role_ti, role_gerente]

permissao_crm = Permissao(
    1,
    "VISUALIZAR_CRM",
    "Permite visualizar informacoes do CRM",
    True
)

permissao_editar = Permissao(
    2,
    "EDITAR_CRM",
    "Permite editar informacoes do CRM",
    False
)

permissao_editar.ativar()

permissoes = [permissao_crm, permissao_editar]

usuario_joao.alterar_role(role_gerente)

for permissao in usuario_joao.role.permissoes:
    print(permissao.nome)

print(usuario_joao.role.nome)

role_gerente.adicionar_permissao(permissao_crm)

usuario_joao.alterar_role(role_gerente)

if usuario_joao.pode_acessar(permissao_crm):
    print("Acesso permitido.")
else:
    print("Acesso negado.")

if usuario_joao.pode_acessar(permissao_crm):
    print("João, estando ativo e com a Role_GERENTE_TI ativa, consegue acessar Visualizar_CRM?")

print(usuario_joao.role.nome)
print(usuario_joao.nome)
print(usuario_joao.role.nome)

print(role_ti.nome)
print(role_ti.status)

permissao_crm = Permissao(
    1,
    "VISUALIZAR_CRM",
    "Permite visualizar informacoes do CRM",
    True
)

role_ti.adicionar_permissao(permissao_crm)

print(role_ti.permissoes)
print(role_ti.permissoes[0].nome)

permissao_editar = Permissao(
    2,
    "EDITAR_CRM",
    "Permite editar informacoes do CRM",
    False
)

role_ti.adicionar_permissao(permissao_editar)

permissao_editar.ativar()

role_ti.adicionar_permissao(permissao_editar)

print(role_ti.permissoes)

for permissao in role_ti.permissoes:
    print(permissao.nome)

role_ti.remover_permissao(permissao_editar)
print(role_ti.permissoes)

role_ti.remover_permissao(permissao_editar)

role_ti.consultar_permissoes()

role_rh = Role(
    2,
    "ROLE_RH",
    "Permissões para o RH",
    True
)

role_rh.consultar_permissoes()

permissao_financeiro = Permissao(
    3,
    "ACESSAR_FINANCEIRO",
    "Permite visualizar informações financeiras",
    True
)

print(usuario_joao.pode_acessar(permissao_financeiro))

usuario_joao.desativar()

print(usuario_joao.pode_acessar(permissao_crm))

usuario_joao.status = True

role_gerente.desativar()

print(usuario_joao.pode_acessar(permissao_crm))

usuario_joao.status = True
role_gerente.ativar()
permissao_crm.desativar()

print(usuario_joao.pode_acessar(permissao_crm))

usuarios = [usuario_joao]

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