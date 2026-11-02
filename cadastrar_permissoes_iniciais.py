from models.permissao import Permissao
from database.repositorio import (
    cadastrar_permissao,
    consultar_permissoes,
)


permissoes_iniciais = [
    ("VISUALIZAR_USUARIOS", "Permite consultar usuários"),
    ("CADASTRAR_USUARIOS", "Permite cadastrar usuários"),
    ("EDITAR_USUARIOS", "Permite atualizar usuários"),
    ("DESATIVAR_USUARIOS", "Permite desativar usuários"),
    ("VISUALIZAR_ROLES", "Permite consultar Roles"),
    ("GERENCIAR_ROLES", "Permite criar Roles e associar permissões"),
    ("VISUALIZAR_PERMISSOES", "Permite consultar permissões"),
    ("GERENCIAR_PERMISSOES", "Permite cadastrar permissões"),
    ("VISUALIZAR_GRUPOS", "Permite consultar grupos"),
    ("GERENCIAR_GRUPOS", "Permite administrar grupos e associações"),
]


permissoes_existentes = consultar_permissoes()

nomes_existentes = {
    permissao.nome for permissao in permissoes_existentes
}

for nome, descricao in permissoes_iniciais:

    if nome in nomes_existentes:
        print(f"Já existe: {nome}")
        continue

    permissao = Permissao(
        None,
        nome,
        descricao,
        True,
    )

    try:
        cadastrar_permissao(permissao)
        print(f"Cadastrada: {nome}")

    except Exception as erro:
        print(f"Erro ao cadastrar {nome}: {erro}")


print("\nProcesso concluído.")