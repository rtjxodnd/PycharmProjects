from selenium import webdriver
from config import config

class Common:

    ###########################################################
    # page driver 설정
    ###########################################################
    def set_page_driver(self, sosok):
        chromeDriverPath = config.chromeDriverPath('test')
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-no-shm-usage')

        driver = webdriver.Chrome(chromeDriverPath, chrome_options=chrome_options)
        url = "https://finance.naver.com/sise/sise_market_sum.nhn?sosok=" + sosok
        driver.get(url)
        click_option1 = driver.find_element_by_xpath("//*[@id='option12']")
        click_option2 = driver.find_element_by_xpath("//*[@id='option18']")
        click_option3 = driver.find_element_by_xpath('//*[@id="contentarea_left"]/div[2]/form/div/div/div/a[1]/img')
        click_option1.click()
        click_option2.click()
        click_option3.click()

        return driver

    ###########################################################
    # pageNum 보정
    ###########################################################
    def make_page_num(self, pageNum):
        if pageNum < 3:
            pageNum = str(pageNum)
        elif pageNum < 12:
            pageNum = str(pageNum + 1)
        else:
            pageNum = str(((pageNum - 2) % 10) + 4)
        return pageNum