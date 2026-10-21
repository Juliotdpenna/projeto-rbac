class Permissao:

    def __init__(self, id, nome, descricao, status):
        self.id = id
        self.nome = nome
        self.descricao = descricao
        self.status = status

    def ativar(self):
            if self.status:
                print("A permissão já está ativa.")
            else:
                self.status = True
                print("Permissão ativada com sucesso.")

    def desativar(self):
            if self.status:
                self.status = False
                print("Permissão desativada com sucesso.")
            else:
                print("A permissão já está desativada.")