# 🚀 LeandroGram

Projeto web desenvolvido do zero com Python, Flask e SQLite.

## 🛠️ Tecnologias usadas
- Python 3
- Flask (servidor web)
- SQLite (banco de dados)
- HTML, CSS, JavaScript
- API do Google Gemini (IA)

## 📋 Funcionalidades
- Sistema de login e cadastro com senha criptografada
- Painel admin protegido com sessão
- Jornal personalizado gerado por IA
- Notificações em tempo real via Ntfy
- Script de limpeza de arquivos duplicados

## 🌐 Site no ar
[leandrogram.pythonanywhere.com](https://leandrogram.pythonanywhere.com)

## 📱 Como rodar localmente
```bash
pip install flask requests python-dotenv werkzeug
python app.py
```

## 👨‍💻 Desenvolvedor
Leandro — aprendendo desenvolvimento web do zero

## 🗄️ Banco de Dados — SQL

Comandos aprendidos:

- `SELECT * FROM tabela` — buscar todos os dados
- `SELECT coluna FROM tabela` — buscar colunas específicas
- `WHERE` — filtrar resultados
- `COUNT(*)` — contar registros
- `ORDER BY coluna DESC` — ordenar resultados
- `LIMIT 3` — limitar quantidade
- `INSERT INTO` — inserir dados
- `UPDATE SET` — atualizar dados
- `DELETE FROM` — apagar dados

Conceito: **CRUD** — Create, Read, Update, Delete

## 🔗 JavaScript + Flask + Banco de Dados

Aprendi a conectar as três camadas de um sistema web:

- **HTML** — formulário para o usuário digitar
- **JavaScript** — envia a consulta para o servidor com `fetch`
- **Flask** — recebe a requisição e processa
- **SQLite** — consulta o banco e retorna a resposta

Conceitos aprendidos:
- `fetch` — faz requisições HTTP pelo JavaScript
- `await` — espera a resposta do servidor antes de continuar
- Rotas Flask que consultam o banco de dados
- Fluxo completo: usuário → JavaScript → Flask → SQLite → resposta


## 🤖 Projeto Bônus: Monitor Automático de Bitcoin (SQLite + Automação)

Desenvolvi também um robô de automação em segundo plano que roda direto no Termux. Ele monitora o valor do Bitcoin e cria um histórico cronológico local.

### O que foi aplicado:
- **`schedule`** e **`time`**: Para criar um loop estável de checagem a cada 10 segundos.
- **`requests`**: Com cabeçalhos customizados (`headers`) para simular um navegador e evitar bloqueios.
- **`datetime`**: Para registrar a estampa de tempo real (`data_hora`) de cada captura.
- **Tratamento de Tuplas**: Passagem segura de parâmetros `(preco, agora)` para prevenir falhas de tipos e injeções no SQLite.

