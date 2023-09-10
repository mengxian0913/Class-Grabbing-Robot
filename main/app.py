from config import User
from PIL import Image
import pytesseract
from bs4 import BeautifulSoup as bs4
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import Select
import time
import requests
import os
import shutil

chromedriver = "/opt/homebrew/bin/chromedriver"
options = webdriver.ChromeOptions()
options.add_argument("--incognito")
# options.add_argument("headless")
# options.add_argument("head")
driver = webdriver.Chrome(options=options)

Course_RUL = "https://course.fcu.edu.tw/"
Logout_button = None

def clear(): os.system('clear')

def Get_Logout_button():
    return driver.find_element(By.XPATH, "//input[@name='ctl00$btnLogout']")

def Get_boxes():
    return [driver.find_element(By.XPATH, "//input[@id='ctl00_Login1_UserName']"), driver.find_element(By.XPATH, "//input[@id='ctl00_Login1_Password']"), driver.find_element(By.XPATH, "//input[@id='ctl00_Login1_vcode']")]

def Get_vcode_element():
    return driver.find_element(By.XPATH, "//img[@id='ctl00_Login1_Image1']")

def checklog():
    global Logout_button

    try:
        # Logout_button = driver.find_element(By.XPATH, "//input[@name='ctl00$btnLogout']")
        # 最多等待 1 秒
        Logout_button = WebDriverWait(driver, 1).until(
                EC.presence_of_element_located((By.XPATH, "//input[@name='ctl00$btnLogout']"))
        )
        print("已成功登入")
        return True

    except:
        # 如果發生異常，顯示錯誤消息
        print("找不到登出按鈕")
        return False

def translate(file):
    img = Image.open(file)
    text = pytesseract.image_to_string(img, lang='eng')
    return text  


def login(cnt):

    print(f"正在破解登入...(第 {cnt} 次)")

    account_box, password_box, vcode_box = Get_boxes()
    vcode_element = Get_vcode_element()

    account_box.clear()
    password_box.clear()
    vcode_box.clear()
    vcode = getvcode(vcode_element)
    
    print("vcode: ", vcode)

    if vcode.strip() == "":
        refresh = driver.find_element(By.XPATH, "//input[@id='ctl00_Login1_ImageButton1']")
        refresh.click()
        account_box, password_box, vcode_box = Get_boxes()
        vcode_element = Get_vcode_element()
        vcode = getvcode(vcode_element)


    account_box.send_keys(User.account)
    password_box.send_keys(User.password)
    vcode_box.send_keys(vcode)

    if checklog() == True:
        return

    print("正在登入中...")
    time.sleep(.5)
    login(cnt + 1)
    
    return


def subscribe():
    global Logout_button
    ToSelectTab = driver.find_element(By.XPATH, "//a[@id='ctl00_MainContent_TabContainer1_tabCourseSearch_wcCourseSearch_lbtnGoToSelectedTab']")
    ToSelectTab.click()
    index = 0
    while True:
        subscribe_buttons = driver.find_elements(By.XPATH, "//input[@value='加選']")

        if len(subscribe_buttons) <= 0:
            break

        
        index %= len(subscribe_buttons)
        button = subscribe_buttons[index]
        index += 1

        msg = driver.find_element(By.XPATH, "//span[@id='ctl00_MainContent_TabContainer1_tabSelected_lblMsgBlock']")
        msg = msg.text

        if msg.find("短時間內發出過量需求") != -1:
            print("正在解決防搶課機制...\n" + "重新登入中...")
            Logout_button = Get_Logout_button()
            Logout_button.click()
            login(1)
            ToSelectTab = driver.find_element(By.XPATH, "//a[@id='ctl00_MainContent_TabContainer1_tabCourseSearch_wcCourseSearch_lbtnGoToSelectedTab']")
            ToSelectTab.click()
        
        else:
            button.click()
            print(msg)
        
    return

def getvcode(vcode_element):
    driver.save_screenshot('../image/screenshot.png')
    shift_x = 90
    shift_y = 250
    left = vcode_element.location['x'] + shift_x
    right = left + vcode_element.size['width'] + shift_x - 40
    top = vcode_element.location['y'] + shift_y
    bottom = top + vcode_element.size['height'] + shift_y/8 - 15
    print(f"正在擷取圖片...({left}, {top}, {right}, {bottom})")
    img = Image.open('../image/screenshot.png')
    img = img.crop((left, top, right, bottom))
    img.save('../image/catupa.png')
    print("圖片已存到 ../image/catupa.png")
    return translate('../image/catupa.png')
    

def main():
    global driver
    driver.get(Course_RUL)
    # driver.execute_script('document.body.style.zoom="1.25"')
    driver.maximize_window()
    
    login(1)
    subscribe()

    time.sleep(1000)

    return


if __name__ == "__main__":
    main()
    
