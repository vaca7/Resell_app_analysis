from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC #selenium에서 사용할 모듈 import
import time
import requests
from bs4 import BeautifulSoup
import re
import csv
from selenium.common.exceptions import NoSuchElementException

options = webdriver.ChromeOptions()

#패션잡화->프리미엄 시계 사이트주소
options.add_experimental_option("excludeSwitches", ["enable-logging"])
driver = webdriver.Chrome(options=options)
# 크림 메인 홈페이지
# url = 'https://kream.co.kr/'
url = 'https://kream.co.kr/search'
driver.get(url)
driver.maximize_window()
time.sleep(3)
# 로그인 클릭
driver.find_element(By.XPATH, '//*[@id="__layout"]/div/div[1]/div[1]/div/ul/li[4]/a').click()
time.sleep(3)
# 아이디 입력
driver.find_element(By.XPATH, '//*[@id="__layout"]/div/div[2]/div[1]/div/div[1]/div/input').send_keys('kimnayeon@hanafos.com')
#비밀번호 입력
driver.find_element(By.XPATH, '//*[@id="__layout"]/div/div[2]/div[1]/div/div[2]/div/input').send_keys('kim523090!')
time.sleep(3)
#로그인
driver.find_element(By.XPATH, '//*[@id="__layout"]/div/div[2]/div[1]/div/div[3]/a').click()
time.sleep(3)
# 플러스 버튼 클릭
# driver.find_element(by=By.XPATH, value='//*[@id="__layout"]/div/div[2]/div[5]/div[1]/div[2]/div[1]/div[2]/svg').click()
driver.find_element(By.XPATH, '//*[@id="__layout"]/div/div[2]/div[5]/div[1]/div[2]/div[1]/div[1]/span[1]').click()
time.sleep(3)

# 테크 카테고리 선택
# driver.find_element(by=By.XPATH, value='//*[@id="__layout"]/div/div[2]/div[5]/div[1]/div[2]/div[2]/ul/li[2]/a/svg').click()
driver.find_element(By.XPATH, '//*[@id="__layout"]/div/div[2]/div[5]/div[1]/div[2]/div[2]/ul/li[5]/a/span').click()
time.sleep(3)

# 그래픽카드 세부카테고리 선택
# driver.find_element(by=By.XPATH, value='//*[@id="__layout"]/div/div[2]/div[5]/div[1]/div[2]/div[2]/ul/li[5]/ul/li[3]/a/span').click()
driver.find_element(By.XPATH, '//*[@id="__layout"]/div/div[2]/div[5]/div[1]/div[2]/div[2]/ul/li[5]/ul/li[3]/a/span').click()

#화면 표시 기다리기
time.sleep(5) 

final_result = []

#처음부터 스크롤 10번 내리기(~400번까지 상품 조회 가능)
for i in range(4):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1)

# # 반복 시작
i = 1
while i <= 42:
    
    # if i == 40:
    # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    # time.sleep(5)

    bname = driver.find_element(By.XPATH, f'//*[@id="__layout"]/div/div[2]/div[5]/div[2]/div[3]/div[1]/div[{i}]/a/div[2]/div[1]/p[1]').text
    pname = driver.find_element(By.XPATH, f'//*[@id="__layout"]/div/div[2]/div[5]/div[2]/div[3]/div[1]/div[{i}]/a/div[2]/div[1]/p[2]').text
    price = driver.find_element(By.XPATH, f'//*[@id="__layout"]/div/div[2]/div[5]/div[2]/div[3]/div[1]/div[{i}]/a/div[2]/div[2]/div[1]').text
    saved = driver.find_element(By.XPATH, f'//*[@id="__layout"]/div/div[2]/div[5]/div[2]/div[3]/div[1]/div[{i}]/div/span[1]/span').text
    feed = driver.find_element(By.XPATH, f'//*[@id="__layout"]/div/div[2]/div[5]/div[2]/div[3]/div[1]/div[{i}]/div/span[2]/span').text
    try:
        total_sales = driver.find_element(By.XPATH, f'//*[@id="__layout"]/div/div[2]/div[5]/div[2]/div[3]/div[1]/div[{i}]/a/div[1]/div').text
    except NoSuchElementException:
        total_sales = '0'
    store_info = {
            'category':'Tech',
            'detailed_category':'Graphic Card',
            'brand_name':bname,
            'product_name':pname,
            'total_sales' :total_sales,
            'product_price':price,
            'saving_person':saved,
            'feeding_person':feed,
            }
    #크롤링한 정보들을 store_info에 담고
    print('Tech','Graphic Card',bname, pname,total_sales, price,saved,feed)
    print("*" * 50)
    # 출력해서 확인 후 final_result에 저장
    final_result.append(store_info)

    i += 1

print(final_result)

# csv 파일 생성
try:
    with open('graphic_card.csv', 'w', encoding= 'CP949') as f:
        writer = csv.DictWriter(f, fieldnames=["category","detailed_category","brand_name", "product_name","total_sales", "product_price", "saving_person", "feeding_person"])
        writer.writeheader()
        for elem in final_result:
            writer.writerow(elem)
except IOError:
    print("I/O error")
