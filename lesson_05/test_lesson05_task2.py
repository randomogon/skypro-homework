from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def test_form_submission():
    driver = webdriver.Chrome()
    driver.get("https://httpbin.qa-territory.online/forms/post")

    original_url = driver.current_url

    name_field = driver.find_element(By.NAME, "custname")
    name_field.send_keys("Александр")

    submit_button = driver.find_element(
        By.XPATH,
        "//button[contains(text(), 'Submit')]",
    )
    submit_button.click()

    WebDriverWait(driver, 5).until(EC.url_changes(original_url))

    assert driver.current_url.endswith("/post")

    driver.quit()
