import os
import time
from budgetting.models import DailyPaid, DailySpent, DailyNet
from django.core.management.base import BaseCommand, CommandError
from dotenv import load_dotenv
from selenium import webdriver
from bs4 import BeautifulSoup
from datetime import datetime

class Command(BaseCommand):
    help = "Scrapes Teachworks for daily pay."

    def add_arguments(self, parser):
        parser.add_argument('start_date', nargs=None, type=str)
        parser.add_argument('end_date', nargs=None, type=str)

    def handle(self, *args, **options):
        teachworks = self.start_driver()

        self.login()
        self.navigate_to_calendar_list(options['start_date'], options['end_date'])
        sessions = self.get_daily_sessions()
        working_hours = self.calculate_hours(sessions)

        for day in working_hours:
            wages = working_hours[day]
            wages = (wages['test_prep']*self.TEST_PREP_WAGE + wages['school']*self.SCHOOL_WAGE)*(1-self.TAX_RATE)
            paid_date = datetime.strptime(day, '%m/%d/%Y')
            new_entry = DailyPaid(paid_date = paid_date, paid_amount = wages)
            new_entry.save()

        self.close_driver()

    def start_driver(self):
        load_dotenv()
        self.url = "http://homeworkhelperstutoring.teachworks.com"
        self.driver = webdriver.Firefox(executable_path = '/usr/local/bin/geckodriver')
        self.USER = os.getenv('USERNAME')
        self.PASSWORD = os.environ.get('PASS')
        self.TEST_PREP_WAGE = float(os.environ.get('TESTPREP'))
        self.SCHOOL_WAGE = float(os.environ.get('SCHOOL'))
        self.TAX_RATE = float(os.environ.get('TAX'))/100
        self.time_format = "%I:%M %p"

    def close_driver(self):
        self.driver.close()

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

    def navigate_to_calendar_list(self, begin_date = None, end_date = None):
        calendar_list_url = f"https://homeworkhelperstutoring.teachworks.com/calendar_list?start={begin_date}&end={end_date}&service_id=&student_id=&filter=true&commit=Submit"
        self.driver.get(calendar_list_url)

    def get_daily_sessions(self):
        student_page = self.driver.page_source
        soup = BeautifulSoup(student_page, 'html.parser')
        sessions = soup.find('tbody', attrs={'class':'calendar-list'}).find_all('tr')
        return sessions

    def calculate_hours(self, sessions):
        dates = {}
        working_hours = {'test_prep': 0, 'school': 0}
        cur_date = None
        for lesson in sessions:
            if len(lesson.find_all('td')) == 0 and len(lesson.find_all('th')) == 1:
                if sum(working_hours.values()) != 0:
                    dates[cur_date] = working_hours
                    working_hours = {'test_prep': 0, 'school': 0}
                cur_date = lesson.find('th').text.split(",")[-1].lstrip()
                cur_date = datetime.strptime(cur_date, '%B %d %Y')
                cur_date = cur_date.strftime('%m/%d/%Y')
                continue
            elif len(lesson.find_all('td')) == 0 and len(lesson.find_all('th')) > 1:
                continue
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

        dates[cur_date] = working_hours
        return dates