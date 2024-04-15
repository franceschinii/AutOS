#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import os
import time

def delete_json_files(directory):
    # Verificar se o diretório existe
    if not os.path.exists(directory):
        print(f"O diretório {directory} não existe.")
        return
    
    try:
        # Obter a lista de arquivos na pasta
        json_files = [f for f in os.listdir(directory) if f.endswith('.json')]
        
        # Deletar cada arquivo
        for file in json_files:
            file_path = os.path.join(directory, file)
            os.remove(file_path)
            print(f"Arquivo {file} deletado com sucesso.")
        
        print("Todos os arquivos JSON foram deletados.")

    except Exception as e:
        print(f"Ocorreu um erro ao deletar os arquivos JSON: {e}")

# Diretório onde os arquivos JSON estão localizados
json_directory = 'DIRETÓRIO_DA_PASTA_DOS_JSONS'

while True:
    # Deletar os arquivos JSON
    delete_json_files(json_directory)

    # Aguardar 2 horas antes de deletar novamente
    time.sleep(2 * 60 * 60)  # 2 horas em segundos


# In[ ]:




