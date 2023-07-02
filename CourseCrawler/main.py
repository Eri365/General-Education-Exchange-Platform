# selenium
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.remote.webelement import WebElement
# 優化 dict 的 module
from frozendict import frozendict
# 確保程式結束時，類別的 driver 會自動 quit
import atexit
# 其他
import time, json, csv


try:
    with open('path.json', mode = 'r') as file:
        path = json.load(file)
except:
    print('----ERROR:', __file__, 'json 加載失敗')

subjects = frozendict(
            {'E': '人文領域', 'F': '社會領域', 'G': '自然領域', 'K': '統合領域',
             'M': '核心素養', 'L': '通識資訊素養', '3': '大學國文',
             '8': '大一英文(109)學年前', 'N': '大學語文(110學年後)'})

class Crawler:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.driver.get(path['url'])
        # 註冊結束處理程序
        atexit.register(self.exit_handler)
        
    def exit_handler(self):
        self.driver.quit()
    
    def query(self, year_value: str, subject_value: str):
        print(f'正在加載 {year_value} 學年期、{subjects[subject_value]}')
        # 選擇 學年期
        Select(self.driver.find_element('xpath', path['year_xpath'])).select_by_value(year_value)
        # 選擇 通識分類
        Select(self.driver.find_element('xpath', path['subject_xpath'])).select_by_value(subject_value)
        # 找到 開始查詢 按鈕
        # 查詢按鈕 可能有多個不同的 xpath，因此改用 find_elements 
        buttons = self.driver.find_elements('xpath', path['submit_xpath'])
        for button in buttons:
            button.click()
        # 確保成功找到資料，否則 return None
        try:
            table = self.driver.find_element('xpath', path['table_xpath'])
        except:
            print('----ERROR:', __file__, '找不到表格')
            return
        
        for row in table.find_elements('xpath', './/tr'):
            for cell in row.find_elements('xpath', './/td'):
                print(cell.text, end = '  ')

if __name__ == '__main__':
    crawler = Crawler()
    crawler.query('1111', 'E')
    print('-' * 10, '程式結束', '-' * 10)
    
    
# //*[@id="myTable01"]/tbody