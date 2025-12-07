#! python3

import re
import json
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.edge.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


#   A random project that crawls the Sothebysrealty Seattle location's website ----->
#   Scrapes and saves every real esate agents information.
#   Got the idea from a job posting on UpWork.com, and made it for practice.

sleep = time.sleep

def initialize_webdriver(driver_path):
    service = Service(driver_path)
    options = EdgeOptions()
    options.add_argument("--headless")
    return webdriver.Edge(service=service, options=options)

def references(html):
    return BeautifulSoup(html, 'html5lib')


def navigate_to_page(browser, url):
    browser.get(url)


def wait_for_element(browser, by, value, timeout=10):
    try:
        element = WebDriverWait(browser, timeout).until(EC.presence_of_element_located((by, value)))
        return element
    except TimeoutException:
        print(f"Element not found: {by} {value}")
        return None
    

def new_page(browser, html):
    html = browser.page_source
    soup = references(html)
    
    pages = []
    page_numbers = []

    links = soup.find_all(href=re.compile("-pg"))
    for link in links:
        clicked = link.get("href")
        pages.append(clicked)
        for char in clicked:
            if char.isdigit():
                page_numbers.append(int(char))
        return pages


def page_count(pages):
    page_numbers = []
    for char in pages:
        if char.isdigit():
            page_numbers.append(int(char))

        x = min(page_numbers, default="empty")
        y = max(page_numbers, default="empty")
        return list(range(x, y))


def extract_data(browser):
    html = browser.page_source
    soup = references(html)

    agents = []

    sleep(0.5)

    info_IDs = soup.find_all("div", class_=re.compile(r"card-container"))
    
    for match in info_IDs:
        ids = [line.strip() for line in match.get_text(separator="\n").split("\n") if line.strip()]
        print(info_IDs)
        
        if not ids:
            continue
        
        agent_data = {
            "name": ids[0] if len(ids) > 0 else 'N/A',
            "position": ids[1] if len(ids) > 1 else 'N/A',
            "company": ids[2] if len(ids) > 2 else 'N/A',
            "address": " ".join(ids[3:6]) if len(ids) > 5 else 'N/A',
        }

        contact_info = {}
        for line in info_IDs:
            if "M:" in line:
                contact_info["CONTACT M"] = line.split("M:")[1].strip()
            if "O:" in line:
                contact_info["CONTACT O"] = line.split("O:")[1].strip()
            
        agent_data.update(contact_info)        
        agents.append(agent_data)
    
    if agents:
        with open("C:/Users/atath/sothebysrealty.json", "a", encoding="utf-8") as f:
            json.dump(agents, f, indent=4)
        print(f"Saved {len(agents)} agents to JSON.")
    
    return len(agents)
    

def full_extraction(browser, url):
    navigate_to_page(browser, url)
    sleep(2)
    html = browser.page_source
    soup = references(html)
    links = soup.find_all(href=re.compile("-pg"))
    extract_data(browser)

    sleep(1)

    pg_numbers = re.findall(r'\d*0', (str(links)))
    end_page = max(pg_numbers)
    count = list(range(1, int(end_page)))

    total_pages = []

    for x in count:
        new_url = f"{url}/{x}-pg"
        total_pages.append(new_url)
    for page in total_pages:
        navigate_to_page(browser, page)
        sleep(1)

        extract_data(browser)


def main():
    driver_path = 'C:/Users/atath/Downloads/edgedriver_win64/msedgedriver.exe'
    url = "https://www.sothebysrealty.com/eng/associates/seattle-wa-usa"  # /{\d}-pg

    browser = initialize_webdriver(driver_path)
    try:
        full_extraction(browser, url)
    except Exception as e:
        print(f"Unable To Complete Due To Error {e}")
    finally:
        browser.quit()

if __name__ == "__main__":
    main()
