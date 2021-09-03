# Web scraping components 
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
DRIVER_PATH = '/app/.chromedriver/bin/chromedriver'

# headless option
options = Options()
options.headless = True
options.add_argument("--window-size=1920,1200")

driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)
driver.get("https://www.google.com/search?q=mars&sxsrf=ALeKk020wmbFGsz8EB7ZDg8J84sbZuuCwQ:1628285751695&source=lnms&tbm=nws&sa=X&ved=2ahUKEwi43cmOrZ3yAhXWWM0KHW-CBdwQ_AUoAXoECAEQAw&biw=1920&bih=948")

# Webscrapes set number of articles based on desired page
# from the search "mars" on google news
class MarsArticles :
    def __init__(self, pagesDesired, articleCount) :
        self.pagesDesired = pagesDesired
        self.articleCount = articleCount

    # given a desired page number and article count
    # method returns a list of urls representing 
    # articles about mars
    def getArticles(self) :
        getPage = self.pagesDesired - 1
        articleCount = self.articleCount
        url = None
        # gets to page desired for article scraping
        set_of_pages = driver.find_element_by_class_name("AaVjTc").find_elements_by_tag_name("a")
        for pageNumber in set_of_pages :
            if getPage <= 0 :
                break
            else :
                url = pageNumber.get_attribute('href')
                getPage = getPage - 1
        if url != None :
            driver.get(url)

        # all links on the page for 'mars' search result on news section
        article_url = []
        
        # gets desired amount of article links
        try: 
            articles = driver.find_elements_by_class_name("dbsr")
            for article in articles : 
                # contains link within css info
                css_info = article.find_elements_by_tag_name("a")
                for url in css_info :
                    if articleCount > 0 :
                        article_url.append(url.get_attribute('href'))
                        articleCount = articleCount - 1
                    else :
                        break
        finally:
            return article_url