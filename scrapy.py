from selenium import webdriver
from bs4 import BeautifulSoup as bs
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os

class Site:
  def __init__(self, driver):
    self.driver = driver
    self.url = 'https://www.governotransparente.com.br/1311490?clean=false'
    self.bs_obj = None
    self.exercise_years = {'2019': 13, '2018': 12, '2017': 11,
                  '2016': 10, '2015': 9, '2014': 8,
                  '2013': 7}

  def navigate(self, url=None):
    if(url):
      self.driver.get(url)
    else:
      self.driver.get(self.url)

  def _get_inital_options(self):
    home_div = self.driver.find_element_by_id('menu-home')
    return home_div.find_elements_by_tag_name('a')

  def _get_expenses_options(self):
    buttons_div = self.driver.find_elements_by_class_name('demo-button')
    return buttons_div[0].find_elements_by_tag_name('a')

  def to_expenses(self):
    url = self._get_inital_options()[1].get_attribute('href')
    self.navigate(url)

  '''
    start_date = DD/MM/YYYY
    end_date = DD/MM/YYYY
  '''
  def get_consults(self, year, start_date, end_date):
    url = self._get_expenses_options()[0].get_attribute('href')
    exercise_year = '/resultado?ano='+str(self.exercise_years[year])
    url_consult = url.split('?')[0]+exercise_year+'&inicio='+start_date+'' \
                    '&fim='+end_date
    self.navigate(url_consult)
    button_csv = self.driver.find_element_by_css_selector('a.dt-button:nth-child(2)')
    site.driver.implicitly_wait(30)
    time.sleep(3)
    actions = webdriver.ActionChains(self.driver)
    actions.click(button_csv)
    actions.perform()

  def close(self):
    self.driver.close()

if __name__ == "__main__":
  profile = webdriver.FirefoxProfile()
  profile.set_preference('browser.download.folderList', 2)
  profile.set_preference('browser.download.manager.showWhenStarting', False)
  profile.set_preference(key="browser.helperApps.neverAsk.saveToDisk", value="text/csv")
  profile.set_preference('browser.download.dir', os.getcwd())
  site = Site(webdriver.Firefox(firefox_profile=profile))
  site.driver.implicitly_wait(10) # seconds
  site.navigate()
  site.to_expenses()
  site.get_consults('2018', '5/02/2018', '06/07/2018')
  time.sleep(2)
  site.close()
