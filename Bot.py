import os
import time
import shutil
import userinfo
import urllib.request
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

class Instagram_Bot:
    driver_path = "chromedriver.exe"

    def __init__(self, username, password):
        self.username = username
        self.password = password

        self.follwers = []
        self.following = []
        self.blacklist = {} #users who you follow but don't follow you back !

        options = webdriver.ChromeOptions()
        self.browser = webdriver.Chrome(Instagram_Bot.driver_path, options=options)

    def sign_in(self):
        self.browser.get("https://www.instagram.com/")
        time.sleep(3)
        usernameInput = self.browser.find_element("name", "username")
        passwordInput = self.browser.find_element("name", "password")
        print("INFO :: Program opened the login page")
        usernameInput.send_keys(self.username)
        passwordInput.send_keys(self.password)
        print("INFO :: Program have entered the user information")
        passwordInput.send_keys(Keys.ENTER)
        time.sleep(10)
        #
        if self.browser.find_element(By.CLASS_NAME, "_ac8f"):
            print("INFO :: Box-1")
            val = self.browser.find_element(By.CLASS_NAME, "_ac8f")
            val.find_element(By.TAG_NAME, "button").click()
            time.sleep(1)
        #
        if self.browser.find_element(By.XPATH, '/html/body/div[1]/div/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]/button[2]'):
            print("INFO :: Box-2")
            self.browser.find_element(By.XPATH, '/html/body/div[1]/div/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]/button[2]').click()
            time.sleep(1)

    def get_my_folowers(self):
        self.browser.get("https://www.instagram.com/{}/followers/".format(self.username))
        print("\nINFO :: Program have opened followers list")
        time.sleep(5)
        scrollBar = self.browser.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[2]")
        print("INFO :: Scrolling have started")
        last_ht, ht = 0, 1
        while last_ht != ht:
            last_ht = ht
            time.sleep(2)
            # scroll down and retrun the height of scroll (JS script)
            ht = self.browser.execute_script(""" 
                arguments[0].scrollTo(0, arguments[0].scrollHeight);
                return arguments[0].scrollHeight; """, scrollBar)
        print("INFO :: Program have finished scrolling")
        print("INFO :: Extracting followers")
        links = scrollBar.find_elements(By.TAG_NAME, 'a')
        time.sleep(3)
        names = [name.text for name in links if name.text != '']
        #print(names)
        self.follwers = names
        print("INFO :: Extracting completed\n\t\tYou have {} followers".format(len(names)))

    def get_my_following(self):
        self.browser.get("https://www.instagram.com/{}/following/".format(self.username))
        print("\nINFO :: Program have opened following list")
        time.sleep(5)
        scrollBar = self.browser.find_element(By.XPATH,"/html/body/div[1]/div/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]")
        last_ht, ht = 0, 1
        print("INFO :: Scrolling have started")
        while last_ht != ht:
            last_ht = ht
            time.sleep(2)
            # scroll down and retrun the height of scroll (JS script)
            ht = self.browser.execute_script(""" 
                        arguments[0].scrollTo(0, arguments[0].scrollHeight);
                        return arguments[0].scrollHeight; """, scrollBar)
        print("INFO :: Program have finished scrolling")
        print("INFO :: Extracting followings")
        links = scrollBar.find_elements(By.TAG_NAME, 'a')
        time.sleep(3)
        names = [name.text for name in links if name.text != '']
        # print(names)
        self.following = names
        print("INFO :: Extracting completed\n\t\tYou are following {} accounts".format(len(names)))

    def who_is_not_following(self):
        self.get_my_folowers()
        self.get_my_following()
        results = []
        for target in self.following:
            cnt = 0
            for name in self.follwers:
                if target == name:
                    cnt+=1
            if cnt == 0:
                results.append(target)

        print("\n====== BLACKLIST ======")
        id = 0
        for i in results:
            print("ID:",id, "User:",i)
            self.blacklist[id] = i
            id += 1

        print("\nDo you want to unfollow someone ? [Y/N]")
        answer = input("> ")
        if answer == "y" or answer == "Y":
            print("Please enter ID numbers (with spaces) you want to unfollow")
            ids = input("=> ")
            liste = ids.split()
            self.unfollow_users(liste)
        else:
            print("INFO :: Process have finished")

    def get_followers(self, username):
        self.browser.get("https://www.instagram.com/{}/followers/".format(username))
        print("\nINFO :: Program have opened followers list")
        time.sleep(5)
        scrollBar = self.browser.find_element(By.XPATH,
                                              "/html/body/div[1]/div/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[2]")
        print("INFO :: Scrolling have started")
        last_ht, ht = 0, 1
        while last_ht != ht:
            last_ht = ht
            time.sleep(2)
            # scroll down and retrun the height of scroll (JS script)
            ht = self.browser.execute_script(""" 
                           arguments[0].scrollTo(0, arguments[0].scrollHeight);
                           return arguments[0].scrollHeight; """, scrollBar)
        print("INFO :: Program have finished scrolling")
        print("INFO :: Extracting followers")
        links = scrollBar.find_elements(By.TAG_NAME, 'a')
        time.sleep(3)
        names = [name.text for name in links if name.text != '']
        # print(names)
        print("INFO :: Extracting completed\n\t\t{} has {} followers".format(username, (names)))
        return names

    def get_following(self, username):
        self.browser.get("https://www.instagram.com/{}/following/".format(username))
        print("\nINFO :: Program have opened following list")
        time.sleep(5)
        scrollBar = self.browser.find_element(By.XPATH,
                                              "/html/body/div[1]/div/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]")
        last_ht, ht = 0, 1
        verified = []
        print("INFO :: Scrolling have started")
        while last_ht != ht:
            last_ht = ht
            time.sleep(2)
            # scroll down and retrun the height of scroll (JS script)
            ht = self.browser.execute_script(""" 
                                  arguments[0].scrollTo(0, arguments[0].scrollHeight);
                                  return arguments[0].scrollHeight; """, scrollBar)
        print("INFO :: Program have finished scrolling")
        print("INFO :: Extracting followings")
        links = scrollBar.find_elements(By.TAG_NAME, 'a')
        time.sleep(3)
        names = [name.text for name in links if name.text != '']
        # print(names)
        for name in names:
            val = name.split("\n")
            if len(val) > 1:
                index = names.index(name)
                names[index] = val[0]
                verified.append(val[0])

        return names, verified

    def unfollow_user(self, username):
        self.browser.get("https://www.instagram.com/{}/".format(username))
        print("\nINFO :: Program have entered {} account page".format(username))
        time.sleep(3)
        btn = self.browser.find_element(By.TAG_NAME, 'button') #sayfadaki ilk buton
        if btn.text == "Mesaj Gönder":
            self.browser.find_elements(By.TAG_NAME, 'button')[1].click()
            time.sleep(1)
            self.browser.find_element(By.CSS_SELECTOR, 'div[role=dialog] button').click()
            print("INFO :: Account succsefully unfollowed")
        else:
            print("INFO :: You don't follow the account")

    def unfollow_users(self, ids):
        for i in ids:
            target = self.blacklist[int(i)]
            self.unfollow_user(target)

    def message(self,account, message):
        print("\nINFO :: {} message process has been started".format(account))
        self.browser.get("https://www.instagram.com/{}/".format(account))
        time.sleep(3)
        btn = self.browser.find_element(By.TAG_NAME, 'button')  # sayfadaki ilk buton
        if btn.text == "Mesaj Gönder":
            btn.click()
            time.sleep(5)
            textbox = self.browser.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/div[1]/section/div/div[2]/div/div/div[2]/div[2]/div/div[2]/div/div/div[2]/textarea")
            textbox.send_keys(message)
            textbox.send_keys(Keys.ENTER)
            print("INFO :: Mesage has been sent to {}".format(account))
        else:
            print("INFO :: This account is private and you don't follow it")

    def send_to_all(self, accounts, message):
        for account in accounts:
            self.message(account, message)