# import time
# import logging
# import smtplib
# import os
# from email.mime.text import MIMEText
# from email.mime.base import MIMEBase
# from email import encoders
import selenium.common.exceptions
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.alert import Alert
import clipboard
# from win10toast import ToastNotifier



def refresher(url):
    chrome_options = Options()
    # chrome_options.add_argument('headless')
    # chrome_options.add_argument('window-size=1920x1080')
    # chrome_options.add_argument("disable-gpu")

    driver = webdriver.Chrome('chromedriver.exe', chrome_options=chrome_options)
    driver.get("https://novelpia.com/page/login")
    driver.implicitly_wait(1)

    driver.find_element_by_css_selector("#login_box > div:nth-child(2) > input").send_keys("ehfmak@naver.com")
    driver.find_element_by_css_selector("#login_box > div:nth-child(3) > input").send_keys("gkanxkfh204")
    driver.find_element_by_css_selector("#login_box > button").click()
    driver.implicitly_wait(3)

    da = Alert(driver)
    da.accept()

    driver.get(url)
    driver.implicitly_wait(3)
    # driver.save_screenshot('screenshot.png')

    Text = driver.find_element_by_css_selector(
        "#novel_drawing"
    ).text

    driver.quit()

    return Text


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    novel = refresher("https://novelpia.com/viewer/265792")
    clipboard.copy(novel)

