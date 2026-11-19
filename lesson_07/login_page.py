
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class LoginPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)

    def open(self):
        self.driver.get("https://www.saucedemo.com/")

    def login(self, username, password):
        self.wait.until(
            EC.visibility_of_element_located(
                (By.ID, "user-name")
            )
        ).send_keys(username)

        self.driver.find_element(
            By.ID, "password"
        ).send_keys(password)

        self.driver.find_element(
            By.ID, "login-button"
        ).click()
