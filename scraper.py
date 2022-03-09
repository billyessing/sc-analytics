import time
import requests
import pandas as pd
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from data import headers


def get_season_data(year):
  print (f'Pulling data from {year} season')

  URL = f'https://www.nrlsupercoachstats.com/stats.php?year={year}'
  driver.get(URL)

  # select max records display option
  driver.find_element_by_xpath('//*[@id="list1_pager_center"]/table/tbody/tr/td[8]/select/option[8]').click()
  time.sleep(10)
  # num pages to iterate through
  num_pages = int(driver.find_element_by_xpath('//*[@id="sp_1_list1_pager"]').text)
  print (f'Number of pages: {num_pages}')

  season_data = ''

  for page in range(num_pages):
    print (f'Retrieving data from page {page+1} of {num_pages} ...')

    # get table data and fill blanks
    data = driver.find_element_by_xpath('//*[@id="list1"]/tbody').text
    data = data.replace('       ', ' na ')
    data = data.replace('   ', ' na ')
    data = data.replace('Partly Cloudy', 'Partly_Cloudy')
    season_data = season_data + '\n' + data

    # go to next page
    driver.find_element_by_xpath('//*[@id="next_list1_pager"]').click()
    time.sleep(20)

  print ('Formatting data ...')

  # format data into a list for each row
  season_data = season_data.split('\n')
  season_data = [d.split(' ') for d in season_data]
  # len(d) ==> 81 for 2021, 2020, 2019, 2018
  # len(d) ==> 79 ... TODO
  season_data = [d for d in season_data if len(d) == 81 and 'Totals' not in d]

  df = pd.DataFrame(season_data, columns=headers)
  df.to_excel(f'data/season_stats_{year}.xlsx')



driver = webdriver.Chrome(ChromeDriverManager().install()) 

for year in ['2021']:
  get_season_data(year)


