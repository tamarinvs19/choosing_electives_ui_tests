import os
import time

import pytest
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from userconfig import UserConfig

DOWNLOAD_DIR = '/home/vyacheslav/Downloads/'
SERVER = 'http://127.0.0.1:8000/electives'


@pytest.fixture
def browser():
    driver = Chrome()
    driver.implicitly_wait(10)
    yield driver
    driver.quit()


@pytest.fixture(autouse=True, scope='session')
def config():
    config = UserConfig()
    yield config


@pytest.fixture()
def login(browser, config):
    url = f'{SERVER}/accounts/login/'
    browser.get(url)

    username_input = browser.find_element(By.ID, 'id_login')
    username_input.send_keys(config.username)

    password_input = browser.find_element(By.ID, 'id_password')
    password_input.send_keys(config.password)

    buttons = browser.find_elements(By.TAG_NAME, 'button')
    sign_up_button = buttons[-1]
    sign_up_button.send_keys(Keys.RETURN)


def test_registation(browser, config):  # Checklist 1
    personal_page_url = f'{SERVER}/users/'
    url = f'{SERVER}/users/invite/?key=NEd2vm1P4lQF.KIGZwuO7J_Srce6Bxyh93taLXoY'
    browser.get(url)

    first_name_input = browser.find_element(By.ID, 'id_first_name')
    first_name_input.send_keys(config.first_name)

    last_name_input = browser.find_element(By.ID, 'id_last_name')
    last_name_input.send_keys(config.last_name)

    username_input = browser.find_element(By.ID, 'id_username')
    username_input.send_keys(config.username)

    email_input = browser.find_element(By.ID, 'id_email')
    email_input.send_keys(config.email)

    password1_input = browser.find_element(By.ID, 'id_password1')
    password1_input.send_keys(config.password)

    password2_input = browser.find_element(By.ID, 'id_password2')
    password2_input.send_keys(config.password)

    buttons = browser.find_elements(By.TAG_NAME, 'button')
    assert len(buttons) == 2
    sign_up_button = buttons[-1]
    sign_up_button.send_keys(Keys.RETURN)

    assert browser.current_url.startswith(personal_page_url)


def test_main_page(browser, config, login):  # Checklist 2
    url = SERVER
    browser.get(url)

    thematic_headers = browser.find_elements(By.CLASS_NAME, 'thematic-name')
    assert 8 < len(thematic_headers) < 16


def test_thematic_panel(browser, config, login):  # Checklist 3
    url = SERVER
    browser.get(url)

    thematic_buttons = browser.find_elements(By.CLASS_NAME, 'accordion-button')
    button = thematic_buttons[0]
    panel = browser.find_element(By.ID, 'panelsStayOpen-collapse1')

    button.send_keys(Keys.RETURN)
    time.sleep(1)
    assert panel.value_of_css_property('display') != 'none'

    button.send_keys(Keys.RETURN)
    time.sleep(1)
    assert panel.value_of_css_property('display') == 'none'


def test_application(browser, config, login):  # Checklist 4-5
    url = SERVER
    browser.get(url)

    thematic_buttons = browser.find_elements(By.CLASS_NAME, 'accordion-button')
    thematic_buttons[0].send_keys(Keys.RETURN)
    time.sleep(1)

    kind_buttons = browser.find_elements(By.CLASS_NAME, 'checkbox-kind')
    button = [b for b in kind_buttons if not b.is_selected()][0]
    button_id = button.get_attribute('id')
    label = browser.find_element(By.CSS_SELECTOR, f'label[for={button_id}]')
    span_id = f'statistic-maybe-{button_id.split("-")[-1]}-{button_id.split("-")[1][2]}'
    maybe_statistic = browser.find_element(By.ID, span_id)
    maybe_value = int(maybe_statistic.text)

    label.click()
    time.sleep(1)
    assert int(maybe_statistic.text) - maybe_value == 1

    label.click()
    time.sleep(1)
    assert int(maybe_statistic.text) - maybe_value == 0


def test_right_column(browser, config, login):  # Checkbox 6
    url = SERVER
    browser.get(url)

    column = browser.find_element(By.CLASS_NAME, 'offcanvas')

    switch_button = browser.find_element(By.CLASS_NAME, 'switch-button')
    switch_button.send_keys(Keys.RETURN)
    assert column.value_of_css_property('visibility') != 'hidden'

    switch_button.send_keys(Keys.RETURN)
    time.sleep(0.5)
    assert column.value_of_css_property('visibility') == 'hidden'


def test_right_column_open_thematics(browser, config, login):  # Checkbox 7
    url = SERVER
    browser.get(url)

    switch_button = browser.find_element(By.CLASS_NAME, 'switch-button')
    switch_button.send_keys(Keys.RETURN)

    open_thematics_switch = browser.find_element(By.CLASS_NAME, 'switch')
    open_thematics_switch.click()
    time.sleep(0.25)

    panels = browser.find_elements(By.CLASS_NAME, 'accordion-collapse')

    for panel in panels:
        assert panel.value_of_css_property('display') != 'none'


def test_right_column_table(browser, config, login):  # Checkbox 8
    url = SERVER
    browser.get(url)

    prev_tables = []
    for file in os.listdir(DOWNLOAD_DIR):
        if 'table' in file:
            prev_tables.append(file)

    switch_button = browser.find_element(By.CLASS_NAME, 'switch-button')
    switch_button.send_keys(Keys.RETURN)

    download_link = browser.find_element(By.CSS_SELECTOR, 'a[href="/electives/download_table/"]')
    download_link.click()
    time.sleep(5.5)

    tables = []
    for file in os.listdir(DOWNLOAD_DIR):
        if 'table' in file:
            tables.append(file)

    assert len(tables) > len(prev_tables)
