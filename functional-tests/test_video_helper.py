import os
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_before_next(browser):
    # only testing Vimeo because YouTube isn't expected to be used anymore
    # and the test is very flaky
    wait = WebDriverWait(browser, 10)

    browser.get('http://localhost:8000/static/panel_randomizer_app/vimeo_test.html')

    next_button = wait.until(
        EC.presence_of_element_located((By.CLASS_NAME, "fake-button"))
    )

    assert next_button
    next_button.click()

    wait.until(EC.alert_is_present())
    alert = browser.switch_to.alert
    assert alert.text == 'Next question!'
    alert.accept()
