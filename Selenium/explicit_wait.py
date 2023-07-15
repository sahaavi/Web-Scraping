from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pandas as pd
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Headless mode
options = Options()
options.headless = False # run chrome in headless mode [This time not using it as we want to see the browser in action]
# options.add_argument("window-size=1920x1080") # set a big window size, so all the data will be displayed
# [This time not using it as we want to see the browser in action]

web = "https://www.audible.ca/adblbestsellers"
path = 'C:/chromedriver_win32/chromedriver.exe'
driver = webdriver.Chrome(path, options=options) # add the "options" argument to make sure the headless mode is applied
driver.get(web)
driver.maximize_window() # maximize the window to make sure all the data will be displayed

# Add implicit wait
# driver.implicitly_wait(5)  # Wait up to 5 seconds for elements to be found

# Initializing storage
book_title = []
book_author = []
book_narrator = []
book_length = []
release_date = []
language = []
regular_price = []
web_page = []

# pagination = driver.find_element_by_xpath('//ul[contains(@class, "pagingElements")]')
pagination = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//ul[contains(@class, "pagingElements")]'))) # explicit wait
# pages = pagination.find_elements_by_tag_name('li')  # locating each page displayed in the pagination bar
pages = WebDriverWait(pagination, 5).until(EC.presence_of_all_elements_located((By.TAG_NAME, 'li')))  # explicit wait
last_page = int(pages[-2].text)  # getting the last page with negative indexing (starts from where the array ends)

current_page = 1 # strats scrapping from page 1

print("Scraping books...")

while current_page <= last_page:
    # implicit wait
    # time.sleep(3)  # let the page render correctly

    print(f"Scraping page {current_page} of {last_page}...")

    # Locating the box that contains all the audiobooks listed in the page
    # container = driver.find_element_by_class_name('adbl-impression-container ') # implicit wait menqioned above
    container = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'adbl-impression-container '))) # explicit wait

    # Getting all the audiobooks listed (the "/" gives immediate child nodes)
    # products = container.find_elements_by_xpath('.//li[contains(@class, "productListItem")]') # implicit wait menqioned above
    products = WebDriverWait(container, 5).until(EC.presence_of_all_elements_located((By.XPATH, './/li[contains(@class, "productListItem")]'))) # explicit wait
    # here used presence of all elements located, as we need to get all the elements, not just one element like the previous one

    # Looping through the products list (each "product" is an audiobook)
    for product in products:
        # We use "contains" to search for web elements that contain a particular text, so we avoid building long XPATH
        book_title.append(product.find_element_by_xpath('.//h3[contains(@class, "bc-heading")]').text)
        authorLabel = product.find_element_by_xpath('.//li[contains(@class, "authorLabel")]').text
        book_author.append(authorLabel.replace('Written by: ', ''))
        try:
            narratorLabel = product.find_element_by_xpath('.//li[contains(@class, "narratorLabel")]').text
            book_narrator.append(narratorLabel.replace('Narrated by: ', ''))
        except:
            book_narrator.append('NA')
        try:
            runtimeLabel = product.find_element_by_xpath('.//li[contains(@class, "runtimeLabel")]').text
            book_length.append(runtimeLabel.replace('Length: ', ''))
        except:
            book_length.append('NA')
        try:
            releaseDateLabel = product.find_element_by_xpath('.//li[contains(@class, "releaseDateLabel")]').text
            release_date.append(releaseDateLabel.replace('Release date: ', ''))
        except:
            release_date.append('NA')
        try:
            languageLabel = product.find_element_by_xpath('.//li[contains(@class, "languageLabel")]').text
            language.append(languageLabel.replace('Language: ', ''))
        except:
            language.append('NA')
        try:
            buybox_regular_price = product.find_element_by_xpath('.//p[contains(@class, "buybox-regular-price")]').text
            regular_price.append(buybox_regular_price.replace('Price: $', ''))
        except:
            regular_price.append('NA')
        
        web_page.append(current_page)

    # Clicking on the next page button
    try:
        next_page = driver.find_element_by_xpath('.//span[contains(@class, "nextButton")]')
        next_page.click()
    except:
        print(f"{current_page}Next page did not load!")
        pass

    current_page += 1 # increment the page number for the next iteration

print("Scrape done!")

driver.quit() # close chrome driver

books_df = pd.DataFrame({'Title': book_title, 'Author': book_author, 'Narrator': book_narrator, 'Length': book_length, 'Release Date': release_date, 'Language': language, 'Regular Price': regular_price, 'Web Page': web_page})
books_df.to_csv('audible_books_pagination_wait.csv', index=False) # save dataframe to csv file

print(books_df.head())