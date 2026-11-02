class Usuario:

    def __init__(self, id, nome, matricula, departamento, cargo, status, role, senha_hash=None):
        self.id = id
        self.nome = nome
        self.matricula = matricula
        self.departamento = departamento
        self.cargo = cargo
        self.status = status
        self.senha_hash = senha_hash
        
        # Roles atribuídas diretamente ao usuário
        self.roles_diretas = []

        # Grupos aos quais o usuário pertence
        self.grupos = []

        # Compatibilidade temporária com o modelo anterior
        if role is not None and role.status:
            self.roles_diretas.append(role)

    @property
    def role(self):
        """Retorna a primeira Role direta, para compatibilidade temporária."""
        return self.roles_diretas[0] if self.roles_diretas else None

    def desativar(self):
        self.status = False

    def adicionar_role(self, role):
        if not role.status:
            print("A Role está desativada. Atribuição recusada.")
        elif role in self.roles_diretas:
            print("Essa Role já está atribuída diretamente ao usuário.")
        else:
            self.roles_diretas.append(role)
            print("Role atribuída com sucesso.")

    def alterar_role(self, nova_role):
        if not nova_role.status:
            print("A nova Role está desativada. Atribuição recusada.")
        else:
            self.roles_diretas = [nova_role]
            print("Role alterada com sucesso.")

    
    def pode_acessar(self, permissao):
        if not self.status or not permissao.status:
            return False

        # Verifica as Roles atribuídas diretamente
        for role in self.roles_diretas:
            if not role.status:
                continue

            for permissao_role in role.permissoes:
                if permissao_role.id == permissao.id and permissao_role.status:
                    return True

        # Verifica as Roles recebidas por grupos ativos
        for grupo in self.grupos:
            if not grupo.status:
                continue

            for role in grupo.roles:
                if not role.status:
                    continue

                for permissao_role in role.permissoes:
                    if permissao_role.id == permissao.id and permissao_role.status:
                        return True

        return False