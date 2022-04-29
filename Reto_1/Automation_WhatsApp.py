# Módulos
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import pyperclip
import time

import os
import login
import pandas as pd
import itertools
import datetime


def wp_automation():
    """
    Proceso de automatización de envío de mensajes por WhatsApp
    """

    options = login.options # Se guardan el atributo de opciones para el webdriver
    driver = webdriver.Chrome(executable_path='C:/Users/camil/Documents/TalenPitch/chromedriver.exe', options=options)
    driver.maximize_window()
    driver.get("https://web.whatsapp.com/") #Webdriver abre página web

    df = pd.read_pickle('News_whatsapp.pkl') #Carga del dataframe

    with open('groups.txt', 'r', encoding='utf8') as f:
            groups = [group.strip() for group in f.readlines()]      # Extracción de nombres de los grupos que se buscaran en WA
        
    #communities = list(df['Comunidad'].unique())

    # Generación de mensaje a partir de muestra del dataframe
    sample = df.sample(5)
        
    msg = f'''¡Hola! \U0001F44B, a continuación te mostramos cinco noticias que te podrían interesar: \n
            1) {list(sample['Titulos'])[0]} : {list(sample['Descripciones'])[0]} \n
            {list(sample['Links'])[0]} \n
            2) {list(sample['Titulos'])[1]} : {list(sample['Descripciones'])[1]} \n
            {list(sample['Links'])[1]} \n
            3) {list(sample['Titulos'])[2]} : {list(sample['Descripciones'])[2]} \n
            {list(sample['Links'])[2]} \n
            4) {list(sample['Titulos'])[3]} : {list(sample['Descripciones'])[3]} \n
            {list(sample['Links'])[3]} \n
            5) {list(sample['Titulos'])[4]} : {list(sample['Descripciones'])[4]} \n
            {list(sample['Links'])[4]}\n
            Ten un bonito día, chauuu. \U0001F4A9
            '''

    # Se borran las noticias extraídas por la muestra para evitar repetir noticias en el futuro
    df.drop(sample.index, inplace=True)
    df.to_pickle("./News_whatsapp.pkl")

    # Para cada grupo se le envía el mensaje, si se desea un envío distinto por comunidad se recomienda el uso de tuplas en el ciclo y filtro del df.
    for group in groups:
            # Busqueda de contenido para ingresar nombre de grupo y al grupo en si
            search_xpath = '//div[@contenteditable="true"][@data-tab="3"]'

            search_box = WebDriverWait(driver, 500).until(
                    EC.presence_of_element_located((By.XPATH, search_xpath))
            )

            search_box.clear()

            time.sleep(1)

            pyperclip.copy(group) #Grupo

            search_box.send_keys(Keys.SHIFT, Keys.INSERT)  # Keys.CONTROL + "v"

            time.sleep(2)

            group_xpath = f'//span[@title="{group}"]'
            group_title = driver.find_element(By.XPATH, group_xpath)

            group_title.click()

            time.sleep(1)

            # Envío de mensaje
            input_xpath = '//div[@contenteditable="true"][@data-tab="10"]'
            input_box = driver.find_element(By.XPATH, input_xpath)

            pyperclip.copy(msg)
            input_box.send_keys(Keys.SHIFT, Keys.INSERT)  # Keys.CONTROL + "v"
            input_box.send_keys(Keys.ENTER)

            time.sleep(2)


    time.sleep(5)
    driver.close()

# Condicional para envío de mensaje automático solo entre semana y el presente mes
if (datetime.datetime.now().weekday() < 5 and datetime.datetime.now().month==4):
        wp_automation()

quit()