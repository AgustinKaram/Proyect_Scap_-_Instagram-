from os import link
import pandas as pd
from typing import Dict
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import time

#Especifico donde estra el driver para comunicarme con el navegador. Puede ser cualquiera, en mi caso Chrome
# opciones = webdriver.ChromeOptions()
# opciones.add_argument("---use-gl")
# opciones.add_argument("--enable-webgl")
# opciones.add_argument("--disable-software-rasterizer")
# driver = webdriver.Chrome('C:/Users/Usuario/Desktop/Proyecto Scrapping/chromedriver.exe',options=opciones)
driver = webdriver.Chrome(executable_path='C:\\Users\\Usuario\\Desktop\\Proyecto Scrapping\\chromedriver.exe')

#Voy a la pagina que quiero scrapear
driver.get("http://www.instagram.com")


#le digo donde voy a colocar el login ( html input ). Tambien considero el tiempo de carga.
username = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='username']")))
password = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='password']")))

#Limpio el input por las dudas y coloco mi usuario
username.clear()
username.send_keys("kozta_marta")
password.clear()
password.send_keys("ikFn2yd5QMDJu2N")

#Le doy click en ingresar
button = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))).click()

#saltamos las alertas
time.sleep(5)
alert = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Ahora no")]'))).click()
alert2 = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Ahora no")]'))).click()

#especificamos el html donde esta el buscador de instagram
searchbox = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Busca']")))
searchbox.clear()

#buscamos el '#' que deseamos
keyword = "#lechevegetal"
searchbox.send_keys(keyword)
time.sleep(5) # esperamos 5''
my_link = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, '/" + keyword[1:] + "/')]")))
my_link.click()

# scroll to the bottom of the page
n_scrolls = 10
for j in range(0, n_scrolls):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(5)

#me traigo todos los links del hashtag
posts = []
links = driver.find_elements_by_tag_name('a')

#este for va a llenar una lista con todos los link o post dentro del # vegano
for link in links:
    post = link.get_attribute('href')
    if "/p/" in post:
        posts.append(post)
    else:
        continue    

pd.DataFrame(posts).to_csv("posts_#lechevegana.csv", index=False)

#con este for voy a sacar las fechas de cada publicacion
dates=[]
for post in posts:
    time.sleep(5)
    #le digo al driver que vaya a cada pagina 
    driver.get(post)
    #y me busque las fechas de las publicaciones
    date = driver.find_element_by_xpath("//time[@class='_1o9PC Nzb55']")
    date = date.get_attribute("datetime")
    dates.append(date)

dicc = {
    'link_a_publicacione':posts,
    'fecha_publicacion':dates
}

pd.DataFrame(dicc).to_csv("scrap_#lechevegetal_instagram.csv", index=False)