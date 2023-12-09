

#Check python version

#python3 --version
#pip3 --version

#pip3 install selenium --user
#pip3 install -U selenium
#pip3 install webdriver-manager

#curl https://files.pythonhosted.org/packages/ed/9c/9030520bf6ff0b4c98988448a93c04fcbd5b13cd9520074d8ed53569ccfe/selenium-3.141.0.tar.gz > selenium.tar.gz
#tar -xzvf selenium.tar.gz
#cd selenium-3.141.0 dà errore
#python3

import pandas as pd
import numpy as np
import selenium 
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

#1) download chromedriver 
#2) put chromedriver.exe file inside the following path folder 
#For example:
#driver=webdriver.Chrome(executable_path=r"/Users/chris/selenium-3.141.0/selenium/webdriver/chrome/chromedriver")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))


datain='2023-03-30'
dataout='2023-03-31'
nadults = '4'
params = '&checkin='+ datain
params = params + '&checkout='+ dataout
params = params + '&group_adults='+nadults
params = params + '&no_rooms=1'
params = params + '&group_children=0'
#Set ages
#params = params + '&age=2'


url = "http://www.booking.com/searchresults.it.html?ss=Castelnuovo+del+Garda"+params

driver.get(url)
#prices
prices=driver.find_elements(By.XPATH, "//span[@class='fcab3ed991 fbd1d3018c e729ed5ab6']")

prezzi=[]
for price in prices:
    prezzi.append(re.findall(r'[\d]+[..\d]+', str(price.text)))  #togliere simbolo euro dal prezzo


prezzi=sum(prezzi,[])
prezzi2=[ float(i)*1000 if '.' in i  else float(i) for i in prezzi ]
np.quantile(prezzi2,0.25)  #problema con 1.076





#hotel names
names=driver.find_elements(By.XPATH, "//div[@class='fcab3ed991 a23c043802']")
nomi=[]
for name in names:
    nomi.append(name.text)


score = driver.find_elements(By.XPATH, "//div[@class='b5cd09854e d10a6220b4']")
rating=[]
for i in score:
    rating.append(i.text)



#Create output df 

df = pd.DataFrame()
df['Denominazione'] = nomi
df['PrezzoEuro']= prezzi
df['Rating']=rating
df['Check-in']=datain
df['Check-out']=dataout
df['Nadulti']=nadults

