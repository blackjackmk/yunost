from selenium import webdriver
import os
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.keys import Keys
import requests

from conf import wks, insta_log, insta_pass
 
def send_insta(foto, text):
    global insta_accounts
    insta_accounts = set()
    insta_accounts = wks.get("D2:D")
    #save image
    response = requests.get(foto)
    if response.status_code == 200:
        with open("image.jpg", "wb") as f:
            f.write(response.content)
    else:
        print("Error downloading image. Status code:", response.status_code)
        return False

    if init(insta_accounts, text):
        return True
    else:
        return False


class bot:
    def __init__(self, username, password, insta_accounts, message):
        self.username = username
        self.password = password
        self.insta_accounts = insta_accounts
        self.message = message
        self.base_url = 'https://www.instagram.com/'
        self.bot = driver
        self.login()
 
    def login(self):
        self.bot.get(self.base_url)
 
        enter_username = WebDriverWait(self.bot, 20).until(
            expected_conditions.presence_of_element_located((By.NAME, 'username')))
        enter_username.send_keys(self.username)
        enter_password = WebDriverWait(self.bot, 20).until(
            expected_conditions.presence_of_element_located((By.NAME, 'password')))
        enter_password.send_keys(self.password)
        enter_password.send_keys(Keys.RETURN)
        time.sleep(5)

        try:#if onetap works
            #cookie
            self.bot.find_element(By.XPATH, '/html/body/div[2]/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/button[2]').click()
            time.sleep(5)

            #click log in btn
            self.bot.find_element(By.XPATH,
                              '/html/body/div[2]/div/div/div[1]/div/div/div/div[1]/section/main/article/div[2]/div[1]/div[2]/form/div/div[3]/button').click()
            time.sleep(5)
        except:
            pass

        #save data ?
        self.bot.find_element(By.XPATH,
                              '/html/body/div[2]/div/div/div[1]/div/div/div/div[1]/div[1]/div[2]/section/main/div/div/div/div/div').click()
        time.sleep(5)

        #second popup
        self.bot.find_element(By.XPATH,
                              '/html/body/div[2]/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]/button[2]').click()
        time.sleep(5)

        print("Loginned. Start posting")

        # direct button
        self.bot.find_element(By.XPATH,
                              '/html/body/div[2]/div/div/div[1]/div/div/div/div[1]/div[1]/div[1]/div/div/div/div/div[2]/div[5]/div/a/div').click()
        time.sleep(3)
 
        # clicks on pencil icon
        self.bot.find_element(By.XPATH,
                              '/html/body/div[2]/div/div/div[1]/div/div/div/div[1]/div[1]/div/div[2]/div/section/div/div/div/div/div[1]/div[1]/div/div[3]/button').click()
        time.sleep(2)
        for m in insta_accounts:
 
             # enter the username
            self.bot.find_element(By.XPATH,
                                  '/html/body/div[2]/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div[2]/div[1]/div/div[2]/input').send_keys(m)
            time.sleep(3)
            try:
                # click on the username
                self.bot.find_element(By.XPATH,
                                    '/html/body/div[2]/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div[2]/div[2]/div/div[1]/div/div/div[3]/div/button').click()
                time.sleep(4)
            except:#if user doesn't exist
                self.bot.find_element(By.XPATH,
                                  '/html/body/div[2]/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div[2]/div[1]/div/div[2]/input').clear()
                print("Unknown user: "+m)
                continue
            # next button
            self.bot.find_element(By.XPATH,
                                  '/html/body/div[2]/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div[1]/div/div[3]/div/button').click()
            time.sleep(4)
 
            # click on message area
            send = self.bot.find_element(By.XPATH,
                                         '/html/body/div[2]/div/div/div[1]/div/div/div/div[1]/div[1]/div/div[2]/div/section/div/div/div/div/div[2]/div[2]/div/div[2]/div/div/div[2]/textarea')

            #send_photo
            file_input = self.bot.find_element(By.XPATH, "//input[@type='file']")
            path = os.getcwd()
            path += '\image.jpg'
            time.sleep(5)
            file_input.send_keys(path) 
            time.sleep(8)
 
            # types message
            send.send_keys(self.message)
            time.sleep(3)
 
            # send message
            send.send_keys(Keys.RETURN)
            time.sleep(3)
            # clicks on direct option or pencil icon
            self.bot.find_element(By.XPATH,
                                  '/html/body/div[2]/div/div/div[1]/div/div/div/div[1]/div[1]/div/div[2]/div/section/div/div/div/div/div[1]/div[1]/div/div[3]/button').click()
            time.sleep(4)
 
 
def init(spis, tekst):
    global driver
    options = webdriver.FirefoxOptions()
    options.add_argument('-headless')

    driver = webdriver.Firefox(options=options)
    try:
        bot(insta_log, insta_pass, spis, tekst)
        driver.quit()
        print("Work finished");
        return True
    except:
        print("Error stop");
        return False

#send_insta("https://cdn.cmc-gallery.pl/static/files/gallery/541/090d434854e917828ad11e48812db01d.jpg", "🔞test")