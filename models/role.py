class Role:

    def __init__(self, id, nome, descricao, status):
        self.id = id
        self.nome = nome
        self.descricao = descricao
        self.status = status

        self.permissoes = []
        self.sistemas = []

    def ativar(self):
        if self.status:
            print("A role já está ativa.")
        else:
            self.status = True
            print("Role ativada com sucesso.")

    def desativar(self):
        if self.status:
            self.status = False
            print("Role desativada com sucesso.")
        else:
            print("A Role já está desativada.")

    def adicionar_permissao(self, permissao):
        if permissao in self.permissoes:
            print("Essa permissão já existe na Role.")
        else:
            if permissao.status:
                self.permissoes.append(permissao)
                print("Permissão adicionada com sucesso.")
            else:
                print("Essa permissão está desativada.")

    def remover_permissao(self, permissao):
        if permissao in self.permissoes:
            self.permissoes.remove(permissao)
            print("Permissão removida com sucesso.")
        else:
            print("Essa permissão não existe.")

    def consultar_permissoes(self):
        if not self.permissoes:
            print("A Role não possui permissões.")
        else:
            print("Essas são as permissões existentes:")
            for permissao in self.permissoes:
                print(permissao.nome)