# -*- coding: utf-8 -*-
"""
Created on Mon Feb  7 16:51:38 2022

@author: aplle
"""

import random
from time import sleep
from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import pandas as pd
from itertools import zip_longest

driver = webdriver.Chrome('./chromedriver.exe')
#abrimos la pagina
driver.get('https://www.olx.com.pe/lima_g4070680/autos_c378?filter=condition_eq_2%2Ccurrency_type_eq_USD')




#Todos los anuncios en una lista


boton = driver.find_element_by_xpath('//button[@data-aut-id="btnLoadMore"]')

for i in range(50):
    
    try:
        boton.click()
        sleep(random.uniform(8.0, 10.0))
        boton = driver.find_element_by_xpath('//button[@data-aut-id="btnLoadMore"]')
    except:
        break
   
htmltext = driver.page_source
#driver.quit()
# Parse HTML structure
soup = BeautifulSoup(htmltext, "lxml")
carros = []

for link in soup.find_all("a",class_='fhlkh'):
    valor = link.get('href')
    union = 'https://www.olx.com.pe'+valor
    carros.append(union)



diccionario = {'Marca':list(),'Año':list(),'Color':list(),'Modelo':list(),'Kilometraje':list(),'Combustible':list(),'Transmisión':list(),'Precio':list()}
key = diccionario.keys()

for carro in carros:
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[1])
    driver.get(carro)
    r = requests.get(carro)
    soup = BeautifulSoup(r.text, 'lxml')
    tit= soup.find_all('span',class_='_25oXN')
    val = soup.find_all('span',class_='_2vNpt')
    #listaP = list()
    
    #HALLAMOS EL PRECIO
    precios = driver.find_elements_by_class_name('_2wMiF')
    for precio in precios:
        precio = precio.find_element_by_xpath('.//span[@data-aut-id="itemPrice"]').text
        #istaP.append(precio)
        
   
        
    valores = list()
    for j in val:
        valores.append(j.text)
    titulos = list()
    for i in tit:
        titulos.append(i.text)
    d = dict(zip(titulos, valores))
    for i in titulos:
        for j in key:
            if(i==j):
                lista = diccionario[j]
                lista.append(d[i])
                diccionario[j]=lista
    lista2 = list()
    lista2 = diccionario['Precio']
    lista2.append(precio)
    diccionario['Precio'] = lista2
    
    
    
  
    
    driver.close()
    driver.switch_to.window(driver.window_handles[0])



fram = pd.DataFrame(zip_longest(*diccionario.values()), columns=diccionario)
#exportar data frame a csv
fram.to_csv('DATA_Carros.csv', index=False)
print(fram)           
                
              
    
    
        
    
        
    
    
    
    
 

#autos = driver.find_elements_by_xpath('//li[@data-aut-id="itemBox"]')
#links = driver.find_elements_by_css_selector(".fhlkh")
#Urls = [el.get_attribute("href") for el in links]

    
    

