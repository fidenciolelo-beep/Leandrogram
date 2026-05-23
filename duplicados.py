import os
import hashlib
from collections import defaultdict

def calcular_hash(arquivo):
    hash_md5 = hashlib.md5()
    try:
        with open(arquivo, 'rb') as f:
            for bloco in iter(lambda: f.read(4096), b''):
                hash_md5.update(bloco)
        return hash_md5.hexdigest()
    except:
        return None

def encontrar_duplicados(pasta):
    print(f'\n🔍 Varrendo {pasta}...\n')
    arquivos_por_hash = defaultdict(list)
    total = 0

    for raiz, dirs, arquivos in os.walk(pasta):
        for arquivo in arquivos:
            caminho = os.path.join(raiz, arquivo)
            hash_arquivo = calcular_hash(caminho)
            if hash_arquivo:
                arquivos_por_hash[hash_arquivo].append(caminho)
                total += 1

    print(f'✅ {total} arquivos verificados\n')

    duplicados = {h: caminhos for h, caminhos in arquivos_por_hash.items() if len(caminhos) > 1}

    if not duplicados:
        print('🎉 Nenhum duplicado encontrado!')
        return

    print(f'⚠️  {len(duplicados)} grupos de duplicados encontrados:\n')

    espaco_total = 0
    for i, (hash_val, caminhos) in enumerate(duplicados.items(), 1):
        tamanho = os.path.getsize(caminhos[0])
        espaco_total += tamanho * (len(caminhos) - 1)
        print(f'Grupo {i}:')
        for j, caminho in enumerate(caminhos):
            print(f'  {"✅ MANTER" if j == 0 else "❌ DUPLICADO"} → {caminho}')
        print()

    print(f'💾 Espaço que pode ser liberado: {espaco_total / 1024 / 1024:.2f} MB\n')

    resposta = input('Deseja deletar os duplicados? (s/n): ')
    if resposta.lower() == 's':
        deletados = 0
        for caminhos in duplicados.values():
            for caminho in caminhos[1:]:
                try:
                    os.remove(caminho)
                    deletados += 1
                except:
                    print(f'Não foi possível deletar: {caminho}')
        print(f'\n🗑️  {deletados} arquivos deletados com sucesso!')
    else:
        print('\n❌ Nenhum arquivo deletado.')

pasta = '/storage/emulated/0'
encontrar_duplicados(pasta)
