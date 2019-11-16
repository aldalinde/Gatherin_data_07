#  1) Написать программу, которая собирает входящие письма из своего
#  или тестового почтового ящика и сложить данные о письмах в базу
#  данных (от кого, дата отправки, тема письма, текст письма полный)

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
#from selenium.webdriver.support.ui import WebDriverWait
#from selenium.webdriver.support import expected_conditions
from selenium.webdriver.chrome.options import Options
from pymongo import MongoClient
import time


chrome_options = Options()
chrome_options.add_argument('start-maximized')
# chrome_options.add_argument('--headless')

driver = webdriver.Chrome(options=chrome_options)

# driver = webdriver.Chrome()
driver.get('https://mail.ru/')
assert 'Mail.ru: почта, поиск в интернете, новости, игры' in driver.title

# entering mailbox name
mail_log = driver.find_element_by_id('mailbox:login')
mail_log.send_keys('ostudentova')

# choosing domain
select_dom = Select(driver.find_element_by_id('mailbox:domain'))
select_dom.select_by_visible_text('@list.ru')

# entering password
button = driver.find_element_by_xpath("//input[@value='Ввести пароль']")
button.click()

submit_pass = driver.find_element_by_id('mailbox:password')
submit_pass.send_keys('SomeWord!')
submit_pass.send_keys(Keys.RETURN)

time.sleep(5)
assert 'Входящие - Почта Mail.ru' in driver.title

# saving to a list variable the elements each containing a letter from a list of letters
testing_title = driver.find_elements_by_class_name('js-letter-list-item')

# forming a Mongo database
client = MongoClient('localhost', 27017)
db = client['mail_db']
mail_db = db.mailru_db

# an empty list variable for collecting dictionaries of letter-items
letter_list = []
# parsing each letter-page and returning to the main page number of times according to the number of letters
for i in range(len(testing_title)):
    try:
        time.sleep(5)
        # each time finding a clickable element, containing the next letter in the list
        button = driver.find_elements_by_class_name('js-letter-list-item')[i]
        button.click()
        time.sleep(3)
        # an empty dictionary to fill with data on each letter
        letter_dict = {}

        topic = driver.find_element_by_xpath('//h2[@class="thread__subject"]').text
        letter_dict['topic'] = topic

        sender_address_element = driver.find_element_by_xpath('//span[@class="letter__contact-item"]')
        sender_address = sender_address_element.get_attribute('title')
        letter_dict['sender_address'] = sender_address

        sender_name = sender_address_element.text
        letter_dict['sender_name'] = sender_name

        letter_date = driver.find_element_by_xpath('//div[@class="letter__date"]').text
        letter_dict['letter_date'] = letter_date

        # the element with the letter contents
        letter_contents = driver.find_element_by_class_name("js-readmsg-msg")
        file_name = f'letter_mailru_{i}'
 #       with open(file_name, mode='wb') as f:
 #           f.write(letter_contents)
        letter_dict['file_name'] = file_name

        # forming a list of all dictionaries available for adding to MongoDB
        letter_list.append(letter_dict)
# back to main page
        driver.back()

    except Exception:
        print("Element is not clickable")
        pass
# adding items list to MongoDB
mail_db.insert_many(letter_list)



driver.quit()