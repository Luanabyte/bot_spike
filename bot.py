import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import requests

# URL base do Looker Studio (com as extensões de página específicas)
# Substitua pelas URLs exatas da página 2 e página 3 do seu relatório
URL_PAGINA_2 = "https://datastudio.google.com/u/0/reporting/381b9841-a980-41cb-9a7d-a7216bad7518/page/p_2k2ig0fg1d" # Ajuste se necessário para a pág 2
URL_PAGINA_3 = "https://datastudio.google.com/u/0/reporting/381b9841-a980-41cb-9a7d-a7216bad7518/page/p_OUTRA_PAGINA_3" # Cole aqui o link da pág 3

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
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(options=chrome_options)

    try:
        # --- PÁGINA 2 ---
        url_p2 = f"{URL_PAGINA_2}&nav=0"
        print(f"Acessando a Página 2...")
        driver.get(url_p2)
        time.sleep(15) # Aguarda carregar os dados
        
        path_p2 = "pagina_2.png"
        driver.save_screenshot(path_p2)
        enviar_para_seatalk(path_p2, "Central Flow - Página 2")

        # --- PÁGINA 3 ---
        url_p3 = f"{URL_PAGINA_3}&nav=0"
        print(f"Acessando a Página 3...")
        driver.get(url_p3)
        time.sleep(15) # Aguarda carregar os dados
        
        path_p3 = "pagina_3.png"
        driver.save_screenshot(path_p3)
        enviar_para_seatalk(path_p3, "Central Flow - Página 3")

    except Exception as e:
        print(f"Ocorreu um erro: {str(e)}")
        driver.save_screenshot("erro_captura.png")
        raise e

    finally:
        driver.quit()

if __name__ == "__main__":
    if not SEATALK_WEBHOOK_URL:
        raise ValueError("A variável SEATALK_WEBHOOK_URL não está configurada.")
    rodar_automacao()
