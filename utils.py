from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service


def read_file(file_path):
    """Прочитать файл, состоящий из одной строчки"""
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.readline().strip()


def load_credentials(file_path):
    """Загрузить логин и пароль из файла"""
    with open(file_path, 'r', encoding='utf-8') as file:
        login = file.readline().strip()
        password = file.readline().strip()
    return login, password


def initialize_driver(proxy, user_agent, driver_path):
    """Создание и инициализация драйвера с полным антидетектом"""
    firefox_options = Options()
    firefox_options.set_preference("general.useragent.override", user_agent)
    firefox_options.add_argument('--headless')

    webdriver.DesiredCapabilities.FIREFOX['proxy'] = {
        "httpProxy": proxy,
        "ftpProxy": proxy,
        "sslProxy": proxy,
        "proxyType": "MANUAL",
    }

    service = Service(driver_path)
    driver = webdriver.Firefox(service=service, options=firefox_options)
    driver.implicitly_wait(30)
    return driver
