import os
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from config import SERVER, DOWNLOAD_DIR


class RegistrationAssert:
    def __init__(self, browser, personal_page_url):
        self.browser = browser
        self.personal_page_url = personal_page_url

    def check_url(self):
        assert self.browser.current_url.startswith(
            self.personal_page_url
        )


class MainPageAssert:
    THEMATIC_HEADERS = (By.CLASS_NAME, 'thematic-name')
    
    def __init__(self, browser):
        self.browser = browser

    def check_thematics_number(self):
        thematic_headers = self.browser.find_elements(*self.THEMATIC_HEADERS)
        assert 8 < len(thematic_headers) < 16


class ThematicPanelAssert:
    THEMATIC_BUTTONS = (By.CLASS_NAME, 'accordion-button')
    PANEL = (By.ID, 'panelsStayOpen-collapse1')

    def __init__(self, browser):
        self.browser = browser

    def check_open_panel(self):
        thematic_buttons = self.browser.find_elements(*self.THEMATIC_BUTTONS)
        button = thematic_buttons[0]
        panel = self.browser.find_element(*self.PANEL)

        button.send_keys(Keys.RETURN)
        time.sleep(1)
        assert panel.value_of_css_property('display') != 'none'

        button.send_keys(Keys.RETURN)
        time.sleep(1)
        assert panel.value_of_css_property('display') == 'none'


class ApplicationAssert:
    THEMATIC_BUTTONS = (By.CLASS_NAME, 'accordion-button')
    KIND_BUTTONS = (By.CLASS_NAME, 'checkbox-kind')

    @classmethod
    def LABEL(cls, button_id):
        return (By.CSS_SELECTOR, f'label[for={button_id}]')

    @classmethod
    def MAYBE_STATISTIC(cls, button_id):
        span_id = f'statistic-maybe-{button_id.split("-")[-1]}-{button_id.split("-")[1][2]}'
        return (By.ID, span_id)

    def __init__(self, browser):
        self.browser = browser

    def check_statistic(self):
        thematic_buttons = self.browser.find_elements(*self.THEMATIC_BUTTONS)
        thematic_buttons[0].send_keys(Keys.RETURN)
        time.sleep(1)

        kind_buttons = self.browser.find_elements(*self.KIND_BUTTONS)
        button = [b for b in kind_buttons if not b.is_selected()][0]
        button_id = button.get_attribute('id')
        label = self.browser.find_element(*self.LABEL(button_id))
        maybe_statistic = self.browser.find_element(*self.MAYBE_STATISTIC(button_id))
        maybe_value = int(maybe_statistic.text)

        label.click()
        time.sleep(1)
        assert int(maybe_statistic.text) - maybe_value == 1

        label.click()
        time.sleep(1)
        assert int(maybe_statistic.text) - maybe_value == 0


class RightColumnAssert:
    COLUMN = (By.CLASS_NAME, 'offcanvas')
    SWITCH_BUTTON = (By.CLASS_NAME, 'switch-button')
    
    def __init__(self, browser):
        self.browser = browser

    def check_right_column(self):
        column = self.browser.find_element(*self.COLUMN)

        switch_button = self.browser.find_element(*self.SWITCH_BUTTON)
        switch_button.send_keys(Keys.RETURN)
        assert column.value_of_css_property('visibility') != 'hidden'

        switch_button.send_keys(Keys.RETURN)
        time.sleep(0.5)
        assert column.value_of_css_property('visibility') == 'hidden'


class RightColumnOpenThematicsAssert:
    SWITCH_BUTTON = (By.CLASS_NAME, 'switch-button')
    OPEN_THEMATICS_SWITCH = (By.CLASS_NAME, 'switch')
    PANELS = (By.CLASS_NAME, 'accordion-collapse')

    def __init__(self, browser):
        self.browser = browser

    def check_open_thematics(self):
        switch_button = self.browser.find_element(*self.SWITCH_BUTTON)
        switch_button.send_keys(Keys.RETURN)

        open_thematics_switch = self.browser.find_element(By.CLASS_NAME, 'switch')
        open_thematics_switch.click()
        time.sleep(0.25)

        panels = self.browser.find_elements(*self.PANELS)

        for panel in panels:
            assert panel.value_of_css_property('display') != 'none'
    

class TableAssert:
    SWITCH_BUTTON = (By.CLASS_NAME, 'switch-button')
    DOWNLOAD_LINK = (By.CSS_SELECTOR, 'a[href="/electives/download_table/"]')

    def __init__(self, browser):
        self.browser = browser

    def check_table(self):
        prev_tables = []
        for file in os.listdir(DOWNLOAD_DIR):
            if 'table' in file:
                prev_tables.append(file)

        switch_button = self.browser.find_element(*self.SWITCH_BUTTON)
        switch_button.send_keys(Keys.RETURN)

        download_link = self.browser.find_element(*self.DOWNLOAD_LINK)
        download_link.click()
        time.sleep(5.5)

        tables = []
        for file in os.listdir(DOWNLOAD_DIR):
            if 'table' in file:
                tables.append(file)

        assert len(tables) > len(prev_tables)
