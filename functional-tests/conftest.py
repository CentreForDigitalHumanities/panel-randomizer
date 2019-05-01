import os
import errno
import pytest
from datetime import datetime

from selenium import webdriver

WEBDRIVER_INI_NAME = 'webdriver'
BASE_ADDRESS_OPTION_NAME = 'base_address'


class Screenshot:
    def __init__(self, driver):
        self.driver = driver
        self.base_timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        self.iteration = 0

    def save(self, name=None):
        timestamp = f'{self.base_timestamp}-{self.iteration:04d}-{self.driver.name}'
        if name == None:
            name = timestamp
        else:
            name = timestamp + '-' + name
        self.iteration += 1

        filepath = os.path.join("screenshots", f"{name}.png")

        try:
            os.makedirs("screenshots")
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
        if not self.driver.save_screenshot(filepath):
            raise

        return filepath

def clean_test(driver):
    if driver.name != 'firefox':
        # no log in Firefox https://github.com/SeleniumHQ/selenium/issues/2972
        for entry in driver.get_log('browser'):
            print(entry)

def pytest_addoption(parser):
    """ py.test hook where we register configuration options and defaults. """
    parser.addini(
        WEBDRIVER_INI_NAME,
        'Specify browsers in which the tests should run',
        type='linelist',
        default=['Chrome', 'Firefox'],
    )
    parser.addoption(
        '--base-address',
        default='http://localhost:{{cookiecutter.backend_port}}/',
        help='specifies the base address where the application is running',
        dest=BASE_ADDRESS_OPTION_NAME,
    )


def pytest_generate_tests(metafunc):
    """ py.test hook where we inject configurable fixtures. """
    if 'webdriver_name' in metafunc.fixturenames:
        names = metafunc.config.getini(WEBDRIVER_INI_NAME)
        metafunc.parametrize('webdriver_name', names, scope='session')


@pytest.fixture(scope='session')
def webdriver_instance(webdriver_name):
    """ Provides a WebDriver instance that persists throughout the session.

        Use the `browser` fixture instead; it performs cleanups after each test.
    """
    if webdriver_name == 'Chrome':
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-gpu')
        driver = webdriver.Chrome(options=options)
    else:
        factory = getattr(webdriver, webdriver_name)
        driver = factory()
    try:
        yield driver
    finally:
        clean_test(driver)
        driver.quit()


@pytest.fixture
def browser(webdriver_instance):
    """ Provides a WebDriver instance and performs some cleanups afterwards. """
    yield webdriver_instance
    webdriver_instance.delete_all_cookies()


@pytest.fixture
def screenshot(browser):
    screenshot = Screenshot(browser)
    try:
        yield screenshot
    finally:
        screenshot.save('final')


@pytest.fixture(scope='session')
def base_address(pytestconfig):
    return pytestconfig.getoption(BASE_ADDRESS_OPTION_NAME)


@pytest.fixture
def api_address(base_address):
    return base_address + 'api/'


@pytest.fixture
def api_auth_address(base_address):
    return base_address + 'api-auth/'


@pytest.fixture
def admin_address(base_address):
    return base_address + 'admin/'
