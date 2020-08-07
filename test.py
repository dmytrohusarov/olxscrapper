from selenium import webdriver
from random import randint
import os
import time
import pandas as pd
import time

from pyvirtualdisplay import Display

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as expected
from selenium.webdriver.common.by import By
'''
add max price
add sorting - first 5 results
'''

url = 'https://www.olx.ua/ru/'

options = webdriver.ChromeOptions()
options.binary_location='/usr/bin/google-chrome-stable'
options.add_argument('--headless')
#options.add_argument('--start-maximized')
#options.add_argument('disable-infobars')
#options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
#options.add_argument('--disable-dev-shm-usage')
#options.add_argument('window-size={},{}'.format(1200,1100))

driver = webdriver.Chrome(chrome_options=options,executable_path='/usr/bin/chromedriver')

time_delay_long = randint(5, 7)
time_delay_short = randint(3, 4)
camping_availability_dictionary = {}
input = pd.read_csv('in.csv')
wait = WebDriverWait(driver, timeout=10)

property_data = []

start = time.time()
# try:
for item in input.index:

        driver.get(url)
        selectElem = driver.find_element_by_xpath('//*[@id="headerSearch"]')
        selectElem.send_keys(input.name[item])
        selectElem.submit()
        selectElemCity = driver.find_element_by_xpath('//*[@id="cityField"]')
        selectElemCity.clear()
        selectElemCity.send_keys(input.city[item])

        time.sleep(time_delay_short)

        try:
            selectElem = driver.find_element_by_xpath('// *[ @ id = "paramsListOpt"] / div / div[3] / div[2] / div[2] / span')
            selectElem.click()
        except:
            pass

        time.sleep(time_delay_long)
        selectElemCity.click()

        wait.until(expected.visibility_of_element_located((By.XPATH, '//*[@id="param_price"]/div/div[1]'))).click()
        #time.sleep(time_delay_long)

        selectElem = driver.find_element_by_xpath('// *[ @ id = "param_price"] / div / div[1] / label / input')
        try:
            selectElem.send_keys(int(input.minprice[item]))
        except Exception as e:
            print(e)

        time.sleep(time_delay_long)

        selectElem = driver.find_element_by_xpath('//*[@id="param_price"]/div/div[2]')
        selectElem.click()
        selectElem = driver.find_element_by_xpath('// *[ @ id = "param_price"] / div / div[2] / label / input')
        selectElem.send_keys(int(input.maxprice[item]))

        time.sleep(time_delay_long)

        selectElem = driver.find_element_by_xpath('//*[@id="order-select-gallery"]/li[3]/a')
        selectElem.click()

        time.sleep(time_delay_long)

        table_body = driver.find_element_by_xpath('//table[@id="offers_table"]')

        l = []
        for row in table_body.find_elements_by_xpath(".//tr"):

            names = [td.text for td in row.find_elements_by_xpath(".//h3[@class='lheight22 margintop5'][text()]")]
            vals  = [td.text for td in row.find_elements_by_xpath(".//td[@class='wwnormal tright td-price'][text()]")]

            # print(names,vals)

            if len(names) > 0:
                t1 = {}
                t1['name'] = input.name[item]
                t1['position'] = names[0]
                t1['price'] = vals[0]
                l.append(t1)

        l1 = [dict(t) for t in set([tuple(d.items()) for d in l])]
        l1 = sorted(l1, key=lambda k: k['price'])
        property_data.extend(l1[:5])

driver.quit()

#print(property_data)
df = pd.DataFrame.from_dict(property_data)
df.to_csv('out.csv', index=False)

print(time.time()- start)