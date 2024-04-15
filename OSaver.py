#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import os
import json
import mysql.connector
from datetime import datetime
import time

# Função para encontrar o arquivo JSON mais recente no diretório
def find_latest_json(directory):
    json_files = [f for f in os.listdir(directory) if f.endswith('.json')]
    if not json_files:
        return None
    # Obtém o caminho completo de cada arquivo e o tempo de modificação
    files_with_mtime = [(os.path.join(directory, f), os.path.getmtime(os.path.join(directory, f))) for f in json_files]
    # Retorna o arquivo JSON mais recente com base no tempo de modificação
    return max(files_with_mtime, key=lambda x: x[1])[0]

# Função para converter data de "dd/mm/yyyy" para "yyyy-mm-dd"
def convert_date(date_string):
    supported_formats = ['%d/%m/%Y', '%d/%m/%Y %H:%M:%S', '%Y-%m-%d']
    for date_format in supported_formats:
        try:
            date_object = datetime.strptime(date_string, date_format)
            return date_object.strftime('%Y-%m-%d')
        except ValueError:
            continue
    return None

# Função para realizar o backup da tabela antiga
def backup_old_table(cursor, backup_table_name):
    try:
        # Criar o nome da tabela de backup com o formato "ostable_DATA E HORA DA CRIAÇÃO DA TABELA_old"
        current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_table_name_with_time = f"{backup_table_name}_{current_time}_old"

        # Realizar o backup da tabela antiga
        cursor.execute(f"CREATE TABLE {backup_table_name_with_time} AS SELECT * FROM {backup_table_name}")

        print(f"Tabela antiga '{backup_table_name}' salva como '{backup_table_name_with_time}'.")

    except mysql.connector.Error as error:
        print("Erro ao realizar o backup da tabela antiga:", error)

# Função para ler dados do JSON e inserir no banco de dados MySQL
def insert_data_from_json(json_file, backup_table_name):
    # Carregar dados do JSON
    with open(json_file, 'r') as file:
        data = json.load(file)

    # Configurações de conexão com o banco de dados MySQL
    db_config = {
        'host': 'localhost',
        'user': 'root',
        'password': 'SENHA_DA_SUA_DATABASE',
        'database': 'NOME_DA_SUA_DATABASE'
    }

    try:
        # Conectar ao banco de dados
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        # Realizar backup da tabela antiga
        backup_old_table(cursor, backup_table_name)

        # Limpar os dados antigos na tabela do banco de dados
        cursor.execute("DELETE FROM OSTable")

        # Iterar sobre os dados e inseri-los na tabela do banco de dados
        for row in data:
            # Converter a data de entrada
            entry_date = convert_date(row[3])
            if entry_date:
                row[3] = entry_date
            else:
                print(f"Erro ao converter data de entrada para a linha: {row}")
                continue
            
            # Converter a data de conclusão
            completion_date = convert_date(row[4]) if row[4] != '' else None

            # Inserir os dados na tabela do banco de dados
            sql = "INSERT INTO NOME_DA_TABELA_DA_DATABASE (os_number, client_name, status, entry_date, completion_date, equipment) VALUES (%s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, (row[0], row[1], row[2], row[3], completion_date, row[5]))

        # Confirmar as alterações
        connection.commit()
        print("Dados inseridos com sucesso no banco de dados!")

    except mysql.connector.Error as error:
        print("Erro ao inserir dados no banco de dados:", error)

    finally:
        # Fechar conexão com o banco de dados, se estiver aberta
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("Conexão com o banco de dados encerrada.")

# Diretório onde os arquivos JSON estão localizados
json_directory = 'DIRETÓRIO_DA_PASTA_DE_JSONS'

# Nome da tabela a ser atualizada
table_name = 'NOME_DA_TABELA_DA_DATABASE'

while True:
    # Encontrar o arquivo JSON mais recente no diretório
    latest_json = find_latest_json(json_directory)

    if latest_json:
        # Caminho completo do arquivo JSON mais recente
        json_file_path = os.path.join(json_directory, latest_json)

        # Chamar a função para inserir os dados no banco de dados e fazer backup da tabela antiga
        insert_data_from_json(json_file_path, table_name)
    else:
        print("Nenhum arquivo JSON encontrado no diretório.")

    # Aguardar 5 segundos antes de verificar novamente
    time.sleep(5)


# In[ ]:




