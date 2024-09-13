from google_automation import GoogleAutomation
from settings import config
from twitter_automation import TwitterAutomation
from utils import initialize_driver, read_file


def main():
    driver = initialize_driver(read_file(config.proxy_path), read_file(config.user_agent_path), config.driver_path)
    try:
        choice = input("Выберите вариант:\n1. Google\n2. Twitter")
        if choice == '1':
            google_automation = GoogleAutomation(driver)
            google_option = input("Выберите вариант: 1 - Сменить пароль, 2 - Изменить логин, 3 - Сохранить данные в таблицу: ")

            if google_option == '1':
                google_automation.change_password()
            elif google_option == '2':
                google_automation.change_username()
            elif google_option == '3':
                google_automation.save_data_to_table()

        elif choice == '2':
            twitter_automation = TwitterAutomation(driver)
            twitter_option = input("Выберите вариант: 1 - Сменить пароль, 2 - случайный твит")

            if twitter_option == '1':
                twitter_automation.change_password()
            elif twitter_option == '2':
                twitter_automation.make_random_tweet()

        else:
            print("Неверный выбор, завершение программы")
    except Exception as e:
        print(f"Произошла непредвиденная ошибка {e}\nЗавершение работы программы")


if __name__ == "__main__":
    main()
