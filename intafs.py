from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
import random

# Função para fazer login no Instagram
def login(driver, username, password):
    driver.get("https://www.instagram.com/accounts/login/")
    time.sleep(random.uniform(2, 4))  # Delay aleatório

    # Preencher campos de usuário e senha
    username_field = driver.find_element(By.NAME, "username")
    password_field = driver.find_element(By.NAME, "password")

    username_field.send_keys(username)
    password_field.send_keys(password)
    password_field.send_keys(Keys.RETURN)
    time.sleep(random.uniform(5, 7))  # Esperar o login ser concluído

# Função para seguir um usuário
def follow_user(driver, target_user):
    driver.get(f"https://www.instagram.com/{target_user}/")
    time.sleep(random.uniform(3, 5))

    try:
        # Clicar no botão "Seguir"
        follow_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Seguir')]")
        follow_button.click()
        print(f"Seguindo o usuário {target_user} com sucesso!")
    except Exception as e:
        print(f"Erro ao seguir o usuário {target_user}: {e}")
    time.sleep(random.uniform(2, 4))

# Função para fazer logout
def logout(driver):
    driver.get("https://www.instagram.com/accounts/logout/")
    time.sleep(random.uniform(3, 5))

# Função para carregar contas de um arquivo
def load_accounts(file_path):
    accounts = []
    with open(file_path, "r") as file:
        for line in file:
            username, password = line.strip().split(":")
            accounts.append({"username": username, "password": password})
    return accounts

# Função principal
def main():
    # Carregar contas do arquivo
    accounts = load_accounts("contas.txt")
    if not accounts:
        print("Nenhuma conta encontrada no arquivo 'contas.txt'.")
        return

    # Usuário alvo a ser seguido
    target_user = input("Digite o nome de usuário do perfil que deseja seguir: ")

    # Configuração do Chrome em modo headless
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Rodar sem interface gráfica
    chrome_options.add_argument("--disable-gpu")  # Desabilitar GPU
    chrome_options.add_argument("--no-sandbox")  # Necessário para Termux
    chrome_options.add_argument("--disable-dev-shm-usage")  # Evitar problemas de memória

    # Configuração do Selenium
    driver = webdriver.Chrome(options=chrome_options)
    driver.implicitly_wait(10)

    try:
        for i, account in enumerate(accounts):
            print(f"Processando conta {i + 1}/{len(accounts)}: {account['username']}")
            login(driver, account["username"], account["password"])
            follow_user(driver, target_user)
            logout(driver)

            # Delay aleatório entre contas para evitar detecção
            if i < len(accounts) - 1:
                delay = random.uniform(10, 20)  # Delay entre 10 e 20 segundos
                print(f"Aguardando {delay:.2f} segundos antes da próxima conta...")
                time.sleep(delay)
    except Exception as e:
        print(f"Erro durante a execução: {e}")
    finally:
        driver.quit()
        print("Processo concluído!")

if __name__ == "__main__":
    main()