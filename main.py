from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
import time 

option = Options()
option.headless = True

def choiceCloud():
    cloudName = input("Enter the name of the cloud service provider whose number of offers you want to know: ")
    if (cloudName.lower() == "aws") or (cloudName.lower() == "amazon web services") or (cloudName.lower() == "amazon"):
        countAws(cloudName.lower())
    elif (cloudName.lower() == "azure") or (cloudName.lower() == "microsoft azure"):
        countAzure(cloudName.lower())
    elif (cloudName.lower() == "google cloud") or (cloudName.lower() == "google cloud platform") or (cloudName.lower() == "gcp"):
        countGcp(cloudName.lower())
    elif (cloudName.lower() == "ibm cloud"):
        countIBM(cloudName.lower())
    elif (cloudName.lower() == "oracle cloud"):
        countOracle(cloudName.lower())
    
def countAws(cloudName):
    driver = webdriver.Firefox(options=option)
    driver.get(f"https://it.pracuj.pl/praca/{cloudName};kw")
    try:
        span_element = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, "core_c11srdo1"))
        )
        span_text = span_element.text
        print(f"The number of offers for {cloudName} is: {span_text}")
        driver.quit()
    finally:
        driver.quit()

def countAzure(cloudName):
    driver = webdriver.Firefox(options=option)
    driver.get(f"https://it.pracuj.pl/praca/{cloudName};kw")

    try:
        span_element = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, "core_c11srdo1"))
        )
        span_text = span_element.text
        print(f"The number of offers for {cloudName} is: {span_text}")
        driver.quit()
    finally:
        driver.quit()

def countGcp(cloudName):
    driver = webdriver.Firefox(options=option)
    driver.get(f"https://it.pracuj.pl/praca/{cloudName};kw")
    try:
        span_element = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, "core_c11srdo1"))
        )
        span_text = span_element.text
        print(f"The number of offers for {cloudName} is: {span_text}")
        driver.quit()
    finally:
        driver.quit()

def countIBM(cloudName):
    driver = webdriver.Firefox(options=option)
    driver.get(f"https://it.pracuj.pl/praca/{cloudName};kw")
    try:
        span_element = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, "core_c11srdo1"))
        )
        span_text = span_element.text
        print(f"The number of offers for {cloudName} is: {span_text}")
        driver.quit()
    finally:
        driver.quit()

def countOracle(cloudName):
    driver = webdriver.Firefox(options=option)
    driver.get(f"https://it.pracuj.pl/praca/{cloudName};kw")
    try:
        span_element = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, "core_c11srdo1"))
        )
        span_text = span_element.text
        print(f"The number of offers for {cloudName} is: {span_text}")
        driver.quit()
    finally:
        driver.quit()
                
choiceCloud()

