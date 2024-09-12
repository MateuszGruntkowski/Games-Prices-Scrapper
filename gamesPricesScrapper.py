from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

def configuration(url):
    driver = webdriver.Chrome()
    driver.get(url)
    return driver

def acceptPolicy(driver, shop):
    if shop == 'MEDIA_EXPERT' or shop == 'RTV_EURO_AGD':
        try:
            accept_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))
            )
        except Exception as e:
            print('Something went wrong ', e)

    if shop == 'XKOM':
        try:
            time.sleep(1)
            accept_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "parts__AcceptButton-sc-22bd9b2d-9"))
            )
        except Exception as e:
            print('Something went wrong ', e)

    accept_button.click()

def wait_for_elements(driver, timeout=10):
    WebDriverWait(driver, timeout).until(
        lambda d: d.execute_script('return document.readyState') == 'complete'
    )

def findElements(price_class, title_class, driver, data_list, shop):
    soup = bs(driver.page_source, features="html.parser")
    wait_for_elements(driver, timeout=10) 
    wait_for_elements(driver, timeout=10)
    prices = soup.find_all(class_=price_class)
    titles = soup.find_all(class_=title_class)
    for price, title in zip(prices, titles):
        data_list.append([price.text, title.text.strip('\n ' ''), shop])

def write_to_txt(data, shop):
    with open(f'{shop}.txt', 'w', encoding='utf-8') as f:
        for line in data:
            f.write(f'{line[1]} {line[0]} \n')

def write_to_excel(data, shop):
    df = pd.DataFrame(data, columns=['Price', 'Name', 'Shop'])
    df.to_excel(f'{shop}.xlsx', index=False)

def addShopToOffers(shop):
    for offer in shop:
        all_offers.append(offer)

def scrapData(price_class, title_class, shop, driver):
    data_list = []

    if shop == 'RTV_EURO_AGD':   
        while True:
            try:
                link = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[data-aut-id="show-more-products-button"]'))
                )
                link = driver.find_element(By.CSS_SELECTOR, 'a[data-aut-id="show-more-products-button"]')
                time.sleep(1.5) # time.sleep necessary because scrapper was bugging during scraping
                link.click()
            except:
                break
        findElements(price_class, title_class, driver, data_list, shop='RTV_EURO_AGD')
                    
    elif shop == 'MEDIA_EXPERT':
        while True:
            findElements(price_class, title_class, driver, data_list, shop='MEDIA_EXPERT')
            try:
                link = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CLASS_NAME, 'icon-next'))
                )
                link = driver.find_element(By.CLASS_NAME, 'icon-next')
                # time.sleep is not necessary for this site
                link.click()
            except:
                break
    
    elif shop == 'XKOM':
        last_page_element = driver.find_element(By.CLASS_NAME, 'parts__PagesTotal-sc-d8adfe33-2')
        last_page_number = int(last_page_element.text.split()[1])

        current_page = 1
        while current_page <= last_page_number:
            findElements(price_class, title_class, driver, data_list, shop='X-KOM')
            try:
                link = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CLASS_NAME, 'parts__NextButton-sc-d8adfe33-3'))
                )
                link = driver.find_element(By.CLASS_NAME, 'parts__NextButton-sc-d8adfe33-3')
                # time.sleep is not necessary for this site
                link.click()
            except:
                break
            current_page+=1
            
    return data_list

def run(url, price_class, title_class, shop):
    driver = configuration(url)
    acceptPolicy(driver, shop)
    data = scrapData(price_class, title_class, shop, driver)
    driver.quit()
    return data   

if __name__ == "__main__":
    all_offers = []
    
    RTV_EURO_AGD = run('https://www.euro.com.pl/gry-playstation-5.bhtml', 'parted-price-total', 'product-medium-box-intro__link', 'RTV_EURO_AGD')
    MEDIA_EXPERT = run('https://www.mediaexpert.pl/gaming/gry/gry-ps5', 'whole', 'is-animate ui-link', 'MEDIA_EXPERT')
    XKOM = run('https://www.x-kom.pl/g-7/c/3106-gry-na-playstation-5.html', 'parts__Price-sc-6e255ce0-0', 'parts__Title-sc-6e280ffa-9', 'XKOM')
    
    addShopToOffers(MEDIA_EXPERT)
    addShopToOffers(RTV_EURO_AGD)
    addShopToOffers(XKOM)
    all_offers.sort(key = lambda x: x[2])

    write_to_excel(all_offers, 'ALL_OFFERS')
    write_to_txt(all_offers, 'ALL_OFFERS')
    