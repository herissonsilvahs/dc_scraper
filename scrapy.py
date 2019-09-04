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

  def _btn_click(self, path):
    site.driver.implicitly_wait(30)
    time.sleep(3)
    actions = webdriver.ActionChains(self.driver)
    actions.click(path)
    actions.perform()

  def _to_expenses(self):
    url = self._get_inital_options()[1].get_attribute('href')
    self.navigate(url)

  def _get_url_contracts(self):
    url = self._get_inital_options()[6].get_attribute('href')
    return url

  def get_contract_details(self, year, start_date, end_date, n_contract):
    self.navigate()
    url = self._get_url_contracts()
    exercise_year = '/resultado?ano='+str(self.exercise_years[year])
    url_consult = url.split('?')[0]+exercise_year+'&inicio='+start_date+'' \
                    '&fim='+end_date+'&contr='+n_contract+'&credor=-1'
    self.navigate(url_consult)
    url_contract = self.driver.find_element_by_css_selector('.odd > td:nth-child(2) > a:nth-child(1)').get_attribute('href')
    self.navigate(url_contract)
    soup = bs(self.driver.page_source, 'html.parser')
    text = soup.select_one('body > section.content > div > div.row.clearfix > div > div > div.body')
    print(text.get_text())

  def get_contracts(self, year, start_date, end_date, credor=-1):
    self.navigate()
    url = self._get_url_contracts()
    exercise_year = '/resultado?ano='+str(self.exercise_years[year])
    url_consult = url.split('?')[0]+exercise_year+'&inicio='+start_date+'' \
                    '&fim='+end_date+'&credor='+str(credor)
    self.navigate(url_consult)
    button_csv = self.driver.find_element_by_css_selector('button.dt-button:nth-child(2)')
    self._btn_click(button_csv)
    time.sleep(2)

    file_name = os.getcwd()+'/data/relatorio_'+year+'.csv'
    if(os.path.isfile(os.getcwd()+'/data/Relatório.csv')):
      print(file_name)
      os.rename(os.getcwd()+'/data/Relatório.csv', file_name)
      time.sleep(1)

  '''
    start_date = DD/MM/YYYY
    end_date = DD/MM/YYYY
  '''
  def get_consults(self, year, start_date, end_date):
    self.navigate()
    self._to_expenses()
    url = self.driver.find_element_by_css_selector('body > section.content > div > div:nth-child(2) > div > div > div.body > div > a:nth-child(1)').get_attribute('href')
    exercise_year = '/resultado?ano='+str(self.exercise_years[year])
    url_consult = url.split('?')[0]+exercise_year+'&inicio='+start_date+'' \
                    '&fim='+end_date
    self.navigate(url_consult)
    button_csv = self.driver.find_element_by_css_selector('button.dt-button:nth-child(2)')
    self._btn_click(button_csv)
    time.sleep(2)

    file_name = os.getcwd()+'/data/empenho_'+year+'.csv'
    if(os.path.isfile(os.getcwd()+'/data/Relatório.csv')):
      print(file_name)
      os.rename(os.getcwd()+'/data/Relatório.csv', file_name)
      time.sleep(1)

  def close(self):
    self.driver.close()

if __name__ == "__main__":
  # Setup
  profile = webdriver.FirefoxProfile()
  profile.set_preference('browser.download.folderList', 2)
  profile.set_preference('browser.download.manager.showWhenStarting', False)
  profile.set_preference(
    key="browser.helperApps.neverAsk.saveToDisk",
    value="text/csv"
  )
  profile.set_preference('browser.download.dir', os.getcwd()+'/data')
  site = Site(webdriver.Firefox(firefox_profile=profile))
  site.driver.implicitly_wait(10) # seconds

  # Start navigation
  site.get_consults('2017', '05/02/2017', '06/12/2017')
  site.get_consults('2018', '05/02/2018', '06/12/2018')
  site.get_consults('2019', '05/02/2019', '06/12/2019')
  # site.get_contracts('2017', '01/01/2017', '01/12/2017')
  # site.get_contracts('2018', '01/01/2018', '01/12/2018')
  # site.get_contracts('2019', '01/01/2019', '01/12/2019')
  # site.get_contract_details('2017', '01/01/2017', '29/12/2017', '2014.02.20.1')
  site.close()
