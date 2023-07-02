# 利用 Selenium module 爬中興大學通識課
# 目前所選的學年期範圍是 105 學期到 111 學期
# 理論上可以爬更舊的課表，但目前只打算先截止到 105 學期的
# 爬到的資料皆會放置在 CourseData 這個資料夾，並且依據學年期在把資料做切分
# course.py 目前不會用到，原先是想把課程的資料用類別包起來，但後來發現沒有必要
# 基於最新學期的課表格式會與舊的課表有些需差異，目前只能爬舊的課表，針對最新的目前還沒完成

from selenium import webdriver # selenium
from selenium.webdriver.support.ui import Select # selenium
from selenium.webdriver.remote.webelement import WebElement # selenium
from selenium.webdriver.chrome.options import Options # selenium
from frozendict import frozendict # 優化 dict 的 module
import atexit # 為確保程式結束時，類別的 driver 會自動 quit
import os, csv # 寫檔
import json # 其他

# 加載所有的 path 
try:
    with open('path.json', mode = 'r') as file:
        path = json.load(file)
except:
    print('----ERROR:', __file__, 'json 加載失敗')
# 所有的學年、期
years = ('1051', '1052', '1061', '1062', '1071', '1072', '1081', '1082', '1091', '1092', '1101', '1102', '1111', '1112')
# 所有的通識分類
subjects = frozendict(
            {'E': '人文領域', 'F': '社會領域', 'G': '自然領域', 'K': '統合領域',
             'M': '核心素養', 'L': '通識資訊素養', '3': '大學國文',
             '8': '大一英文(109)學年前', 'N': '大學語文(110學年後)'})
# CourseData 資料夾的路徑
course_data_path = os.path.join(os.getcwd(), 'CourseData') 

class Crawler:
    def __init__(self):
        self.options = Options()
        self.options.add_argument("--headless") # 關掉預覽模式
        self.driver = webdriver.Chrome(options = self.options)
        self.driver.implicitly_wait(10) # 設置隱性等待時間
        self.driver.get(path['url'])
        atexit.register(self.exit_handler) # 註冊結束處理程式
    
    # 程式結束時，自動 quit 掉 driver
    def exit_handler(self):
        self.driver.quit()
    
    def query(self, year_value: str, subject_value: str) -> WebElement:
        print(f'正在加載 {year_value} 學年期、{subjects[subject_value]}')
        # 選擇 學年期
        Select(self.driver.find_element('xpath', path['year_xpath'])).select_by_value(year_value)
        # 選擇 通識分類
        Select(self.driver.find_element('xpath', path['subject_xpath'])).select_by_value(subject_value)
        # 找到 開始查詢 按鈕
        # 學校網頁中的 查詢按鈕 可能有多個不同的 xpath，因此改用 find_elements
        # 並將每個按鈕都實際按一次 (反正不影響結果)
        buttons = self.driver.find_elements('xpath', path['submit_xpath'])
        for button in buttons:
            button.click()
        # 回傳表格
        return self.driver.find_element('xpath', path['table_xpath'])
    
    @staticmethod
    def pack_table_list(table: WebElement):
        header = []
        for thead in table.find_elements('tag name', 'thead'):
            for row in thead.find_elements('tag name', 'tr'):
                for cell in row.find_elements('tag name', 'th'):
                    header.append(cell.text.replace('\n', ' '))
        body = []
        for tbody in table.find_elements('tag name', 'tbody'):
            for row in tbody.find_elements('tag name', 'tr'):
                data_list = []
                for cell in row.find_elements('tag name', 'td'):
                    data_list.append(cell.text.replace('\n', ' '))
                body.append(data_list)
        return header, body
    
    @staticmethod
    def write_to_csv(header: list, body: list, year_value: str, subject_value: str):
        # 以學年期作分類依據，切成多個子資料夾
        subfolder_path = os.path.join(course_data_path, year_value)
        # 確保資料夾存在
        if not os.path.exists(subfolder_path):
            os.makedirs(subfolder_path)
        csv_filepath = os.path.join(subfolder_path, subjects[subject_value] + '.csv')
        # 遇到特殊字體時會跳出 Error，這邊都先直接忽略
        with open(csv_filepath, 'w', newline = '', errors = 'ignore') as file:
            writer = csv.writer(file)
            writer.writerow(header)  # 寫入標題列
            writer.writerows(body)  # 寫入資料列

if __name__ == '__main__':
    crawler = Crawler()
    for year_value in years:
        for subject_value, _ in subjects.items():
            table = crawler.query(year_value, subject_value)
            header, body = crawler.pack_table_list(table)
            crawler.write_to_csv(header, body, year_value, subject_value)
    print('-' * 10, '程式結束', '-' * 10)