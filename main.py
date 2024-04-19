from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementClickInterceptedException, WebDriverException
import time
import re
import sqlite3
import subprocess
import os
import json

options = Options() 
options.add_argument("-headless") 
driver = webdriver.Firefox(options=options) 

def choiceCloud():
    cloud_providers = ["aws", "azure", "gcp", "ibm cloud", "oracle cloud"]
    website_providers = ["pracuj", "justjoin", "nfj", "theprotocol"]
    results = {
        "offerswebsite": {wp: {cp: 0 for cp in cloud_providers} for wp in website_providers},
        "cloudprovider": {cp: {wp: 0 for wp in website_providers} for cp in cloud_providers}
    }

    for cloud_provider in cloud_providers:
        for website_provider in website_providers:
            count = countOffers(cloud_provider, website_provider, driver) 
            results["offerswebsite"][website_provider][cloud_provider] += count
            results["cloudprovider"][cloud_provider][website_provider] += count

    for key in results["offerswebsite"]:
        results["offerswebsite"][key]["all"] = sum(results["offerswebsite"][key].values())

    for key in results["cloudprovider"]:
        results["cloudprovider"][key]["all"] = sum(results["cloudprovider"][key].values())

    with open('jobs_offers.json', 'w') as f:
        json.dump(results, f, indent=4)
    driver.close()

def countOffers(cloud_provider, website_provider, driver):
    count = 0
    try:
        if website_provider == "pracuj":
            words = cloud_provider.split()
            if len(words) > 1:   
                search_query = '%20'.join(words)
                driver.get(f"https://it.pracuj.pl/praca/{search_query};kw")
            else:
                driver.get(f"https://it.pracuj.pl/praca/{cloud_provider};kw")
            try:
                elementPracuj = WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "core_c11srdo1"))
                )
                count = int(elementPracuj.text.replace(" ", ""))
            except TimeoutException:
                return 0

        elif website_provider == "justjoin":
            words = cloud_provider.split()
            if len(words) > 1:   
                search_query = '+'.join(words)
                driver.get(f"https://justjoin.it/?keyword={search_query}")
            else:
                driver.get(f"https://justjoin.it/?keyword={cloud_provider}")
            try:
                elementJoin = WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "MuiTab-iconWrapper"))
                )
                count = int(re.search(r'(\d+)', elementJoin.text.replace(" ", "")).group(0))
            except TimeoutException:
                return 0

        elif website_provider == "nfj":
            if cloud_provider.lower() in ["ibm cloud", "oracle cloud"]:   
                return 0
            else: 
                try:
                    driver.get(f"https://nofluffjobs.com/pl/jobs/{cloud_provider}")

                    while True:
                        try:
                            load_more_button = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'Pokaż kolejne oferty')]"))
                            )

                            driver.execute_script("arguments[0].click();", load_more_button)
                            time.sleep(2)
                            driver.find_element(By.XPATH, "//button[contains(text(), 'Pokaż kolejne oferty')]")

                        except (NoSuchElementException, TimeoutException):
                            break
                        except ElementClickInterceptedException:
                            print("Another element received the click, trying again...")
                            time.sleep(2)

                    offer_elements = driver.find_elements(By.CSS_SELECTOR, ".list-container > a")
                    count = len(offer_elements)
                except WebDriverException as e:
                    print(f"WebDriver error: {e}")
                return 0  
            
        elif website_provider == "theprotocol":
            if cloud_provider.lower() in ["oracle cloud"]:
                return 0
            else:
                words = cloud_provider.split()
                if len(words) > 1:   
                    search_query = '-'.join(words)
                    driver.get(f"https://theprotocol.it/filtry/{search_query};t")
                else:
                    driver.get(f"https://theprotocol.it/filtry/{cloud_provider};t")

                elementProtocol = WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "su6nd6p"))
                )
                quantityProtocol = re.search(r'(\d{1,3}(?:\s\d{3})*)', elementProtocol.text)
                if quantityProtocol:
                    numberProtocol = quantityProtocol.group(1)
                    numberProtocol = numberProtocol.replace(" ", "")
                    cloud_provider = cloud_provider.replace("+", " ")

                count = int(re.search(r'(\d+)', elementProtocol.text.split()[0]).group(0))

    except (NoSuchElementException, TimeoutException):
        print(f"Nie znaleziono ofert dla {cloud_provider} na {website_provider}")
    except Exception as e:
        print(f"Wystąpił błąd: {e}")
    finally:
        return count
    
if __name__ == "__main__":
    while True: 
        choice = input("Do you want to directly run app? (YES/NO): ").strip().lower()
        if choice == 'yes':
            if os.path.exists('jobs_offers.json'):
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
            print("Web scrapping will be done again")
            choiceCloud()
            subprocess.run(["python", "app.py"])
            break  
        else:
            print("Type 'yes' or 'no'.")

