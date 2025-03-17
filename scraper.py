from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import json

# Konfiguracja opcji Chrome
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

# Konfiguracja przeglądarki z użyciem Selenium Manager
driver = webdriver.Chrome(options=chrome_options)

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

# Zapisz odpowiedź do pliku tekstowego
with open('response.txt', 'w') as text_file:
    text_file.write(response)

# Spróbuj zdekodować dane JSON
try:
    data = json.loads(response)
    # Zapisz dane JSON do pliku
    with open('matches.json', 'w') as json_file:
        json.dump(data, json_file, indent=4)
    print("Dane zostały zapisane do pliku matches.json")
except json.JSONDecodeError:
    print("Błąd dekodowania JSON: Odpowiedź nie jest poprawnym JSON")

driver.quit()
