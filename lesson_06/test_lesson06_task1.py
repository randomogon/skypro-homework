
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def test_dynamic_loading():
    driver = webdriver.Chrome()

    try:
        url = (
            "https://the-internet.herokuapp.com/"
            "dynamic_loading/2"
        )

        for attempt in range(3):
            driver.get(url)

            try:
                wait = WebDriverWait(driver, 15)

                wait.until(
                    lambda d: d.execute_script(
                        "return typeof window.jQuery !== 'undefined'"
                    )
                )

                start_button = wait.until(
                    EC.element_to_be_clickable(
                        (By.CSS_SELECTOR, "#start button")
                    )
                )
                start_button.click()

                hello_text = wait.until(
                    EC.visibility_of_element_located(
                        (By.CSS_SELECTOR, "#finish h4")
                    )
                )

                assert hello_text.text == "Hello World!"

                assert driver.save_screenshot(
                    "lesson_06/dynamic_loading.png"
                )

                break

            except TimeoutException as error:
                if attempt == 2:
                    raise AssertionError(
                        "Сайт не завершил динамическую загрузку "
                        "после трёх попыток. Проверьте доступность "
                        "JavaScript-файлов и ошибки HTTP 503."
                    ) from error

    finally:
        driver.quit()
