import pytest
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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


def test_context_menu(context_menu_page: WebDriver):
    element = context_menu_page.find_element(By.ID, "hot-spot")
    ActionChains(context_menu_page).context_click(element).perform()
    WebDriverWait(context_menu_page, 2).until(EC.alert_is_present())
    assert EC.alert_is_present()(context_menu_page)
    context_menu_page.switch_to.alert.accept()
    assert not EC.alert_is_present()(context_menu_page)


def test_drag_and_drop(drag_and_drop_page: WebDriver):
    column_a = drag_and_drop_page.find_element(By.ID, "column-a")
    column_b = drag_and_drop_page.find_element(By.ID, "column-b")
    assert column_a.text == "A"
    assert column_b.text == "B"
    ActionChains(drag_and_drop_page).drag_and_drop(column_a, column_b).pause(1).perform()
    assert column_a.text == "B"
    assert column_b.text == "A" 
    ActionChains(drag_and_drop_page).drag_and_drop(column_b, column_a).pause(1).perform()
    assert column_a.text == "A"
    assert column_b.text == "B"


def test_dropdown(dropdown_page: WebDriver):
    select = Select(dropdown_page.find_element(By.ID, "dropdown"))
    select.select_by_index(0)
    assert select.first_selected_option.text == "Please select an option"
    assert select.options[0].get_property("disabled")
    select.select_by_index(1)
    assert select.first_selected_option.text == "Option 1"
    select.select_by_index(2)
    assert select.first_selected_option.text == "Option 2"
    with pytest.raises(NotImplementedError):
        select.select_by_index(0)


def test_dynamic_controls_checkbox(dynamic_controls_page: WebDriver):
    form = dynamic_controls_page.find_element(By.CSS_SELECTOR, "form#checkbox-example")
    check_button = form.find_element(By.TAG_NAME, "button")
    assert check_button.text == "Remove"
    assert form.find_element(By.ID, "checkbox").is_displayed()
    check_button.click()
    WebDriverWait(dynamic_controls_page, 10).until(EC.invisibility_of_element((By.ID, "checkbox")))
    assert check_button.text == "Add"
    assert len(form.find_elements(By.ID, "checkbox")) == 0
    check_button.click()
    WebDriverWait(dynamic_controls_page, 10).until(EC.visibility_of_element_located((By.ID, "checkbox")))
    assert len(form.find_elements(By.ID, "checkbox")) == 1
    assert form.find_element(By.ID, "checkbox").is_displayed()
    assert form.find_element(By.ID, "checkbox").is_enabled()
    assert not form.find_element(By.ID, "checkbox").is_selected()
    assert check_button.text == "Remove"


def test_dynamic_controls_input(dynamic_controls_page: WebDriver):
    form = dynamic_controls_page.find_element(By.CSS_SELECTOR, "form#input-example")
    input_button = form.find_element(By.CSS_SELECTOR, "button")
    input_button.click()