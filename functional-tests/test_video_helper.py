import os
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def test_before_next(browser, screenshot):
    # only testing Vimeo because YouTube isn't expected to be used anymore
    # and the test is very flaky
    wait = WebDriverWait(browser, 10)

    browser.get(
        'http://localhost:8000/static/panel_randomizer_app/vimeo_test.html')

    next_button = wait.until(
        EC.presence_of_element_located((By.CLASS_NAME, "fake-button"))
    )

    screenshot.save('ready')

    assert next_button
    next_button.click()

    filepath = screenshot.save('clicked')
    # expect that the complexity of the picture is higher (because a video is playing)
    assert os.path.getsize(filepath) >= 32000

    if not 'TRAVIS' in os.environ:
        # for some reason the end of playback isn't triggered in Travis
        message = wait.until(
            EC.text_to_be_present_in_element((By.ID, "message"), 'Next question!'))
        assert message
