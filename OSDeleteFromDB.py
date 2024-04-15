#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import mysql.connector

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

    # Query para deletar todos os dados da tabela
    sql = "DELETE FROM NOME_DA_TABELA_DA_DATABASE"

    # Executar a query
    cursor.execute(sql)

    # Confirmar as alterações
    connection.commit()
    print("Dados deletados com sucesso da tabela!")

except mysql.connector.Error as error:
    print("Erro ao deletar dados da tabela:", error)

finally:
    # Fechar conexão com o banco de dados, se estiver aberta
    if 'connection' in locals() and connection.is_connected():
        cursor.close()
        connection.close()
        print("Conexão com o banco de dados encerrada.")

