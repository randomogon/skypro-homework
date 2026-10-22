
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def test_shop():
    driver = webdriver.Firefox()
    total = None

    try:
        driver.get("https://www.saucedemo.com/")

        wait = WebDriverWait(driver, 15)

        wait.until(
            EC.visibility_of_element_located((By.ID, "user-name"))
        ).send_keys("standard_user")

        driver.find_element(
            By.ID, "password"
        ).send_keys("secret_sauce")

        driver.find_element(By.ID, "login-button").click()

        wait.until(
            EC.visibility_of_element_located(
                (By.ID, "add-to-cart-sauce-labs-backpack")
            )
        )

        products = [
            "add-to-cart-sauce-labs-backpack",
            "add-to-cart-sauce-labs-bolt-t-shirt",
            "add-to-cart-sauce-labs-onesie",
        ]

        for product_id in products:
            wait.until(
                EC.element_to_be_clickable((By.ID, product_id))
            ).click()

        wait.until(
            EC.element_to_be_clickable(
                (By.CLASS_NAME, "shopping_cart_link")
            )
        ).click()

        wait.until(
            EC.element_to_be_clickable((By.ID, "checkout"))
        ).click()

        wait.until(
            EC.visibility_of_element_located((By.ID, "first-name"))
        ).send_keys("Alex")

        driver.find_element(
            By.ID, "last-name"
        ).send_keys("Tester")

        driver.find_element(
            By.ID, "postal-code"
        ).send_keys("12345")

        driver.find_element(By.ID, "continue").click()

        total_element = wait.until(
            EC.visibility_of_element_located(
                (By.CLASS_NAME, "summary_total_label")
            )
        )

        wait.until(
            lambda browser: browser.find_element(
                By.CLASS_NAME, "summary_total_label"
            ).text.strip() == "Total: $58.29"
        )

        total = total_element.text.strip()

    finally:
        driver.quit()

    assert total == "Total: $58.29", (
        f"Ожидали Total: $58.29, получили {total}"
    )
