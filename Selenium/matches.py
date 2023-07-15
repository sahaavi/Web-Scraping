from selenium import webdriver
import pandas as pd

website = "https://www.adamchoi.co.uk/overs/detailed" # website to scrape
path = "C:/chromedriver_win32/chromedriver.exe" # path to chromedriver.exe
driver = webdriver.Chrome(path) # setup chrome driver
driver.get(website) # open website

# Add implicit wait
driver.implicitly_wait(10)  # Wait up to 10 seconds for elements to be found

# remember if you use single quotes inside for attribute value, use double quotes outside for the whole xpath or vice versa
all_matches_button = driver.find_element_by_xpath("//label[@analytics-event='All matches']") # find element by xpath
all_matches_button.click() # click on the element

matches = driver.find_elements_by_tag_name('tr') # find all elements by tr tag name 
# print(matches)

# for match in matches: # loop through all matches
#     print(match.text) # print text of each match

date = []
home_team = []
score = []
away_team = []

print("Scraping matches...")
# loop through all matches and append data to lists
for match in matches: 
    date.append(match.find_element_by_xpath('./td[1]').text)

    # home = match.find_element_by_xpath('./td[2]').text
    # home_team.append(home)
    # print(home)
    
    home_team.append(match.find_element_by_xpath('./td[2]').text)
    score.append(match.find_element_by_xpath('./td[3]').text)
    away_team.append(match.find_element_by_xpath('./td[4]').text)

print("Scrape done!")

driver.quit() # close chrome driver

matches_df = pd.DataFrame({'Date': date, 'Home Team': home_team, 'Score': score, 'Away Team': away_team})
matches_df.to_csv('matches.csv', index=False) # save dataframe to csv file

print(matches_df.head())