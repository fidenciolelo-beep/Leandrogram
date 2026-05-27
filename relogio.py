from datetime import datetime
import sqlite3
import schedule
import time 
import requests

def minha_tarefa():
    # 1. Abre a conexão e cria o cursor primeiro
    conexao = sqlite3.connect("historico_btc.db")
    cursor = conexao.cursor()

    # 2. Executa o comando que você escreveu, mas dentro do cursor.execute()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS historico (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        preco TEXT, data_hora TEXT
    )
    """)

    disfarce = {"User-Agent": "Mozilla/5.0 (windows NT 10.0; win64; x64)"}
    resposta = requests.get("http://api.coinbase.com/v2/prices/BTC-USD/spot", headers=disfarce)
    dados = resposta.json()
    preco = dados["data"]["amount"]
    agora = datetime.now().strftime("%d/%m/%Y/%H:%M:%S")
    
    print(f"O preço do Bitcoin agora é: ${preco}")

    cursor.execute("INSERT INTO historico (preco, data_hora) VALUES (?,?)", (preco, agora))
    conexao.commit()
    conexao.close()

schedule.every(10).seconds.do(minha_tarefa)

print("Agendador Iniciado... Pressione CTRL C para parar.")

while True:
    schedule.run_pending()
    time.sleep(1)
