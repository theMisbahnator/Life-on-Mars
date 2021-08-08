# Web scraping components 
from selenium import webdriver
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


try: 
    main = driver.find_elements_by_class_name("dbsr")
    
    for articles in main : 
        article = articles.find_elements_by_tag_name("a")
        for i in article :
            print(i.get_attribute('href'))

finally:
    driver.quit()

