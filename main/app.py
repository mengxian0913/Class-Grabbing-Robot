from config import User
import ddddocr
from PIL import Image
import pytesseract
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
options.add_argument("headless")
driver = webdriver.Chrome(options=options)

Course_RUL = "https://course.fcu.edu.tw/"
Logout_button = None
webwait = 5
ok = False

def clear(): os.system('clear')

def Get_Logout_button():
    return driver.find_element(By.XPATH, "//input[@name='ctl00$btnLogout']")

def Get_boxes():
    return [
        WebDriverWait(driver, webwait).until(
                EC.presence_of_element_located((By.XPATH, "//input[@id='ctl00_Login1_UserName']"))
        ),
        WebDriverWait(driver, webwait).until(
                EC.presence_of_element_located((By.XPATH, "//input[@id='ctl00_Login1_Password']"))
        ),
        WebDriverWait(driver, webwait).until(
                EC.presence_of_element_located((By.XPATH, "//input[@id='ctl00_Login1_vcode']"))
        ),
        WebDriverWait(driver, webwait).until(
                EC.presence_of_element_located((By.XPATH, "//img[@id='ctl00_Login1_Image1']"))
        )
    ]

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
    ocr = ddddocr.DdddOcr()
    res = ocr.classification(img)
    print('识别出的验证码为：' + res)
    # text = pytesseract.image_to_string(img, lang='eng')
    return res

broken = False

def login(cnt):
    global broken

    if broken:
        return

    try:

        print(f"正在破解登入...(第 {cnt} 次)")

        account_box, password_box, vcode_box, vcode_element = Get_boxes()

        account_box.clear()
        password_box.clear()
        vcode_box.clear()
        vcode = getvcode(vcode_element)
        
        print("vcode: ", vcode)

        if vcode.strip() == "":
            refresh = driver.find_element(By.XPATH, "//input[@id='ctl00_Login1_ImageButton1']")
            refresh.click()
            account_box, password_box, vcode_box, vcode_element = Get_boxes()
            vcode = getvcode(vcode_element)


        account_box.send_keys(User.account)
        password_box.send_keys(User.password)
        vcode_box.send_keys(vcode)

        if checklog() == True:
            return

        print("正在登入中...")
        time.sleep(.5)
        login(cnt + 1)
    
    except:
        broken = True
        print("連線逾時٩(ŏ﹏ŏ、)۶\n重新導向中...")
        return

    return


def subscribe():
    global Logout_button, ok
    ToSelectTab = driver.find_element(By.XPATH, "//a[@id='ctl00_MainContent_TabContainer1_tabCourseSearch_wcCourseSearch_lbtnGoToSelectedTab']")
    ToSelectTab.click()
    index = 0
    while True:
        subscribe_buttons = driver.find_elements(By.XPATH, "//input[@value='加選']")

        if len(subscribe_buttons) <= 0:
            ok = True
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
            if broken:
                return
            ToSelectTab = driver.find_element(By.XPATH, "//a[@id='ctl00_MainContent_TabContainer1_tabCourseSearch_wcCourseSearch_lbtnGoToSelectedTab']")
            ToSelectTab.click()
        
        else:
            button.click()
            print(msg)
        
    return

def getvcode(vcode_element):
    driver.save_screenshot('../image/screenshot.png')
    
    shift_x = 85 # 90
    shift_y = 245 # 250
    left = vcode_element.location['x']# + shift_x
    right = left + vcode_element.size['width']# + shift_x - 40
    top = vcode_element.location['y']# + shift_y
    bottom = top + vcode_element.size['height']# + shift_y/8 - 15
    print(f"正在擷取圖片...({left}, {top}, {right}, {bottom})")
    img = Image.open('../image/screenshot.png')
    img = img.crop((left, top, right, bottom))
    img.save('../image/catupa.png')
    print("圖片已存到 ../image/catupa.png")
    return translate('../image/catupa.png')
    

def main():

    global driver, broken

    while not ok:
        broken = False
        try:
            print('正在獲取網站資源...')
            driver.get(Course_RUL)
            # driver.maximize_window()
        except:
            continue

        login(1)
        subscribe()    

    print("任務完成")
    time.sleep(1000)

    return


if __name__ == "__main__":
    main()
    
