from selenium import webdriver
from selenium.webdriver.support.ui import Select
import time, json

try:
    with open('path.json', mode = 'r') as file:
        path = json.load(file)
except:
    print("ERROR:", __file__, "json 加載失敗")

if __name__ == '__main__':
    driver = webdriver.Chrome()
    driver.get(path['url'])

    select_year = Select(driver.find_element('xpath', path['year_xpath']))
    select_year.select_by_value('1111')
    
    subject_option_count = len(Select(driver.find_element('xpath', path['subject_xpath'])).options)
    for i in range(subject_option_count):
        # 找到通識分類元素
        select_subject = Select(driver.find_element('xpath', path['subject_xpath']))
        # 取得所有選項
        options = select_subject.options
        # 取得當前索引值的 value
        value = options[i].get_attribute("value")
        print(f'正在加載 {value} 領域')  
        # Select
        select_subject.select_by_value(value)

        # 找到 開始查詢 按鈕
        button = driver.find_element('xpath', path['submit_xpath'])
        # 開始查詢
        button.click()
        
        time.sleep(1)
        
    driver.quit()