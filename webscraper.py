# Web scraping components 
from selenium import webdriver
import selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
DRIVER_PATH = '/home/misbahaving/Documents/chromedriver'

options = Options()
options.headless = True
options.add_argument("--window-size=1920,1200")

driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)
driver.get("https://www.google.com/search?q=mars&sxsrf=ALeKk020wmbFGsz8EB7ZDg8J84sbZuuCwQ:1628285751695&source=lnms&tbm=nws&sa=X&ved=2ahUKEwi43cmOrZ3yAhXWWM0KHW-CBdwQ_AUoAXoECAEQAw&biw=1920&bih=948")


class MarsArticles :
    def __init__(self, pagesDesired) :
        self.pagesDesired = pagesDesired

    def getArticles(self) :
        getPage = self.pagesDesired
        # gets to page desired for article scraping
        while(getPage > 1) :
            nextPage = driver.find_elements_by_class_name('d6cvqb')[1].find_element_by_tag_name('a').get_attribute('href')
            driver.get(nextPage)
            getPage = getPage - 1
        
        # all links on the page for 'mars' search result on news section
        try: 
            articles = driver.find_elements_by_class_name("dbsr")
            for article in articles : 
                # contains link within css info
                css_info = article.find_elements_by_tag_name("a")
                for url in css_info :
                    print(url.get_attribute('href'))
        finally:
            driver.quit()





