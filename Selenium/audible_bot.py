from selenium import webdriver
import pandas as pd

web = "https://www.audible.ca/search"
path = 'C:/chromedriver_win32/chromedriver.exe'
driver = webdriver.Chrome(path)
driver.get(web)
driver.maximize_window()

# Add implicit wait
driver.implicitly_wait(10)  # Wait up to 10 seconds for elements to be found

# Locating the box that contains all the audiobooks listed in the page
container = driver.find_element_by_class_name('adbl-impression-container ')

# Getting all the audiobooks listed (the "/" gives immediate child nodes)
products = container.find_elements_by_xpath('.//li[contains(@class, "productListItem")]')

# Initializing storage
book_title = []
book_author = []
book_narrator = []
book_length = []
release_date = []
language = []
regular_price = []

print("Scraping books...")

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

print("Scrape done!")

driver.quit() # close chrome driver

books_df = pd.DataFrame({'Title': book_title, 'Author': book_author, 'Narrator': book_narrator, 'Length': book_length, 'Release Date': release_date, 'Language': language, 'Regular Price': regular_price})
books_df.to_csv('audible_books.csv', index=False) # save dataframe to csv file

print(books_df.head())