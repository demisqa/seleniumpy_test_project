import os
import pytest
from dotenv import load_dotenv
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options as OptionsFirefox


def pytest_addoption(parser):
    parser.addoption('--browser_name', action='store', default='chrome',
                     help="Choose browser: chrome or firefox")
    parser.addoption('--language', action='store', default='en',
                     help="Choose user's language")

@pytest.fixture(scope="function")
def browser(request) -> webdriver:
    browser_name = request.config.getoption("browser_name")
    user_language = request.config.getoption("language")
    browser = None
    load_dotenv()
    os.environ['GH_TOKEN'] = os.getenv('GH_TOKEN')
    
    if browser_name == "chrome":
        print("\nstart chrome browser for test..")
        options = Options()
        options.add_experimental_option('prefs', {'intl.accept_languages': user_language})
        browser = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),options=options)

    elif browser_name == "firefox":
        print("\nstart firefox browser for test..")
        options_firefox = OptionsFirefox()
        options_firefox.set_preference("intl.accept_languages", user_language)
        browser = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install(),log_output='/dev/null'), options=options_firefox)
    else:
        raise pytest.UsageError("--browser_name should be chrome or firefox")
    yield browser
    print("\nquit browser..")
    browser.quit()
