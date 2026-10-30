
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class CalculatorPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 60)

    def open(self):
        self.driver.get(
            "https://bonigarcia.dev/selenium-webdriver-java/"
            "slow-calculator.html"
        )

    def set_delay(self, seconds):
        delay = self.wait.until(
            EC.visibility_of_element_located((By.ID, "delay"))
        )
        delay.clear()
        delay.send_keys(str(seconds))

    def click_button(self, button):
        self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, f"//span[text()='{button}']")
            )
        ).click()

    def get_result(self, expected_result):
        self.wait.until(
            lambda driver: driver.find_element(
                By.CLASS_NAME, "screen"
            ).text.strip() == str(expected_result)
        )

        return self.driver.find_element(
            By.CLASS_NAME, "screen"
        ).text.strip()
