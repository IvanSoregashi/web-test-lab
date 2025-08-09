import pytest
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import time


def test_title(the_internet: WebDriver):
    assert the_internet.title == "The Internet"


def test_adding_elements(add_remove_page: WebDriver):
    for _ in range(5):
        add_remove_page.find_element(By.XPATH, "//button[text()='Add Element']").click()
    assert len(add_remove_page.find_elements(By.XPATH, "//button[text()='Delete']")) == 5


def test_removing_elements(add_remove_page: WebDriver):
    for _ in range(5):
        add_remove_page.find_element(By.XPATH, "//button[text()='Add Element']").click()
    for _ in range(5):
        add_remove_page.find_element(By.XPATH, "//button[text()='Delete']").click()
    with pytest.raises(NoSuchElementException):
        add_remove_page.find_element(By.XPATH, "//button[text()='Delete']")


def test_basic_auth_success(basic_auth_page: WebDriver):
    assert basic_auth_page.find_element(By.CSS_SELECTOR, "div.example p").text == "Congratulations! You must have the proper credentials."