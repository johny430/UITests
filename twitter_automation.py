import openai
from selenium.webdriver.common.by import By

import utils
from settings import config


class TwitterAutomation:
    def __init__(self, driver):
        self.driver = driver
        self.username, self.password = utils.load_credentials(config.twitter_credentials_path)

    def login(self):
        """Вход в Twitter"""
        self.driver.get(r"https://x.com/i/flow/login?redirect_after_login=%2Fx_login")

        if self.driver.find_element(By.CSS_SELECTOR, ".css-1jxf684.r-bcqeeo.r-1ttztb7.r-qvutc0.r-poiln3") is not None:
            return

        self.driver.find_element(By.CSS_SELECTOR, ".r-30o5oe.r-1dz5y72.r-13qz1uu.r-1niwhzg.r-17gur6a.r-1yadl64.r-deolkf.r-homxoj.r-poiln3.r-7cikom.r-1ny4l3l.r-t60dpp.r-fdjqy7").send_key(self.username)
        self.driver.find_element(By.CSS_SELECTOR, ".css-1jxf684.r-bcqeeo.r-1ttztb7.r-qvutc0.r-poiln3").click()
        self.enter_password(self.password)
        while True:
            if self.driver.find_element(By.CSS_SELECTOR, ".css-1jxf684.r-bcqeeo.r-1ttztb7.r-qvutc0.r-poiln3") is not None:
                break
            self.enter_password(input("Пароль в файле не верный.\nВведите верный пароль заново"))

    def enter_password(self, password):
        self.driver.find_element(By.CSS_SELECTOR, ".r-30o5o.r-1dz5y72.r-13qz1uu.r-1niwhzg.r-17gur6a.r-1yadl64.r-deolkf.r-homxoj.r-poiln3.r-7cikom.r-1ny4l3l.r-t60dpp.r-fdjqy7").send_key(password)
        self.driver.find_element(By.CSS_SELECTOR, ".css-146c3p1.r-bcqeeo.r-qvutc0.r-37j5jr.r-q4m81j.r-a023e6.r-rjixqe.r-b88u0q.r-1awozwy.r-6koalj.r-18u37iz.r-16y2uox.r-1777fci").click()

    def change_password(self):
        """Изменить пароль Twitter"""
        self.login()
        self.driver.get(r"https://x.com/settings/password")

        while True:
            new_password = input("Введите новый пароль: ")
            inputs = self.driver.find_elements(By.CSS_SELECTOR, ".r-30o5oe.r-1dz5y72.r-13qz1uu.r-1niwhzg.r-17gur6a.r-1yadl64.r-deolkf.r-homxoj.r-poiln3.r-7cikom.r-1ny4l3l.r-t60dpp.r-fdjqy7")
            inputs[0].send_key(self.password)
            inputs[1].send_key(new_password)
            inputs[2].send_key(new_password)
            self.driver.find_element(By.CSS_SELECTOR, ".css-1jxf684.r-bcqeeo.r-1ttztb7.r-qvutc0.r-poiln3").click()

            if self.driver.find_element(By.CSS_SELECTOR, ".css-1jxf684.r-bcqeeo.r-1ttztb7.r-qvutc0.r-poiln3") is not None:
                print("Пароль успешно изменен")
                break

    def make_random_tweet(self):
        """Создать случайный твит с помощью ChatGPT"""
        self.login()
        self.driver.get(r"https://x.com/home?lang=en")

        self.driver.find_element(By.CSS_SELECTOR, ".css-146c3p1.r-bcqeeo.r-qvutc0.r-37j5jr.r-q4m81j.r-a023e6.r-rjixqe.r-b88u0q.r-1awozwy.r-6koalj.r-18u37iz.r-16y2uox.r-1777fci").click()
        tweet_topic = input("Тема твита: ")

        openai.api_key = config.openai_api_key
        response = openai.Completion.create(
            engine="gpt-4",
            prompt=tweet_topic,
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.7,
        )
        tweet_text = response.choices[0].text.strip()
        self.driver.find_element(By.CSS_SELECTOR, ".public-DraftStyleDefault-block.public-DraftStyleDefault-ltr").send_key(tweet_text)
        self.driver.find_element(By.CSS_SELECTOR, ".css-1jxf684.r-dnmrzs.r-1udh08x.r-3s2u2q.r-bcqeeo.r-1ttztb7.r-qvutc0.r-poiln3.r-a023e6.r-rjixqe").click()
        print(f"Создан твит с темой {tweet_topic}:\n{tweet_text}")
