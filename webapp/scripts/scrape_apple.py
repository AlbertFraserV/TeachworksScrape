import sys
import os
sys.path.append(os.path.abspath("/Users/alv/Documents/Scripts/Teachworks/webapp/src"))
from AppleWallet import AppleWallet
from database import Database

apple = AppleWallet()
conn = Database()

breakpoint()

sign_in_button = apple.driver.find_element('xpath', "/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[2]/div/div/div")
sign_in_button.click()


iframe = apple.driver.find_element('xpath' , '//*[@id="aid-auth-widget-iFrame"]')
apple.driver.switch_to.frame(iframe)
apple_id_field = apple.driver.find_element('xpath', '//*[@id="account_name_text_field"]')
submit_btn = apple.driver.find_element('xpath', '/html/body/div[3]/apple-auth/div/div[1]/div/sign-in/div/div[1]/button[1]/i')
pwd_field = apple.driver.find_element('xpath', '//*[@id="password_text_field"]')
submit_btn = apple.driver.find_element('xpath', '/html/body/div[3]/apple-auth/div/div[1]/div/sign-in/div/div[1]/button[1]/i')


apple_card_iframe = apple.driver.find_element('xpath', '//*[@id="apple-card"]')
apple.driver.switch_to.frame(apple_card_iframe)
balance = apple.driver.find_element('xpath', '/html/body/div[1]/div/div/div/div/ui-main-pane/div[2]/main/div/div[2]/div/div/div/section[1]/div/div/div[1]/div/div/div[1]').text

balance_details_btn = apple.driver.find_element('xpath', '/html/body/div[1]/div/div/div/div/ui-main-pane/div[2]/main/div/div[2]/div/div/div/section[1]/div/div/div[2]/ui-button')
