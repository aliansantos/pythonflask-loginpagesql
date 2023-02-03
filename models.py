class Comentario:
    def __init__(self, nome, comentario, id=None):
        self.id = id
        self.nome = nome
        self.comentario = comentario

class Usuario:
    def __init__(self, id, nome, senha):
        self.id = id
        self.nome = nome
        self.senha = senha