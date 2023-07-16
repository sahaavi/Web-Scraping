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

def get_tweet(element):
    """
    This function scrapes data of tweets. 
    It returns a list with username, tweet text, reply, retweet and like
    """
    try:
        user = element.find_element_by_xpath(".//span[contains(text(), '@')]").text  # there are more than 1 but we pick the first
        text = element.find_element_by_xpath(".//div[@lang]").text
        reply_count = element.find_element_by_xpath(".//div[@data-testid='reply']").text
        retweet_count = element.find_element_by_xpath(".//div[@data-testid='retweet']").text
        like_count = element.find_element_by_xpath(".//div[@data-testid='like']").text
        tweets_data = [user, text, reply_count, retweet_count, like_count]
    except:
        tweets_data = ['NA', 'NA', 'NA', 'NA', 'NA']
    return tweets_data

# locating username and password inputs and sending text to the inputs

# username
username = driver.find_element_by_xpath('//input[@autocomplete ="username"]')
# username.send_keys("username")  # Write Email Here
username.send_keys(os.environ.get("TWITTER_USER"))

time.sleep(5)  # using this to make the action slower and more human like

# locating and clicking on "Next" button
next_button = driver.find_element_by_xpath('//div[@role="button"]//span[text()="Next"]')
next_button.click()

# password
password = driver.find_element_by_xpath('//input[@autocomplete ="current-password"]')
# password.send_keys("password")  # Write Password Here
password.send_keys(os.environ.get("TWITTER_PASS"))

time.sleep(5)  # using this to make the action slower and more human like

# locating land clicking on login button
login_button = driver.find_element_by_xpath('//div[@role="button"]//span[text()="Log in"]')
login_button.click()

# Initializing storage
user_data = []
text_data = []
reply_data = []
retweet_data = []
like_data = []

print("Scraping tweets...")

# getting all the tweet cards/boxes listed in a single page
tweets = WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.XPATH, "//article[@role='article']")))
# looping through the tweets list
for tweet in tweets:
    tweet_list = get_tweet(tweet)  # calling the function get_tweet to scrape data of the tweets list
    user_data.append(tweet_list[0])  # appending the first element of tweet_list (user)
    text_data.append(" ".join(tweet_list[1].split()))  # appending the second element of tweet_list (text)
    reply_data.append(tweet_list[2])
    retweet_data.append(tweet_list[3])
    like_data.append(tweet_list[4])

print("Scraping done!")
time.sleep(20)
driver.quit() # close chrome driver

tweets_df = pd.DataFrame({'user': user_data, 'tweet_text': text_data, 'reply_count': reply_data, 'retweet_count': retweet_data, 'like_count': like_data})
tweets_df.to_csv('tweets.csv', index=False) # save dataframe to csv file

print(tweets_df.head())
