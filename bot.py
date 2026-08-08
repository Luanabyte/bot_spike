import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests

# Variáveis injetadas pelo ambiente do GitHub Actions
LOOKER_URL = os.getenv("LOOKER_URL")
SEATALK_WEBHOOK_URL = os.getenv("SEATALK_WEBHOOK_URL")

def enviar_para_seatalk(imagem_path, legenda):
    print(f"Enviando '{legenda}' para o SeaTalk...")
    with open(imagem_path, "rb") as img:
        files = {"file": img}
        data = {"caption": legenda}
        response = requests.post(SEATALK_WEBHOOK_URL, files=files, data=data)
        if response.status_code == 200:
            print(f"Sucesso ao enviar: {legenda}")
        else:
            print(f"Erro ao enviar {legenda}: {response.text}")

def rodar_automacao():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(options=chrome_options)

    try:
        # Adiciona o parâmetro &nav=0 para ocultar a barra superior e deixar o print limpo
        url_base = f"{LOOKER_URL}&nav=0"
        print("Acessando o Looker Studio...")
        driver.get(url_base)
        
        # Tempo de espera generoso para garantir que o dashboard carregue os dados da Pág 1
        time.sleep(15)

        # --- PÁGINA 1 ---
        print("Salvando print da Página 1...")
        path_p1 = "pagina_1.png"
        driver.save_screenshot(path_p1)
        enviar_para_seatalk(path_p1, "Relatório - Página 1")

        # --- NAVEGAR PARA A PÁGINA 2 ---
        print("Navegando para a Página 2...")
        # Localiza e clica no botão de próxima página do Looker Studio
        botao_proxima = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-label*='Next page'], button[aria-label*='Próxima página'], div[aria-label*='Next page']"))
        )
        botao_proxima.click()
        
        # Aguarda a renderização dos dados da Página 2
        time.sleep(10)

        # --- PÁGINA 2 ---
        print("Salvando print da Página 2...")
        path_p2 = "pagina_2.png"
        driver.save_screenshot(path_p2)
        enviar_para_seatalk(path_p2, "Relatório - Página 2")

    finally:
        driver.quit()

if __name__ == "__main__":
    if not LOOKER_URL or not SEATALK_WEBHOOK_URL:
        raise ValueError("As variáveis de ambiente LOOKER_URL e SEATALK_WEBHOOK_URL precisam estar configuradas.")
    rodar_automacao()
