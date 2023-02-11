from selenium import webdriver
import time
from bs4 import BeautifulSoup
from datetime import datetime
import os
from dotenv import load_dotenv

class AppleWallet:
    def __init__(self):
        load_dotenv()
        self.url = "https://card.apple.com"
        self.driver = webdriver.Firefox(executable_path = '/usr/local/bin/geckodriver')

