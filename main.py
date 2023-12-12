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
    else:
        print("Check cloud name")
    
def countCloud(cloudName):

    try:
        #scrapping from pracuj
        quantityPracuj = countPracuj(cloudName, driver)

        #scrapping from just join
        numberJoin = countJust(cloudName, driver)
        #scrapping from NFJ 
        quantityNFJ = countNFJCloud(cloudName, driver)

        #scrapping from protocol
        numberProtocol = countProtocol(cloudName, driver)
        #offerSum
        quantityAll = int(quantityPracuj) + int(numberJoin) + int(quantityNFJ) + int(numberProtocol)
        print(f"Sum offer is: {quantityAll}")
        driver.quit()
    finally:
        driver.quit()

def countPracuj(cloudName, driver):
    words = cloudName.split()
    if len(words) > 1:   
        search_query = '%20'.join(words)
        driver.get(f"https://it.pracuj.pl/praca/{search_query};kw")
    else:
        driver.get(f"https://it.pracuj.pl/praca/{cloudName};kw")

        # Oczekiwanie na element zawierający liczbę ofert pracy
    elementPracuj = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CLASS_NAME, "core_c11srdo1"))
    )
    quantityPracuj = elementPracuj.text
    print(f"The number of offers for {cloudName} in Pracuj.pl is: {quantityPracuj}")

    return quantityPracuj

def countJust(cloudName, driver):
    words = cloudName.split()
    if len(words) > 1:   
        search_query = '+'.join(words)
        driver.get(f"https://justjoin.it/?keyword={search_query}")
    else:
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

    return numberJoin

def countNFJCloud(cloudName, driver):
    if( cloudName == "ibm cloud") or (cloudName == "oracle cloud") \
    or (cloudName.lower() == "microsoft azure") or (cloudName.lower() == "ms azure") \
    or (cloudName.lower() == "amazon web services") or (cloudName.lower() == "google cloud platform") or (cloudName.lower() == "google cloud"):
        quantityNFJ = 0
        print("Not key word for this webiste")

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

def countProtocol(cloudName, driver):
    if( cloudName == "ibm cloud") or (cloudName == "oracle cloud") or (cloudName.lower() == "ms azure"):
        numberProtocol = 0
        print("Not key word for this webiste")
        return numberProtocol == 0
    else:
        driver.get(f"https://theprotocol.it/filtry/{cloudName};t")
        elementProtocl = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, "su6nd6p"))
        )
        quantityProtocol = re.search(r'(\d{1,3}(?:\s\d{3})*)', elementProtocl.text)
        if quantityProtocol:
            numberProtocol = quantityProtocol.group(1)
            numberProtocol = numberProtocol.replace(" ", "")
            cloudName = cloudName.replace("+", " ")
            print(f"The number of offers for {cloudName} in theProtocol is: {numberProtocol}")
        else:
            print("No valid number found in the text.")

        return numberProtocol
        
choiceCloud()

