from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import pyautogui
import time
import pyperclip
import re

import requests
from bs4 import BeautifulSoup

import pandas as pd

url = 'https://abrange.app/#/login'

driver = webdriver.Chrome()
driver.get(url)
driver.maximize_window()
time.sleep(10)

html = driver.page_source

soup = BeautifulSoup(html, "html.parser")

# Procurar todos os orçamentos na tela inicial
orcamentos = soup.find_all("div", class_="q-item__label")

# Processar os resultados
dados = []
for orcamento in orcamentos:
    texto = orcamento.get_text(strip=True)  # Obter texto sem espaços desnecessários
    dados.append(texto)

orcamentos_filtrados = [item for item in dados if item.strip().startswith("OR")]

orcamentos_filtrados = orcamentos_filtrados[1:2]

# Lista para armazenar os dados
dados_completos = []

# Iterar sobre cada orçamento
for i, orcamento in enumerate(orcamentos_filtrados):
    try:
        # Usando XPath para localizar o orçamento pelo texto contido no <div>
        orcamento = driver.find_element(By.XPATH, f"//div[contains(text(), '{orcamento}')]")
        
        # Clicar no orçamento atual
        orcamento.click()
        print(f"Clicado no orçamento: {orcamento}")
        time.sleep(3)  # Aguarda o carregamento da página do orçamento

        # Extrair o HTML da página atual
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")

        # Encontrar todas as linhas de informações detalhadas
        linhas = soup.find_all("div", class_="row border-u text-body1")

        # Extrair dados do orçamento em formato de dicionário
        dados = {}
        for linha in linhas:
            chave = linha.find("div", class_="col-6").text.strip()
            valor = linha.find_all("div", class_="col-6")[1].text.strip()
            dados[chave] = valor
        
        # Adicionar os dados extraídos à lista principal
        dados_completos.append(dados)
                     
        # Voltar para a tela anterior
        pyautogui.click(347, 250, duration=0.8)
        time.sleep(3)  # Aguarda o carregamento da tela inicial
    except Exception as e:
        print(f"Erro ao processar orçamento {i + 1}: {e}")

# Criar um DataFrame com todos os dados
df = pd.DataFrame(dados_completos)

# Salvar os dados em um arquivo CSV
df.to_csv("tabela_orcamentos_completa.csv", index=False, encoding="utf-8")

# Fechar o navegador
driver.quit()

# Exibir a tabela criada
print("Tabela final:")
print(df)











numero = driver.find_element(By.CSS_SELECTOR, "div.col-9 b").text.strip()
descricao = driver.find_element(By.CSS_SELECTOR, "div.col-9").text.replace(numero, "").strip()
quantidade = driver.find_element(By.CSS_SELECTOR, "div.col-3.text-center").text.strip()


elementos = driver.find_elements(By.CSS_SELECTOR, "div.text-h6")
valores_list = []
for i in range(2, len(elementos), 1):
    elementos[i].click()
    time.sleep(2)
    valores = driver.find_elements(By.CSS_SELECTOR, "div.col-3.text-right")
    for v in valores:
        valor = v.text.strip()
        valores_list.append(valor)



