class Usuario:

    def __init__(self, id, nome, matricula, departamento, cargo, status, role):
        self.id = id
        self.nome = nome
        self.matricula = matricula
        self.departamento = departamento
        self.cargo = cargo
        self.status = status
        self.role = role


    def desativar(self):
        self.status = False  

    def alterar_role(self, nova_role):
        self.role = nova_role

    def pode_acessar(self, permissao):
        if self.status:
            if self.role.status:
                if permissao in self.role.permissoes:
                    if permissao.status:
                        return True


        return False