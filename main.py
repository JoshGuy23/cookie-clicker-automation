from selenium import webdriver
from selenium.webdriver.common.by import By
import time


def upgrades_available(drv):
    # This function checks if there are any upgrades available for purchase.
    # drv is the Selenium webdriver

    # Get the list of upgrades.
    x_path = '//*[@id="store"]'
    stores = [drv.find_element(By.XPATH, value=f'{x_path}/div[{i}]') for i in range(1, 10)]

    # If there is an upgrade without a class of 'grayed', return true. Otherwise, return false.
    # The 'grayed' class indicates that the upgrade isn't affordable.
    for item in stores:
        if item.get_attribute("class") != "grayed":
            return True
    return False


def buy_upgrade(drv):
    # This function finds the most expensive upgrade in the shop.
    # drv is the Selenium webdriver

    # Get the list of upgrades.
    x_path = '//*[@id="store"]'
    stores = [drv.find_element(By.XPATH, value=f'{x_path}/div[{i}]') for i in range(1, 10)]

    # Get the list of affordable items and their prices.
    affordable = [item for item in stores if item.get_attribute("class") != "grayed"]
    prices = [int(i.find_element(By.CSS_SELECTOR, value="b").text.split("-")[1].split()[0]) for i in affordable]

    # Find the most expensive affordable item and return it.
    most_expensive = max(prices)
    buy = affordable[prices.index(most_expensive)]
    return buy


# Set up the webdriver.
edge_options = webdriver.EdgeOptions()
edge_options.add_experimental_option("detach", True)
edge_options.add_argument("--start-maximized")
driver = webdriver.Edge(options=edge_options)

# Get the cookie element.
driver.get("https://orteil.dashnet.org/experiments/cookie/")
cookie = driver.find_element(By.CSS_SELECTOR, value="#cookie")

# Set the timer for five minutes as well as a 5-second timer.
five_seconds = time.time() + 5
five_minutes = time.time() + 60 * 5

# This portion runs while the five-minute timer is running.
while time.time() < five_minutes:
    # Click the cookie
    cookie.click()

    # After 5 seconds, check if there are any upgrades available.
    # If there are, get the most expensive upgrade and purchase it.
    # Always reset the five-second timer.
    if time.time() >= five_seconds:
        if upgrades_available(driver):
            upgrade = buy_upgrade(driver)
            upgrade.click()
        five_seconds = time.time() + 5

# Once the program stops clicking, get the current cookies per second stat.
cookies_per_second = float(driver.find_element(By.ID, value="cps").text.split(":")[1].split()[0])
print(f"You have achieved {cookies_per_second} cookies per second!")
