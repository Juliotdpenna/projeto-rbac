class Grupo:

    def __init__(self, id, nome, descricao, status):
        self.id = id
        self.nome = nome
        self.descricao = descricao
        self.status = status

        self.usuarios = []
        self.roles = []

    def adicionar_usuario(self, usuario):
        if not self.status:
            print("O grupo está desativado.")
        elif not usuario.status:
            print("O usuário está desativado.")
        elif usuario in self.usuarios:
            print("O usuário já pertence ao grupo.")
        else:
            self.usuarios.append(usuario)

            if self not in usuario.grupos:
                usuario.grupos.append(self)

            print("Usuário adicionado ao grupo com sucesso.")

    def remover_usuario(self, usuario):
        if usuario not in self.usuarios:
            print("O usuário não pertence ao grupo.")
        else:
            self.usuarios.remove(usuario)

            if self in usuario.grupos:
                usuario.grupos.remove(self)

            print("Usuário removido do grupo com sucesso.")

    def adicionar_role(self, role):
        if not self.status:
            print("O grupo está desativado.")
        elif not role.status:
            print("A Role está desativada.")
        elif role in self.roles:
            print("Essa Role já pertence ao grupo.")
        else:
            self.roles.append(role)
            print("Role adicionada ao grupo com sucesso.")

    def remover_role(self, role):
        if role not in self.roles:
            print("Essa Role não pertence ao grupo.")
        else:
            self.roles.remove(role)
            print("Role removida do grupo com sucesso.")