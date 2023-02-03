import MySQLdb
print('Conectando...')
conn = MySQLdb.connect(user='root', passwd='senhateste@2023', host='localhost', port=3306)

# Descomente se quiser desfazer o banco...
#conn.cursor().execute("DROP DATABASE `site`;")
#conn.commit()

criar_tabelas = '''SET NAMES utf8;
    CREATE DATABASE `site` /*!40100 DEFAULT CHARACTER SET utf8 COLLATE utf8_bin */;
    USE `site`;
    CREATE TABLE `comentario` (
      `id` int(11) NOT NULL AUTO_INCREMENT,
      `nome` varchar(50) COLLATE utf8_bin NOT NULL,
      `comentario` varchar(40) COLLATE utf8_bin NOT NULL,
      PRIMARY KEY (`id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
    CREATE TABLE `usuario` (
      `id` varchar(8) COLLATE utf8_bin NOT NULL,
      `nome` varchar(20) COLLATE utf8_bin NOT NULL,
      `senha` varchar(8) COLLATE utf8_bin NOT NULL,
      PRIMARY KEY (`id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;'''

conn.cursor().execute(criar_tabelas)

# inserindo usuarios
cursor = conn.cursor()
cursor.executemany(
      'INSERT INTO site.usuario (id, nome, senha) VALUES (%s, %s, %s)',
      [
            ('alian', 'Alian dos Santos', 'senha888')
      ])

cursor.execute('select * from site.usuario')
print(' -------------  Usuários:  -------------')
for user in cursor.fetchall():
    print(user[1])

# inserindo jogos
cursor.executemany(
      'INSERT INTO site.comentario (nome, comentario) VALUES (%s, %s)',
      [
            ('Alian', 'Teste')
      ])

cursor.execute('select * from site.comentario')
print(' -------------  Comentarios:  -------------')
for comentario in cursor.fetchall():
    print(comentario[1],comentario[2])

# commitando senão nada tem efeito
conn.commit()
cursor.close()