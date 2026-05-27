import sqlite3

# 1. Conecta no mesmo arquivo criado pelo robô
conexao = sqlite3.connect("historico_btc.db")
cursor = conexao.cursor()

# 2. Busca todas as linhas da tabela historico
cursor.execute("SELECT id, preco, data_hora  FROM historico")
linhas = cursor.fetchall()

# 3. Mostra linha por linha na tela
print("--- HISTÓRICO SALVO NO BANCO ---")
for linha in linhas:
    print(f"ID: {linha[0]} | Preço Guardado: ${linha[1]} | Hora: {linha[2]}")

# 4. Fecha a conexão
conexao.close()

