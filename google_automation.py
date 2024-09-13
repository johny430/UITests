import os

import gspread
import requests
from google.oauth2.service_account import Credentials
from selenium.webdriver.common.by import By
from twocaptcha import TwoCaptcha

import utils
from settings import config


class GoogleAutomation:
    def __init__(self, driver):
        self.driver = driver
        self.solver = TwoCaptcha(config.two_captcha_api_key)
        self.username, self.password = utils.load_credentials(config.google_credentials_path)

    def login(self):
        """Вход в аккаунт"""
        self.driver.get("https://accounts.google.com/v3/signin/identifier?...")

        if self.driver.find_element(By.CSS_SELECTOR, ".gb_Ld") is None:
            self.driver.find_element(By.CSS_SELECTOR, ".identifierId").send_keys(self.username)
            self.driver.find_element(By.CSS_SELECTOR, ".VfPpkd-vQzf8d").click()
            self.driver.find_element(By.CSS_SELECTOR, ".whsOnd.zHQkBf").send_keys(self.password)
            self.driver.find_element(By.CSS_SELECTOR, ".VfPpkd-RLmnJb").click()

            image_element = self.driver.find_element(By.CSS_SELECTOR, '.img.f4ZpM.TrZEUc')
            image_url = image_element.get_attribute('src')
            image_data = requests.get(image_url).content
            with open('captcha.png', 'wb') as file:
                file.write(image_data)
            result = self.solver.normal(image_data)
            os.remove('captcha.png')

            self.driver.find_element(By.CSS_SELECTOR, ".dMNVAe").send_keys(result['code'])
            self.driver.find_element(By.CSS_SELECTOR, ".VfPpkd-vQzf8d").click()

        print("Вход в гугл аккаунт проведен успешно")

    def change_password(self):
        """Изменение пароля"""
        self.login()
        self.driver.get("https://myaccount.google.com/u/2/signinoptions/password?...")

        new_password = input("Enter new password: ")
        inputs = self.driver.find_elements(By.CSS_SELECTOR, ".VfPpkd-fmcmS-wGMbrd.uafD5")
        inputs[0].send_keys(self.password)
        inputs[1].send_keys(new_password)
        self.driver.find_element(By.CSS_SELECTOR, ".UywwFc-RLmnJb").click()

        self.update_credentials(new_password)
        print("Пароль успешно изменен")

    def update_credentials(self, new_password):
        """Перезапись логина и пароля в файл"""
        with open(config.google_credentials_path, 'w', encoding='utf-8') as file:
            file.write(f"{self.username}\n")
            file.write(f"{new_password}\n")

    def change_username(self):
        """Изменить  Имени и Фамилии"""
        self.login()
        self.driver.get("https://myaccount.google.com/u/2/profile/name/edit?...")

        info = input("Enter new name and surname (separated by space): ")
        name, surname = info.split(" ")
        inputs = self.driver.find_elements(By.CSS_SELECTOR, ".VfPpkd-fmcmS-wGMbrd")
        inputs[0].send_keys(name)
        inputs[1].send_keys(surname)
        self.driver.find_element(By.CSS_SELECTOR, ".VfPpkd-dgl2Hf-ppHlrf-sM5MNb").click()
        print("Имя и фамилия успешно изменены")

    def save_data_to_table(self):
        """Сохранение данных в таблицу – Емейл, пароль, Имя фамилия, дата рождения, резервный емейл"""
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = Credentials.from_service_account_file(config.google_sheet_credentials_path, scopes=scope)
        client = gspread.authorize(creds)

        self.login()
        table_name = input("Введите название таблицы: ")
        worksheet_name = input("Введите название страницы: ")
        sheet = client.open(table_name).worksheet(worksheet_name)

        # Получение персональных данных
        self.driver.get("https://myaccount.google.com/u/2/personal-info?...")
        info = self.driver.find_elements(By.CSS_SELECTOR, ".bJCr1d")
        name = info[4].text.split(" ")[0]
        surname = info[4].text.split(" ")[1]
        birthday = info[5].text

        # Получение резервного емаил
        self.driver.get("https://myaccount.google.com/u/2/security?...")
        security_info = self.driver.find_elements(By.CSS_SELECTOR, ".kFNik")
        backup_email = security_info[3].text if security_info[3].text != "Добавьте адрес электронной почты" else "Not provided"

        # Сохранение в таблицу
        column_a_values = sheet.col_values(1)
        last_row = len(column_a_values) + 1
        values = [[name, surname, self.username, self.password, birthday, backup_email]]
        sheet.update(f"A{last_row}:F{last_row}", values)
        print("Данные успешно сохранены в таблицу")
