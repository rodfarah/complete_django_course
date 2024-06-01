import os
from dotenv import load_dotenv
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.service import Service


ROOT_PATH = Path(__file__).parent.parent
load_dotenv()
CHROMEDRIVER_NAME = os.environ.get('CHROMEDRIVER_NAME')
CHROMEDRIVER_PATH = ROOT_PATH / 'bin' / CHROMEDRIVER_NAME

# --headless (does not open browser)


def make_chrome_browser(*options):
    chrome_options = webdriver.ChromeOptions()
    for option in options:
        chrome_options.add_argument(option)
    if os.environ.get('SELENIUM_HEADLESS') == '1':
        chrome_options.add_argument('--headless')
    chrome_service = Service(executable_path=CHROMEDRIVER_PATH)
    browser = webdriver.Chrome(service=chrome_service, options=chrome_options)
    return browser


if __name__ == '__main__':
    browser = make_chrome_browser('--headless')
    browser.get('https://www.twoofus.com.br')
    browser.sleep(5)
    browser.quit()
