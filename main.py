from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
import re
import sqlite3
import subprocess
import os

options = Options() 
options.add_argument("-headless") 
driver = webdriver.Firefox(options=options) 

def choiceCloud():
    cloud_providers = ["aws", "azure", "gcp", "ibm cloud", "oracle cloud"]
    website_providers = ["pracuj", "justjoin", "nfj", "theprotocol"]
    for cloud_provider in cloud_providers:
        for website_provider in website_providers:
            quantityPracuj = countPracuj(cloud_provider, driver)
            numberJoin = countJust(cloud_provider, driver)
            quantityNFJ = countNFJCloud(cloud_provider, driver)
            numberProtocol = countProtocol(cloud_provider, driver)
            quantityAll = int(quantityPracuj) + int(numberJoin) + int(quantityNFJ) + int(numberProtocol)
        
            countCloud(cloud_provider, quantityPracuj, numberJoin, quantityNFJ, numberProtocol, quantityAll)
    
            countForWebsite(website_provider, cloud_provider, quantityPracuj, numberJoin, quantityNFJ, numberProtocol)


def countCloud(cloudName, quantityPracuj, numberJoin, quantityNFJ, numberProtocol, quantityAll):
        conn = sqlite3.connect('jobs_offers.db')
        cursor = conn.cursor()
        cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{cloudName}'")
        table_exists = cursor.fetchone()

        if table_exists:
            update_query = f'''
            UPDATE "{cloudName}"
                SET quantityPracuj = ?,
                numberJoin = ?,
                quantityNFJ = ?,
                numberProtocol = ?,
                quantityAll = ?
            WHERE id = ?
            '''
            cursor.execute(update_query, (quantityPracuj, numberJoin, quantityNFJ, numberProtocol, quantityAll, 1))
        else:
            create_query = f'''
            CREATE TABLE "{cloudName}" (
            id INTEGER PRIMARY KEY,
            quantityPracuj INTEGER,
            numberJoin INTEGER,
            quantityNFJ INTEGER,
            numberProtocol INTEGER,
            quantityAll INTEGER
            )
            '''
            cursor.execute(create_query)

            insert_query = f'''
            INSERT INTO "{cloudName}" (quantityPracuj, numberJoin, quantityNFJ, numberProtocol, quantityAll)
            VALUES (?, ?, ?, ?, ?)
            '''
            cursor.execute(insert_query, (quantityPracuj, numberJoin, quantityNFJ, numberProtocol, quantityAll))
        conn.commit()
        conn.close()

def countForWebsite(website_provider, cloud_provider, quantityPracuj, numberJoin, quantityNFJ, numberProtocol):
    if website_provider == "pracuj":
        updateJobPortalTable(website_provider, cloud_provider, quantityPracuj)
    elif website_provider == "justjoin":
        updateJobPortalTable(website_provider, cloud_provider, numberJoin)
    elif website_provider == "nfj":
        updateJobPortalTable(website_provider, cloud_provider, quantityNFJ)
    elif website_provider == "theprotocol":
        updateJobPortalTable(website_provider, cloud_provider, numberProtocol)

def updateJobPortalTable(website_provider, cloud_provider, quantity):
    conn = sqlite3.connect('jobs_offers.db')
    cursor = conn.cursor()
    table_name = f"{website_provider}"
    cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'")
    if not cursor.fetchone():
        cursor.execute(f'''
            CREATE TABLE '{table_name}' (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                portal_name TEXT UNIQUE,
                quantity INTEGER
            )
        ''')
    cursor.execute(f"SELECT quantity FROM '{table_name}' WHERE portal_name = ?", (cloud_provider,))
    row = cursor.fetchone()
    if row:

        cursor.execute(f'''
            UPDATE '{table_name}'
            SET quantity = quantity + ?
            WHERE portal_name = ?
        ''', (quantity, cloud_provider))
    else:

        cursor.execute(f'''
            INSERT INTO '{table_name}' (portal_name, quantity)
            VALUES (?, ?)
        ''', (cloud_provider, quantity))

    conn.commit()
    conn.close()

def countPracuj(cloudName, driver):
    words = cloudName.split()
    if len(words) > 1:   
        search_query = '%20'.join(words)
        driver.get(f"https://it.pracuj.pl/praca/{search_query};kw")
    else:
        driver.get(f"https://it.pracuj.pl/praca/{cloudName};kw")

    elementPracuj = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CLASS_NAME, "core_c11srdo1"))
    )
    quantityPracuj = elementPracuj.text

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
        
    return numberJoin

def countNFJCloud(cloudName, driver):
    if( cloudName == "ibm cloud") or (cloudName == "oracle cloud"):
        quantityNFJ = 0

        return quantityNFJ 
    else:
        driver.get(f"https://nofluffjobs.com/pl/{cloudName}")
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, "list-container"))
        )
        link_elements = driver.find_elements(By.CLASS_NAME, "list-container a")
        quantityNFJ = len(link_elements)

        return quantityNFJ 

def countProtocol(cloudName, driver):
    if( cloudName == "ibm cloud") or (cloudName == "oracle cloud"):
        numberProtocol = 0
        return numberProtocol
    
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
        return numberProtocol
    
if __name__ == "__main__":
    while True: 
        choice = input("Do you want to directly run app? (YES/NO): ").strip().lower()
        if choice == 'yes':
            if os.path.exists('jobs_offers.db'):
                try:
                    subprocess.run(["python", "app.py"])
                finally:
                    driver.quit()
                break 
            else:
                print("Database doesn't exist. First, web scraping will be done.")
                choiceCloud()
                subprocess.run(["python", "app.py"])
                break  
        elif choice == 'no':
            choiceCloud()
            subprocess.run(["python", "app.py"])
            break  
        else:
            print("Type 'yes' or 'no'.")

