#  1) Написать программу, которая собирает входящие письма из своего
#  или тестового почтового ящика и сложить данные о письмах в базу
#  данных (от кого, дата отправки, тема письма, текст письма полный)

from lxml import html
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions



driver = webdriver.Chrome()
driver.get('https://mail.ru/')
assert 'Mail.ru: почта, поиск в интернете, новости, игры' in driver.title

mail_log = driver.find_element_by_id('mailbox:login')
mail_log.send_keys('ostudentova')

select_dom = Select(driver.find_element_by_id('mailbox:domain'))
select_dom.select_by_visible_text('@list.ru')

button = driver.find_element_by_xpath("//*[@value='Ввести пароль']")
button.click()

submit_pass = driver.find_element_by_id('mailbox:password')
submit_pass.send_keys('SomeWord!')
#button = driver.find_element_by_xpath("//*[@value='Ввести пароль']")
button.click()

#
letters_url = driver.find_elements_by_xpath('//div[@class="dataset__items"]/a[contains(@class,"js-letter-list-item")]')

# extracring address from each collected element-tag <a>,
for url in letters_url:
    letter = url.get_attribute('href')
    print(letter)
# request to the extracted address
    lettr = requests.get(letter,
                          headers={'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
                                                 " AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36"}).text
# forming html-page
    letter_page = html.fromstring(lettr)
#parsing the page with xpath
    topic = letter_page.xpath('//h2[@class="thread__subject"]/text').extract()
    sender_address = letter_page.xpath('//span[@class="letter__contact-item"]/@title').extract()
    sender_name = letter_page.xpath('//span[@class="letter__contact-item"]/text').extract()
    letter_date = letter_page.xpath('//div[@class="letter__date"]/text').extract()
    print(topic)
    print(sender_address)
    print(sender_name)
    print(letter_date)



#button <//dev[@class='dataset__items'//a[contains(@class, "js-letter-list-item"/@href
#//span[@class="letter__contact-item"]/@title
#//div[@class="attachlist__header"]//a/@href
# rel="history" href="https://e.mail.ru/thread/2:33c54b33c6c63415:0/"
# class="js-href b-datalist__item__link" data-name="transaction_link"
# data-subject="Заказ № 8043 1477 подтверждение отправки."
# data-title="Лабиринт <shop@labirintmail.ru>">

#xpath //a[contains(@class, 'js-letter-list-item')]/@href
# //h2[@class='thread__subject']/text
#//div[@class='letter__author']/span[@class='letter__contact-item']/@title
# //div[@class='letter-body']


driver.quit()