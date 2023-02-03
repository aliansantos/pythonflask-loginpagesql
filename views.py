from flask import render_template, request, redirect, session, flash, url_for, send_from_directory
from dao import ComentarioDao, UsuarioDao
from models import Comentario
import os
import time
from helpers import deleta_arquivo, recupera_imagem
from siteinit import db, app

comentario_dao = ComentarioDao(db)
usuario_dao = UsuarioDao(db)

@app.route('/')
def index():
    lista = comentario_dao.listar()
    return render_template('lista.html', titulo='Jogos', lista=lista)


@app.route('/novo')
def novo():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('novo')))
    return render_template('novo.html', titulo='Novo Jogo')


@app.route('/criar', methods=['POST',])
def criar():
    nome = request.form['nome']
    comentario = request.form['comentario']
    comentarios = Comentario(nome, comentario)
    comentarios = comentario_dao.salvar(comentarios)

    arquivo = request.files['arquivo']
    upload_path = app.config['UPLOAD_PATH']
    timestamp = time.time()
    arquivo.save(f'{upload_path}/capa{comentarios.id}-{timestamp}.jpg')
    return redirect(url_for('index'))


@app.route('/editar/<int:id>')
def editar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('editar')))
    jogo = comentario_dao.busca_por_id(id)
    nome_imagem =  recupera_imagem(id)
    capa_jogo = f'capa{id}.jpg'
    return render_template('editar.html', titulo='Editando jogo', jogo=jogo, capa_jogo = nome_imagem)


@app.route('/atualizar', methods=['POST',])
def atualizar():
    nome = request.form['nome']
    comentario = request.form['comentario']
    comentarios = Comentario(nome, comentario, id=request.form['id'])
    comentario_dao.salvar(comentarios)

    arquivo = request.files['arquivo']
    upload_path = app.config['UPLOAD_PATH']
    timestamp = time.time()
    deleta_arquivo(comentarios.id)
    arquivo.save(f'{upload_path}/capa{comentarios.id}-{timestamp}.jpg')
    return redirect(url_for('index'))


@app.route('/deletar/<int:id>')
def deletar(id):
    comentario_dao.deletar(id)
    flash('O jogo foi removido com sucesso!')
    return redirect(url_for('index'))

@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    return render_template('login.html', proxima=proxima)


@app.route('/autenticar', methods=['POST', ])
def autenticar():
    usuario = usuario_dao.buscar_por_id(request.form['usuario'])
    if usuario:
        if usuario.senha == request.form['senha']:
            session['usuario_logado'] = usuario.id
            flash(usuario.nome + ' logou com sucesso!')
            proxima_pagina = request.form['proxima']
            return redirect(proxima_pagina)
    else:
        flash('Não logado, tente denovo!')
        return redirect(url_for('login'))


@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Nenhum usuário logado!')
    return redirect(url_for('index'))


@app.route('/uploads/<nome_arquivo>')
def imagem(nome_arquivo):
    return send_from_directory('uploads', nome_arquivo)