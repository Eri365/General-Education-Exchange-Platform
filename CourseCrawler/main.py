from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
import time, json

try:
    with open('path.json', mode = 'r') as file:
        path = json.load(file)
except:
    print("ERROR:", __file__, "json 加載失敗")

def query_table_data(driver: webdriver.Chrome, year_value: str, subject_value: str):
    print(f'正在加載 {year_value} 學年期、{subject_value} 領域')
    # 選擇 學年期
    Select(driver.find_element('xpath', path['year_xpath'])).select_by_value(year_value)
    # 選擇 通識分類
    Select(driver.find_element('xpath', path['subject_xpath'])).select_by_value(subject_value)
    # 找到 開始查詢 按鈕
    
    buttons = driver.find_elements('xpath', "//input[@type='submit']")
    for button in buttons:
        button.click()
    return None

subject_values = ['E', 'G', 'K', 'M', 'L', '3', '8', 'N']

if __name__ == '__main__':
    driver = webdriver.Chrome()
    driver.get(path['url'])

    for value in subject_values:
        query_table_data(driver, '1111', value)
        time.sleep(1)
    driver.quit()
    
# 