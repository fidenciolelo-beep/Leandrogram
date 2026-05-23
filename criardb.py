import sqlite3

conn = sqlite3.connect('leandrogram.db')
conn.execute('''
    CREATE TABLE IF NOT EXISTS acessos (
        id INTEGER PRIMARY KEY,
        usuario TEXT,
        senha TEXT,
        data TEXT
    )
''')
conn.commit()
conn.close()
print('Banco criado com sucesso!')
