from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import requests
import time
import os

# 1️⃣ Ustawienia Selenium
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Tryb bez interfejsu
options.add_argument("--no-sandbox")  # Potrzebne na GitHub Actions
options.add_argument("--disable-dev-shm-usage")  # Unika błędów pamięci
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)


# 2️⃣ Otwórz stronę główną i pobierz SID
main_url = "https://n01darts.com/n01/league/n01_view.html?tmid=t_KcSD_1414_rr_0_bQoQ_gcqN"
driver.get(main_url)
time.sleep(3)

# logs = driver.get_log("performance")


sid_url = None
for log in logs:
    message = log["message"]
    if "match_view&sid=" in message:
        sid_url = message.split("https://tk2-228-23746.vs.sakura.ne.jp")[1].split('"')[0]
        sid_url = "https://tk2-228-23746.vs.sakura.ne.jp" + sid_url
        break

driver.quit()

# 3️⃣ Pobieranie JSON
if sid_url:
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(sid_url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        df = pd.json_normalize(data)  # Konwersja JSON → tabela

        # 4️⃣ Zapis CSV lokalnie
        file_name = "darts_data.csv"
        df.to_csv(file_name, index=False)
        print(f"Plik CSV zapisany jako {file_name}")

        # 5️⃣ (Opcjonalnie) Wysłanie do Google Drive
        from pydrive.auth import GoogleAuth
        from pydrive.drive import GoogleDrive
        
        gauth = GoogleAuth()
        gauth.LocalWebserverAuth()  # Autoryzacja Google Drive
        drive = GoogleDrive(gauth)

        file_drive = drive.CreateFile({'title': file_name})
        file_drive.SetContentFile(file_name)
        file_drive.Upload()
        print(f"Plik CSV został przesłany do Google Drive: {file_name}")
    else:
        print("Błąd pobierania JSON:", response.status_code)
else:
    print("Nie znaleziono `sid`!")
