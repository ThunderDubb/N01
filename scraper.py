from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time
import json

# Ścieżka do ChromeDriver
chrome_driver_path = 'chromedriver.exe'

# Konfiguracja usługi ChromeDriver
service = Service(executable_path=chrome_driver_path)

# Konfiguracja przeglądarki
driver = webdriver.Chrome(service=service)

# Przejdź do strony meczu
driver.get('https://n01darts.com/n01/league/n01_view.html?tmid=t_KcSD_1414_rr_0_bQoQ_gcqN')

# Poczekaj na załadowanie strony
time.sleep(5)

# Pobierz dane z XHR
xhr_url = 'https://tk2-228-23746.vs.sakura.ne.jp/n01/tournament/n01_user_t.php?cmd=match_view&sid='
driver.get(xhr_url)
time.sleep(5)

# Pobierz dane JSON
response = driver.page_source
data = json.loads(response)

# Zapisz dane JSON do pliku
with open('matches.json', 'w') as json_file, open('matches.json', 'w') as json_file:
    json.dump(data, json_file, indent=4)

driver.quit()
print("Dane zostały zapisane do pliku matches.json")
