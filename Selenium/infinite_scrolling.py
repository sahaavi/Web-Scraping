from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
import os

web = "https://twitter.com/i/flow/login"
path = 'C:/chromedriver_win32/chromedriver.exe'
driver = webdriver.Chrome(path)
driver.get(web)
driver.maximize_window()

# wait of 10 seconds to let the page load the content
driver.implicitly_wait(6) # this time might vary depending on your computer

# locating username and password inputs and sending text to the inputs

# username
username = driver.find_element_by_xpath('//input[@autocomplete ="username"]')
# username.send_keys("username")  # Write Email Here
username.send_keys(os.environ.get("TWITTER_USER"))

time.sleep(3)  # using this to make the action slower and more human like

# locating and clicking on "Next" button
next_button = driver.find_element_by_xpath('//div[@role="button"]//span[text()="Next"]')
next_button.click()

# password
password = driver.find_element_by_xpath('//input[@autocomplete ="current-password"]')
# password.send_keys("password")  # Write Password Here
password.send_keys(os.environ.get("TWITTER_PASS"))

time.sleep(3)  # using this to make the action slower and more human like

# locating land clicking on login button
login_button = driver.find_element_by_xpath('//div[@role="button"]//span[text()="Log in"]')
login_button.click()

# click on explore button
explore_button = driver.find_element_by_xpath('//a[@aria-label="Search and explore"]')
explore_button.click()

# type in the search bar
search_bar = driver.find_element_by_xpath('//input[@aria-label="Search query"]')
search_bar.send_keys("@avisheksaha123")

time.sleep(3)  # using this to make the action slower and more human like

# click on the first result
first_result = driver.find_element_by_xpath('//span[contains(text(), "Avishek Saha")]')
first_result.click()

# Get the initial scroll height
last_height = driver.execute_script("return document.body.scrollHeight")
while True:
    # Scroll down to bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    # Wait to load page
    time.sleep(5)
    # Calculate new scroll height and compare it with last scroll height
    new_height = driver.execute_script("return document.body.scrollHeight")
    print(new_height)
    if new_height == last_height:  # if the new and last height are equal, it means that there isn't any new page to load, so we stop scrolling
        break
    else:
        last_height = new_height

driver.quit()