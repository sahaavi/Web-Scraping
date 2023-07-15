from selenium import webdriver
import pandas as pd
from selenium.webdriver.support.ui import Select
import time

website = "https://www.adamchoi.co.uk/overs/detailed" # website to scrape
path = "C:/chromedriver_win32/chromedriver.exe" # path to chromedriver.exe
driver = webdriver.Chrome(path) # setup chrome driver
driver.get(website) # open website

# Add implicit wait
driver.implicitly_wait(10)  # Wait up to 10 seconds for elements to be found

# remember if you use single quotes inside for attribute value, use double quotes outside for the whole xpath or vice versa
all_matches_button = driver.find_element_by_xpath("//label[@analytics-event='All matches']") # find element by xpath
all_matches_button.click() # click on the element

dropdown = Select(driver.find_element_by_id('country')) # find dropdown element by id
dropdown.select_by_visible_text('Argentina') # select dropdown option by visible text


# time.sleep(5) # wait for 5 seconds for the page to load after selecting dropdown option

matches = driver.find_elements_by_tag_name('tr') # find all elements by tr tag name 

date = []
home_team = []
score = []
away_team = []

print("Scraping matches...")
# loop through all matches and append data to lists
for match in matches: 
    date.append(match.find_element_by_xpath('./td[1]').text)
    home_team.append(match.find_element_by_xpath('./td[2]').text)
    score.append(match.find_element_by_xpath('./td[3]').text)
    away_team.append(match.find_element_by_xpath('./td[4]').text)

print("Scrape done!")

driver.quit() # close chrome driver

matches_df = pd.DataFrame({'Date': date, 'Home Team': home_team, 'Score': score, 'Away Team': away_team})
matches_df.to_csv('argentina_matches.csv', index=False) # save dataframe to csv file

print(matches_df.head())