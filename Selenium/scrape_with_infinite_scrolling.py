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
        tweet_id_element = element.find_element_by_xpath(".//div[starts-with(@id, 'id__') and (@data-testid='tweetText')]")
        tweet_id = tweet_id_element.get_attribute('id').replace('id__', '')
        tweets_data = [user, text, reply_count, retweet_count, like_count, tweet_id]
    except Exception as e:
        tweets_data = ['NA', 'NA', 'NA', 'NA', 'NA', 'NA']
        print(e)
    return tweets_data

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

# Initializing storage
user_data = []
text_data = []
reply_data = []
retweet_data = []
like_data = []
tweet_ids = set()
tweet_ids_list = []

print("Scraping tweets...")

scrolling = True
while scrolling:
    # getting all the tweet cards/boxes listed in a single page
    tweets = WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.XPATH, "//article[@role='article']")))
    print(len(tweets))
    # looping through the tweets list
    for tweet in tweets[-15:]: # you can change this number with the number of tweets in a website || NOTE: ONLY THOSE LOADED IN THE last page will be considered while those from previous page will be forgotten (example: scroll all the way down and then try to find an @username that it's on top --> it won't find it)
        tweet_list = get_tweet(tweet)  # calling the function get_tweet to scrape data of the tweets list
        if tweet_list[5] not in tweet_ids:
            user_data.append(tweet_list[0])  # appending the first element of tweet_list (user)
            text_data.append(" ".join(tweet_list[1].split()))  # appending the second element of tweet_list (text)
            reply_data.append(tweet_list[2])
            retweet_data.append(tweet_list[3])
            like_data.append(tweet_list[4])
            tweet_ids.add(tweet_list[5])
            tweet_ids_list.append(tweet_list[5])

    # Get the initial scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # Wait to load page
        time.sleep(5)
        # Calculate new scroll height and compare it with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        # this will scroll infinite times [most probably no end]
        # if new_height == last_height:  # if the new and last height are equal, it means that there isn't any new page to load, so we stop scrolling
        #     scrolling = False
        #     break
        # get the data of first 50 tweets
        if len(tweet_ids) > 50:
            scrolling = False
            break
        else:
            last_height = new_height
            break

print("Scraping done!")
time.sleep(3)
driver.quit() # close chrome driver

tweets_df = pd.DataFrame({'user': user_data, 'tweet_text': text_data, 'reply_count': reply_data, 'retweet_count': retweet_data, 'like_count': like_data, 'tweet_id': tweet_ids_list})
tweets_df.to_csv('tweets_infinite_scrolling.csv', index=False) # save dataframe to csv file

print(tweets_df.head())
