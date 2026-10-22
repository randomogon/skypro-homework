from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def test_calculator():
    driver = webdriver.Chrome()

    try:
        driver.get(
            "https://bonigarcia.dev/selenium-webdriver-java/"
            "slow-calculator.html"
        )

        wait = WebDriverWait(driver, 60)

        delay = wait.until(
            EC.visibility_of_element_located((By.ID, "delay"))
        )
        delay.clear()
        delay.send_keys("45")

        buttons = ["7", "+", "8", "="]

        for button in buttons:
            wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, f"//span[text()='{button}']")
                )
            ).click()

        wait.until(
            lambda browser: browser.find_element(
                By.CLASS_NAME, "screen"
            ).text.strip() == "15"
        )

        result = driver.find_element(By.CLASS_NAME, "screen").text
        assert result == "15", (
            f"Ожидали результат 15, получили {result}"
        )

    finally:
        driver.quit()
