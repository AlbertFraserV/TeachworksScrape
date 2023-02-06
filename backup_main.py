from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.ui import Select
from selenium import webdriver
from bs4 import BeautifulSoup

from datetime import datetime
import time

from database import Database

cur = Database()
import os
from dotenv import load_dotenv
load_dotenv()

USER = os.getenv('USERNAME')
PASSWORD = os.environ.get('PASS')
TEST_PREP_WAGE = float(os.environ.get('TESTPREP'))
SCHOOL_WAGE = float(os.environ.get('SCHOOL'))
TAX_RATE = float(os.environ.get('TAX'))/100
time_format = "%I:%M %p"

driver = webdriver.Firefox(executable_path = '/usr/local/bin/geckodriver')
driver.set_window_size(1120, 550)

url = "http://homeworkhelperstutoring.teachworks.com"
driver.get(url)
time.sleep(5)

user_name_box = driver.find_element("xpath", '//*[@id="user_email"]')
password_box = driver.find_element("xpath", '//*[@id="user_password"]')
submit_button = driver.find_element("xpath", "/html/body/main/div/div[1]/div/div[2]/form/div[3]/div/button")

user_name_box.send_keys(USER)
password_box.send_keys(PASSWORD)
time.sleep(1)
submit_button.click()

#Get to correct page
calendar_button = driver.find_element("xpath", '/html/body/header/div/nav/ul[1]/li[2]/a')
calendar_button.click()
time.sleep(1)
calendar_list_button = driver.find_element("xpath", "/html/body/header/div/nav/ul[1]/li[2]/ul/li[4]/a")
calendar_list_button.click()
time.sleep(1)

#Pull only the current date
today = driver.find_element("xpath",  '//*[@id="start"]').get_dom_attribute('value')
end_date = driver.find_element("xpath",  '//*[@id="end"]')
end_date.send_keys(today)
time.sleep(1)
driver.find_element("xpath", "//body").click()
time.sleep(1)
submit_button = driver.find_element("xpath", '/html/body/main/div/div/div[2]/div/div[2]/form/div[4]/div/input[3]')
submit_button.click()
time.sleep(5)

#Get student info
student_page = driver.page_source
soup = BeautifulSoup(student_page, 'html.parser')
students = soup.find('tbody', attrs={'class':'calendar-list'}).find_all('tr')[2:]

working_hours = {'test_prep': 0, 'school': 0}
for lesson in students:
    time_range = lesson.find_all('td')[0].text
    time_range = time_range.split(" - ")
    lesson_type = lesson.find_all('td')[6].text
    start_time = datetime.strptime(time_range[0], time_format)
    end_time = datetime.strptime(time_range[1], time_format)
    total_time = abs(end_time - start_time).seconds/3600
    if 'Test Preparation' in lesson_type:
        working_hours['test_prep'] += total_time
    else:
        working_hours['school'] += total_time

wages = (working_hours['test_prep']*TEST_PREP_WAGE + working_hours['school']*SCHOOL_WAGE)*(1-TAX_RATE)
print(f"You made {str(round(wages,2))} after taxes today!")
sql = f"INSERT INTO daily_pay (daily_pay_date, daily_pay) VALUES('{today}', {wages});"
print(sql)
cur.commit(sql)
driver.close()


