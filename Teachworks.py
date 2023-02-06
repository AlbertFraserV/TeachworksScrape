from selenium import webdriver
import time
from bs4 import BeautifulSoup
from datetime import datetime
import os
from dotenv import load_dotenv

class Teachworks:
    def __init__(self):
        load_dotenv()
        self.url = "http://homeworkhelperstutoring.teachworks.com"
        self.driver = webdriver.Firefox(executable_path = '/usr/local/bin/geckodriver')
        self.USER = os.getenv('USERNAME')
        self.PASSWORD = os.environ.get('PASS')
        self.TEST_PREP_WAGE = float(os.environ.get('TESTPREP'))
        self.SCHOOL_WAGE = float(os.environ.get('SCHOOL'))
        self.TAX_RATE = float(os.environ.get('TAX'))/100
        self.time_format = "%I:%M %p"

    def login(self):
        self.driver.get(self.url)
        time.sleep(5)

        user_name_box = self.driver.find_element("xpath", '//*[@id="user_email"]')
        password_box = self.driver.find_element("xpath", '//*[@id="user_password"]')
        submit_button = self.driver.find_element("xpath", "/html/body/main/div/div[1]/div/div[2]/form/div[3]/div/button")

        user_name_box.send_keys(self.USER)
        password_box.send_keys(self.PASSWORD)
        time.sleep(1)
        submit_button.click()
        time.sleep(2)

    def navigate_to_calendar_list(self):
        calendar_button = self.driver.find_element("xpath", '/html/body/header/div/nav/ul[1]/li[2]/a')
        calendar_button.click()
        time.sleep(1)
        calendar_list_button = self.driver.find_element("xpath", "/html/body/header/div/nav/ul[1]/li[2]/ul/li[4]/a")
        calendar_list_button.click()
        time.sleep(1)
        self.today = self.driver.find_element("xpath",  '//*[@id="start"]').get_dom_attribute('value')
        end_date = self.driver.find_element("xpath",  '//*[@id="end"]')
        end_date.send_keys(self.today)
        time.sleep(1)
        self.driver.find_element("xpath", "//body").click()
        time.sleep(1)
        submit_button = self.driver.find_element("xpath", '/html/body/main/div/div/div[2]/div/div[2]/form/div[4]/div/input[3]')
        submit_button.click()
        time.sleep(5)

    def get_daily_sessions(self):
        student_page = self.driver.page_source
        soup = BeautifulSoup(student_page, 'html.parser')
        sessions = soup.find('tbody', attrs={'class':'calendar-list'}).find_all('tr')[2:]
        return sessions

    def calculate_hours(self, sessions):
        working_hours = {'test_prep': 0, 'school': 0}
        for lesson in sessions:
            time_range = lesson.find_all('td')[0].text
            time_range = time_range.split(" - ")
            lesson_type = lesson.find_all('td')[6].text
            start_time = datetime.strptime(time_range[0], self.time_format)
            end_time = datetime.strptime(time_range[1], self.time_format)
            total_time = abs(end_time - start_time).seconds/3600
            if 'Test Preparation' in lesson_type:
                working_hours['test_prep'] += total_time
            else:
                working_hours['school'] += total_time

        return working_hours