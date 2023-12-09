from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
import re

options = Options() 
options.add_argument("-headless") 
driver = webdriver.Firefox(options=options) 
def choiceCloud():
    cloudName = input("Enter the name of the cloud service provider whose number of offers you want to know: ")
    if (cloudName.lower() == "aws") or (cloudName.lower() == "amazon web services") or \
    (cloudName.lower() == "amazon") or (cloudName.lower() == "google cloud") or \
    (cloudName.lower() == "azure") or (cloudName.lower() == "microsoft azure") or \
    (cloudName.lower() == "ms azure") or (cloudName.lower() == "google cloud platform") or \
    (cloudName.lower() == "gcp") or (cloudName.lower() == "ibm cloud") or (cloudName.lower() == "oracle cloud"):
        countCloud(cloudName.lower())
    
def countCloud(cloudName):

    try:
        driver.get(f"https://it.pracuj.pl/praca/{cloudName};kw")
        elementPracuj = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, "core_c11srdo1"))
        )
        quantityAWS = elementPracuj.text
        print(f"The number of offers for {cloudName} in Pracuj.pl is: {quantityAWS}")
        
        cloudName = cloudName.replace(" ", "+")
        driver.get(f"https://justjoin.it/?keyword={cloudName}")
        elementJoin = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, "MuiTab-iconWrapper"))
        )
        quantityJoin = re.search(r'(\d{1,3}(?:\s\d{3})*)', elementJoin.text)
        if quantityJoin:
            numberJoin = quantityJoin.group(1)
            numberJoin = numberJoin.replace(" ", "")
            cloudName = cloudName.replace("+", " ")
            print(f"The number of offers for {cloudName} in Just Join is: {numberJoin}")
        else:
            print("No valid number found in the text.")
            
        quantityNFJ = countNFJCloud(cloudName, driver)
        
        driver.get(f"https://theprotocol.it/filtry/{cloudName};t")
        quantityAll = int(quantityAWS) + int(numberJoin) + quantityNFJ
        print(f"Sum offer is: {quantityAll}")
        driver.quit()
    finally:
        driver.quit()

def countNFJCloud(cloudName, driver):
        if( cloudName == "ibm cloud") or (cloudName == "oracle cloud") or (cloudName == "oracle cloud") or (cloudName.lower() == "microsoft azure"):
            zmienna1, zmienna2 = cloudName.split()
            driver.get(f"https://nofluffjobs.com/pl/{zmienna2}?criteria=requirement={zmienna1}")
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CLASS_NAME, "list-container"))
            )
            link_elements = driver.find_elements(By.CLASS_NAME, "list-container a")
            quantityNFJ = len(link_elements)
            print(f"The number of offers for {cloudName} in No Fluff Jobs is: {quantityNFJ}")

            return quantityNFJ
        else:
            driver.get(f"https://nofluffjobs.com/pl/{cloudName}")
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CLASS_NAME, "list-container"))
            )
            link_elements = driver.find_elements(By.CLASS_NAME, "list-container a")
            quantityNFJ = len(link_elements)
            print(f"The number of offers for {cloudName} in No Fluff Jobs is: {quantityNFJ}")

            return quantityNFJ
    
                
choiceCloud()

