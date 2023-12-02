from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time


def upgrades_available(drv):
    x_path = '//*[@id="store"]'
    stores = [drv.find_element(By.XPATH, value=f'{x_path}/div[{i}]') for i in range(1, 10)]
    for shop in stores:
        if shop.get_attribute("class") != "grayed":
            return True
    return False


def buy_upgrade(drv):
    x_path = '//*[@id="store"]'
    stores = [drv.find_element(By.XPATH, value=f'{x_path}/div[{i}]') for i in range(1, 10)]

    affordable = [shop for shop in stores if shop.get_attribute("class") != "grayed"]
    prices = [int(i.find_element(By.CSS_SELECTOR, value="b").text.split("-")[1].split()[0]) for i in affordable]

    most_expensive = max(prices)
    buy = affordable[prices.index(most_expensive)]
    return buy


edge_options = webdriver.EdgeOptions()
edge_options.add_experimental_option("detach", True)
edge_options.add_argument("--start-maximized")

driver = webdriver.Edge(options=edge_options)
driver.get("https://orteil.dashnet.org/experiments/cookie/")
cookie = driver.find_element(By.CSS_SELECTOR, value="#cookie")

five_seconds = time.time() + 5
five_minutes = time.time() + 60 * 5

while time.time() < five_minutes:
    cookie.click()

    if time.time() >= five_seconds:
        if upgrades_available(driver):
            upgrade = buy_upgrade(driver)
            upgrade.click()
        five_seconds = time.time() + 5
    pass

cookies_per_second = float(driver.find_element(By.ID, value="cps").text.split(":")[1].split()[0])
print(f"You have achieved {cookies_per_second} cookies per second!")
