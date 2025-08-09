import pytest
from typing import Generator
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from settings import Config


@pytest.fixture(scope="session")
def config() -> Config:
    return Config.load()


@pytest.fixture(scope="function")
def driver(config: Config, request: pytest.FixtureRequest) -> Generator[WebDriver, None, None]:
    browser = config.browser.NAME
    
    match browser:
        case "chrome":
            options = webdriver.ChromeOptions()
            for option in config.browser.OPTIONS_CHROME.split(";"):
                options.add_argument(option)
            driver = webdriver.Chrome(options=options)
        case "firefox":
            options = webdriver.FirefoxOptions()
            for option in config.browser.OPTIONS_FIREFOX.split(";"):
                options.add_argument(option)
            driver = webdriver.Firefox(options=options)
        case "edge":
            options = webdriver.EdgeOptions()
            for option in config.browser.OPTIONS_EDGE.split(";"):
                options.add_argument(option)
            driver = webdriver.Edge(options=options)
        case _:
            raise ValueError(f"Invalid browser: {browser}")
    
    yield driver
    
    driver.quit()


@pytest.fixture(scope="function")
def the_internet(driver: WebDriver, config: Config) -> WebDriver:
    driver.get(config.the_internet.base_url)
    return driver


@pytest.fixture(scope="function")
def add_remove_page(the_internet: WebDriver) -> WebDriver:
    the_internet.find_element(By.LINK_TEXT, "Add/Remove Elements").click()
    return the_internet


@pytest.fixture(scope="function")
def basic_auth_page(driver: WebDriver, config: Config) -> WebDriver:
    driver.get(config.the_internet.basic_auth_url)
    return driver
