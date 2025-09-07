import os
import shutil
import re

# 🗂️ Caminho onde estão os arquivos a serem movidos
caminho_arquivos = os.path.join(os.getcwd(), 'arquivos')  # Subpasta 'arquivos' dentro da pasta do script
base_destino = os.getcwd()  # Pasta onde o script está

# 🔍 Expressão regular para capturar número + torre (torre opcional, letra ou número)
padrao_codigo = re.compile(r'(\d{1,6})(?:\s*([A-Z0-9]))?', re.IGNORECASE)

for nome_arquivo in os.listdir(caminho_arquivos):
    caminho_arquivo = os.path.join(caminho_arquivos, nome_arquivo)

    if os.path.isfile(caminho_arquivo):
        resultado = padrao_codigo.search(nome_arquivo)

        if resultado:
            numero_str = resultado.group(1)
            torre = resultado.group(2).upper() if resultado.group(2) else None

            # 🔢 Remove zeros à esquerda do número
            numero = str(int(numero_str))

            if torre:
                # Com torre
                nome_pasta = f"{numero} {torre}"
                destino_pasta = os.path.join(base_destino, torre, nome_pasta)
            else:
                # Sem torre
                nome_pasta = numero
                destino_pasta = os.path.join(base_destino, nome_pasta)

            # 🚚 Cria as pastas se não existirem e move o arquivo
            os.makedirs(destino_pasta, exist_ok=True)
            destino_arquivo = os.path.join(destino_pasta, nome_arquivo)

            shutil.move(caminho_arquivo, destino_arquivo)

            print(f"Movido: {nome_arquivo} → {destino_pasta}")
        else:
            print(f"Código não identificado no nome do arquivo: {nome_arquivo}")

print("✅ Processo concluído.")

    




