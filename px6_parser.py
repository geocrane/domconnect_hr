from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


PATH = "https://px6.me/"


def wait_capture() -> None:
    """Ожидание и подтверждение ввода капчи."""
    input("Нажми Enter, когда CAPTURE будет пройдена")


def login_func(login: str, password: str, driver: Firefox) -> None:
    """Авторизация."""
    driver.get(PATH)
    authorization_btn = driver.find_element(By.CSS_SELECTOR, "[data-role='login']")
    authorization_btn.click()

    email_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "[name='email']"))
    )
    email_field.send_keys(login)
    password_field = driver.find_element(By.CSS_SELECTOR, "[name='password']")
    password_field.send_keys(password)

    wait_capture()

    if driver.current_url == PATH:
        login_btn = driver.find_element(
            By.XPATH, ".//button[@type='submit' and text()='Войти']"
        )
        login_btn.click()


def get_proxies_data(driver: Firefox) -> list[dict]:
    """Извлечь данные со страницы."""
    table = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CLASS_NAME, "user_proxy_table"))
    )
    proxies = []
    rows = table.find_elements(By.TAG_NAME, "tr")
    for row in rows[1:-2]:
        proxy_info = {}
        data_lists = row.find_elements(By.CLASS_NAME, "list-dotted")
        for list_ in data_lists:
            for item in list_.find_elements(By.TAG_NAME, "li"):
                left_element = item.find_element(By.CLASS_NAME, "left")
                right_element = item.find_element(By.CLASS_NAME, "right")
                key = left_element.text.strip()
                value = right_element.text.strip()
                proxy_info[key] = value
        proxies.append(proxy_info)
    return proxies


def print_data_to_console(
    data: list[dict], columns: list[str] = ["ПроксиIP:PORT", "Дата"]
) -> None:
    """Вывести данные в консоль."""
    for element in data:
        printable_data = [element[column] for column in columns]
        print(" - ".join(str(data) for data in printable_data))


def main(login: str, password: str) -> None:
    """Запустить парсинг."""
    try:
        driver = Firefox()
        login_func(login, password, driver)
        proxies_data = get_proxies_data(driver)
        print_data_to_console(proxies_data)
    except Exception as e:
        print(f"Ошибка: {e}")
    finally:
        driver.close()


if __name__ == "__main__":
    login = "tzpythondemo@domconnect.ru"
    password = "kR092IEz"

    main(login, password)
