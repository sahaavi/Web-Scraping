from selenium import webdriver
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

time.sleep(6)  # using this to make the action slower and more human like

# locating and clicking on "Next" button
next_button = driver.find_element_by_xpath('//div[@role="button"]//span[text()="Next"]')
next_button.click()

# password
password = driver.find_element_by_xpath('//input[@autocomplete ="current-password"]')
# password.send_keys("password")  # Write Password Here
password.send_keys(os.environ.get("TWITTER_PASS"))

time.sleep(6)  # using this to make the action slower and more human like

# locating land clicking on login button
login_button = driver.find_element_by_xpath('//div[@role="button"]//span[text()="Log in"]')
login_button.click()

time.sleep(30)

# closing driver
driver.quit()