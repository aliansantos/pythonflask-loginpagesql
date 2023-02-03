from models import Comentario, Usuario

SQL_DELETA_COMENTARIO = 'delete from comentario where id = %s'
SQL_COMENTARIO_POR_ID = 'SELECT id, nome, comentario from comentario where id = %s'
SQL_USUARIO_POR_ID = 'SELECT id, nome, senha from usuario where id = %s'
SQL_ATUALIZA_COMENTARIO = 'UPDATE comentario SET nome=%s, comentario=%s where id = %s'
SQL_BUSCA_COMENTARIOS = 'SELECT id, nome, comentario from comentario'
SQL_CRIA_COMENTARIO = 'INSERT into comentario (nome, comentario) values (%s, %s)'


class ComentarioDao:
    def __init__(self, db):
        self.__db = db

    def salvar(self, comentario):
        cursor = self.__db.connection.cursor()

        if (comentario.id):
            cursor.execute(SQL_ATUALIZA_COMENTARIO, (comentario.nome, comentario.comentario, comentario.id))
        else:
            cursor.execute(SQL_CRIA_COMENTARIO, (comentario.nome, comentario.comentario))
            comentario.id = cursor.lastrowid
        self.__db.connection.commit()
        return comentario

    def listar(self):
        cursor = self.__db.connection.cursor()
        cursor.execute(SQL_BUSCA_COMENTARIOS)
        comentarios = traduz_comentarios(cursor.fetchall())
        return comentarios

    def busca_por_id(self, id):
        cursor = self.__db.connection.cursor()
        cursor.execute(SQL_COMENTARIO_POR_ID, (id,))
        tupla = cursor.fetchone()
        return Comentario(tupla[1], tupla[2], tupla[3], id=tupla[0])

    def deletar(self, id):
        self.__db.connection.cursor().execute(SQL_DELETA_COMENTARIO, (id, ))
        self.__db.connection.commit()


class UsuarioDao:
    def __init__(self, db):
        self.__db = db

    def buscar_por_id(self, id):
        cursor = self.__db.connection.cursor()
        cursor.execute(SQL_USUARIO_POR_ID, (id,))
        dados = cursor.fetchone()
        usuario = traduz_usuario(dados) if dados else None
        return usuario


def traduz_comentarios(jogos):
    def cria_jogo_com_tupla(tupla):
        return Comentario(tupla[1], tupla[2], id=tupla[0])
    return list(map(cria_jogo_com_tupla, jogos))


def traduz_usuario(tupla):
    return Usuario(tupla[0], tupla[1], tupla[2])
