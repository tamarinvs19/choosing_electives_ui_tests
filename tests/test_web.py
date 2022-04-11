import os
import time

import pytest
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from asserts import RegistrationAssert, MainPageAssert, ThematicPanelAssert, ApplicationAssert, RightColumnAssert, RightColumnOpenThematicsAssert, TableAssert
from config import SERVER, INVITE_KEY
from test_envs import BaseTestEnv, Registration, Login
from userconfig import UserConfig


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
    login_env = Login(browser, config)
    login_env.load()
    login_env.login()


def test_registation(browser, config):  # Checklist 1
    registration = Registration(browser, config, INVITE_KEY)
    registration.load()
    registration.registrate()

    personal_page_url = f'{SERVER}/users/'
    registration_asserts = RegistrationAssert(browser, personal_page_url)
    registration_asserts.check_url()


def test_main_page(browser, config, login):  # Checklist 2
    test_env = BaseTestEnv(browser, SERVER)
    test_env.load()

    main_page_asserts = MainPageAssert(browser)
    main_page_asserts.check_thematics_number()


def test_thematic_panel(browser, config, login):  # Checklist 3
    test_env = BaseTestEnv(browser, SERVER)
    test_env.load()

    thematic_panel_asserts = ThematicPanelAssert(browser)
    thematic_panel_asserts.check_open_panel()


def test_application(browser, config, login):  # Checklist 4-5
    test_env = BaseTestEnv(browser, SERVER)
    test_env.load()

    application_asserts = ApplicationAssert(browser)
    application_asserts.check_statistic()


def test_right_column(browser, config, login):  # Checkbox 6
    test_env = BaseTestEnv(browser, SERVER)
    test_env.load()

    right_column_asserts = RightColumnAssert(browser)
    right_column_asserts.check_right_column()


def test_right_column_open_thematics(browser, config, login):  # Checkbox 7
    test_env = BaseTestEnv(browser, SERVER)
    test_env.load()

    right_column_asserts = RightColumnOpenThematicsAssert(browser)
    right_column_asserts.check_open_thematics()


def test_right_column_table(browser, config, login):  # Checkbox 8
    test_env = BaseTestEnv(browser, SERVER)
    test_env.load()

    table_asserts = TableAssert(browser)
    table_asserts.check_table()
