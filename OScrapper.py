#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import os
import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup

# Especifique o caminho para o executável do ChromeDriver
chromedriver_path = 'chromedriver.exe'  # Substitua pelo caminho correto

# Opções do Chrome para evitar detecção como bot
options = webdriver.ChromeOptions()
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("excludeSwitches", ["enable-automation"])

# URL da página de login
login_url = 'URL_DA_PÁGINA_DE_LOGIN'

# Credenciais de login
username = 'LOGIN'
password = 'SENHA'

# URL da página que contém as informações após o login
url = 'URL_DA_PÁGINA_ALVO_PARA_SCRAPPING'

# Função para realizar o scraping e salvar os dados em um arquivo JSON
def scrape_and_save_data(driver):
    # Atualizar a página para garantir que os dados estejam atualizados
    driver.refresh()

    # Aguarde a página carregar completamente após a atualização
    time.sleep(10)
    
    # Extrair informações da página atual
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    table = soup.find_all('table')[1]  # Ajuste o índice conforme necessário para selecionar a tabela correta
    os_column_data = table.find_all('tr')  # Remova o index [1] para pegar todas as linhas

    # Verifique se há pelo menos uma linha na tabela antes de tentar acessar
    if os_column_data:
        # Crie uma lista para armazenar os dados
        data_list = []
        for row in os_column_data:
            row_data = row.find_all('td')
            if len(row_data) >= 9:  # Garante que há dados suficientes na linha
                os_number = row_data[0].text.strip()  # Número da OS
                client_name = row_data[1].text.strip()  # Nome do cliente
                status = row_data[5].text.strip()  # Status da OS
                entry_date = row_data[6].text.strip()  # Data de entrada
                completion_date = row_data[7].text.strip()  # Data de finalização
                equipment = row_data[8].text.strip()  # Equipamento
                
                # Adicionar os dados filtrados à lista
                data_list.append([os_number, client_name, status, entry_date, completion_date, equipment])

        # Crie o diretório 'NOME_DA_PASTA_DOS_JSONS' se não existir
        os.makedirs('NOME_DA_PASTA_DOS_JSONS', exist_ok=True)

        # Salvar os dados em um arquivo JSON com o nome "OS_LIST_data_hora.json" na pasta 'OS_LIST_JSONS'
        filename = f"DIRETÓRIO_DA_PASTA_DOS_JSONS/NOME_DA_LISTA_DE_OS_{time.strftime('%Y-%m-%d_%H-%M-%S')}.json"
        with open(filename, 'w') as json_file:
            json.dump(data_list, json_file, ensure_ascii=False)

    else:
        print("Nenhuma linha de dados encontrada na tabela.")

# Crie um serviço do Chrome
chrome_service = webdriver.chrome.service.Service(chromedriver_path)
chrome_service.start()

try:
    # Crie um driver do Chrome com as opções configuradas
    driver = webdriver.Chrome(service=chrome_service, options=options)

    # Acesse a página de login
    driver.get(login_url)

    # Preencha os campos de login
    driver.find_element(By.NAME, "login").send_keys(username)
    driver.find_element(By.NAME, "senha").send_keys(password)

    # Pressione Enter para enviar o formulário de login
    driver.find_element(By.NAME, "senha").send_keys(Keys.RETURN)

    # Aguarde a página carregar completamente
    time.sleep(5)

    while True:
        # Acesse a página desejada com a quantidade de resultados por página definida como 2000
        driver.get(url + '&length=2000')
        
        # Chame a função para realizar o scraping e salvar os dados
        scrape_and_save_data(driver)
        
        # Print que foi realizado o scrapping
        print('Scrapping realizado com sucesso. ' + time.strftime('%Y-%m-%d_%H-%M-%S'))

        # Aguarde 5 segundos antes de realizar o próximo scraping
        time.sleep(5)

except KeyboardInterrupt:
    print("Interrupção do usuário recebida, fechando o navegador.")
    driver.quit()
finally:
    # Pare o serviço do Chrome ao finalizar
    chrome_service.stop()

