import time
import selenium.common.exceptions
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.alert import Alert
import configparser
import re
from random import randint


def driverLogin(account):
    chrome_options = Options()
    # chrome_options.add_argument('headless')
    # chrome_options.add_argument('window-size=1920x1080')
    # chrome_options.add_argument("disable-gpu")
    config = configparser.ConfigParser()
    config.read(account)

    driver = webdriver.Chrome('chromedriver.exe', chrome_options=chrome_options)
    driver.get("https://novelpia.com/page/login")
    driver.implicitly_wait(1)

    driver.find_element_by_css_selector("#login_box > div:nth-child(2) > input").send_keys(config['USER_INFO']['ID'])
    driver.find_element_by_css_selector("#login_box > div:nth-child(3) > input").send_keys(config['USER_INFO']['PW'])
    driver.find_element_by_css_selector("#login_box > button").click()
    driver.implicitly_wait(3)

    Alert(driver).accept()

    return driver


def driverCrawlList(listUrl, driver):
    regex = re.compile(r'/viewer/\d+')
    dictList = {}

    driver.get(listUrl)
    # Page detect
    listPage = driver.find_element_by_css_selector("#episode_list > div > nav > ul")
    allPage = listPage.find_elements_by_css_selector("li.page-item")
    currentPage = listPage.find_element_by_css_selector("li.page-item.active").text

    for i in range(len(allPage)):
        allPage[i] = allPage[i].text

    print(allPage)
    # while currentPage <= max(allPage):

    driver.find_element_by_xpath("//li[@class='active']/following-sibling::*/div").click()
    episodeList = driver.find_element_by_css_selector("#episode_list")
    episodeList = episodeList.find_elements_by_css_selector("#episode_list > table > tbody > tr.ep_style5")

    for i in range(len(episodeList)):
        episodeNo = episodeList[i].find_element_by_xpath("td[2]/div/font/span[1]").text
        episodeUrl = episodeList[i].find_element_by_xpath("td[2]").get_attribute("onclick")
        mo = regex.search(episodeUrl)
        episodeUrl = mo.group()
        dictList.update({episodeNo: episodeUrl})

    # {{EP1:/viewer/1134}, {EP2:/viewer/1134}}
    # //li[@class='page-item' and @class='active']/following-sibling::*
    #

    return dictList


def driverCrawl(url, driver):
    urlRegex = re.compile(r'/viewer/\d+')
    titleRegex = re.compile(r'EP.+')

    driver.get(url)
    driver.implicitly_wait(3)

    try:
        while driver.find_element_by_css_selector("div#next_epi_btn_bottom") is not None:
            title = driver.find_element_by_css_selector("span.cut_line_one").text
            mo1 = titleRegex.search(title)
            title = mo1.group()

            novel = driver.find_element_by_css_selector("#novel_drawing").text

            saveText(title, novel)
            print(title+' 완료')

            time.sleep(randint(3,10))

            nextPage = driver.find_element_by_css_selector("div#next_epi_btn_bottom").get_attribute("onclick")
            mo2 = urlRegex.search(nextPage)
            nextPage = mo2.group()
            driver.get('https://novelpia.com'+nextPage)
    except selenium.common.exceptions.WebDriverException as e:
        print(str(e))


def driverQuit(driver):
    driver.quit()

def saveText(title, str):
    file = open('text/'+title+'.txt', 'w', encoding='UTF-8')
    file.write(str)
    file.close()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    driver = driverLogin('account.ini')
    # res = driverCrawlList('https://novelpia.com/novel/23', driver)
    driverCrawl('https://novelpia.com/viewer/1134', driver)
    driverQuit(driver)


    # print(res)

    # novel = refresher("https://novelpia.com/viewer/265792")
    # clipboard.copy(novel)
