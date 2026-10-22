from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def test_form():
    driver = webdriver.Edge()

    try:
        driver.get(
            "https://bonigarcia.dev/selenium-webdriver-java/data-types.html"
        )

        wait = WebDriverWait(driver, 10)

        fields = {
            "first-name": "Иван",
            "last-name": "Петров",
            "address": "Ленина, 55-3",
            "e-mail": "test@skypro.com",
            "phone": "+7985899998787",
            "city": "Москва",
            "country": "Россия",
            "job-position": "QA",
            "company": "SkyPro",
        }

        wait.until(
            EC.presence_of_element_located((By.NAME, "first-name"))
        )

        for name, value in fields.items():
            driver.find_element(By.NAME, name).send_keys(value)

        driver.find_element(By.NAME, "zip-code").clear()

        driver.find_element(
            By.CSS_SELECTOR, "button[type='submit']"
        ).click()

        wait.until(
            EC.url_contains("data-types-submitted.html")
        )

        zip_code = wait.until(
            EC.presence_of_element_located((By.ID, "zip-code"))
        )

        wait.until(
            lambda browser: "alert-danger"
            in zip_code.get_attribute("class")
        )

        assert "alert-danger" in zip_code.get_attribute("class"), (
            "Поле Zip code должно быть красным"
        )

        for name in fields:
            field = driver.find_element(By.ID, name)

            assert "alert-success" in field.get_attribute("class"), (
                f"Поле {name} должно быть зелёным"
            )

    finally:
        driver.quit()
