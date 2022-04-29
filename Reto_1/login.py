#Módulos
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


options = Options()
# Se adiciona el directorio caché para el webdriver de Chrome
options.add_argument("--user-data-dir=C:/Users/camil/OneDrive/Escritorio/Automation/UserData")

# Se adicionan otras opciones para evitar posibles errores
options.page_load_strategy = 'normal'
options.add_experimental_option('excludeSwitches', ['enable-logging'])

#driver = webdriver.Chrome(executable_path='C:/Users/camil/Documents/TalenPitch/chromedriver.exe', options=options)
#driver.maximize_window()
#driver.get("https://web.whatsapp.com/")