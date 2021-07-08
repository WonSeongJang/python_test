import smtplib # 메일을 보내기 위한 라이브러리 모듈
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication 
import openpyxl
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from datetime import datetime
import time
import os

chromedriver = 'D:\\ETC\\Python\\ChromeDriver\\chromedriver.exe'
driver = webdriver.Chrome(chromedriver)
driver.get('https://www.ih.co.kr/open_content/bbs.do?act=list&bcd=notice&bgcd=site1&pgdiv=site1_2&cate_cd=임대&pageno=1')
inchoen_lists = list()
no_content = '오늘 올라온 공고가 없습니다.'

loop, count = True, 0
time.sleep(3)
while loop and count <1 :
    try:        
        comment_box = driver.find_element_by_css_selector('#detail_con > div.bbs_con > div > table > tbody')
        comment_list = comment_box.find_elements_by_tag_name('tr')
        for comment in comment_list:
            #print(i, type(i))
            product_name = comment.find_element_by_css_selector('td.title > a')
            product_type = comment.find_element_by_css_selector('td:nth-child(2)')
            product_startdate = comment.find_element_by_css_selector('td:nth-child(5)')
            product_link = comment.find_element_by_css_selector('td.title > a').get_attribute('href')
            if product_startdate == datetime.today().strftime("%Y.%m.%d"):
                product_info = [product_name.text.strip(), product_type.text, product_startdate.text, product_link]
                inchoen_lists.append(product_info)
        count += 1
        time.sleep(2)
    except TimeoutException:
        loop = False
print(comment_list)

driver.quit()

sendEmail = "msnjws12264@gmail.com"
recvEmail = "msnjws12264@gmail.com" #"flatworldmanage@gmail.com"
password = "unajkygwlaatuaxb"

smtpName = "smtp.gmail.com"
smtpPort = 587
text = ''
#여러 MIME을 넣기위한 MIMEMultipart 객체 생성
msg = MIMEMultipart()

if inchoen_lists == ():
    msg['Subject'] ="인천 크롤링"+datetime.today().strftime("%Y_%m_%d")
    msg['From'] = sendEmail 
    msg['To'] = recvEmail 
    for num in inchoen_lists:
        text = text + "제목 : " + str(num[0]) + "\n구분 : " + str(num[1]) + "\n날짜 : " + str(num[2]) + "\n링크 : " + str(num[3]) + '\n-------------------------------\n'
    contentPart = MIMEText(text) #MIMEText(text , _charset = "utf8")
    msg.attach(contentPart) 
else:
    msg['Subject'] ="인천 크롤링"+datetime.today().strftime("%Y_%m_%d") + no_content
    msg['From'] = sendEmail 
    msg['To'] = recvEmail 
    text = no_content
    contentPart = MIMEText(text) #MIMEText(text , _charset = "utf8")
    msg.attach(contentPart) 


s=smtplib.SMTP( smtpName , smtpPort )
s.starttls()
s.login( sendEmail , password ) 
s.sendmail( sendEmail, recvEmail, msg.as_string() )  
s.close() 
