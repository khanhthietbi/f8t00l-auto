from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC, wait
from selenium.common.exceptions import NoSuchElementException
import time
from selenium.webdriver.chrome.options import Options
 

content = open("1.acc.js","r")
accs = content.read().splitlines()
content = open("2.target.js","r")
targets = content.read().splitlines()
for acc in accs:
    try:
        obj = acc.split()
        usn = obj[0]
        pw = obj[1]
        if usn.startswith('//'): continue
        options = Options()
        options.headless = False
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-notifications")
        driver.minimize_window()
        stopWhenSeeLikedPost = True
        # options.add_argument("--start-maximized")
        driver = webdriver.Chrome("C:\\driver\\chromedriver.exe", options=options)
        driver.get('https://www.facebook.com/login.php?login_attempt=1&lwv=110')
        print("Opened facebook with usn {}".format(usn))
        email = driver.find_element_by_xpath("//input[@id='email' or @name='email']")
        email.send_keys(usn)
        print("email entered...")
        password = driver.find_element_by_xpath("//input[@id='pass']")
        password.send_keys(pw)
        print("Password entered...")
        button = driver.find_element_by_xpath("//button[@id='loginbutton']")
        button.click()
        print("facebook opened")
        swait = WebDriverWait(driver, 5)
        swait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'path')))
        print("redirected finish, jump to target page")
        for target in targets:
            i = 1
            if target.startswith("//"): continue
            driver.get(target)
            while True:
                try:
                    parent = 'div[aria-posinset="{}"]'.format(i) if target.count('/') < 4 else 'div[role="complementary"]'
                    child = 'div[aria-label="Like"]'
                    swait.until(EC.presence_of_element_located((By.CSS_SELECTOR, parent)))
                    print("done wait parent of {}".format(i))
                    
                    # Default 10 posts like in a row
                    script = """
                        el = document.querySelector(\'{} {}\');
                        if (el) {{
                            el.scrollIntoView();
                            el.click();
                        }}
                        """.format(parent, child)

                    # Without check the script will thow exception, which lead to stop the loop
                    if stopWhenSeeLikedPost: 
                        script = """"
                            el = document.querySelector(\'{} {}\');
                            el.scrollIntoView();
                            el.click();
                        """

                    driver.execute_script(script)
                    sleep(5)
                    driver.execute_script("window.scrollTo(0,window.scrollY + window.innerHeight - 100);")
                    
                    # Limit 10 posts like for pages profile or 1 post like for specific post
                    if target.count("/") < 4 and i < 10: i+=1 
                    else: break
                except Exception as e:
                    print(e)
                    break
            print("done loop")
            driver.close()
            driver.quit()
    except Exception as e: 
        print("Error ocurred with account {}, error: {}".format(acc, e))