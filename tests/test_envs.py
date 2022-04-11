from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from config import SERVER


class BaseTestEnv:
    def __init__(self, browser, url):
        self.browser = browser
        self.url = url

    def load(self):
        self.browser.get(self.url)


class Login(BaseTestEnv):
    USERNAME_INPUT = (By.ID, 'id_login')
    PASSWORD_INPUT = (By.ID, 'id_password')
    BUTTONS = (By.TAG_NAME, 'button')

    def __init__(self, browser, config):
        url = f'{SERVER}/accounts/login/'
        super().__init__(browser, url)
        self.config = config

    def login(self):
        username_input = self.browser.find_element(*self.USERNAME_INPUT)
        username_input.send_keys(self.config.username)

        password_input = self.browser.find_element(*self.PASSWORD_INPUT)
        password_input.send_keys(self.config.password)

        buttons = self.browser.find_elements(*self.BUTTONS)
        sign_up_button = buttons[-1]
        sign_up_button.send_keys(Keys.RETURN)


class Registration(BaseTestEnv):
    FIRST_NAME_INPUT = (By.ID, 'id_first_name')
    LAST_NAME_INPUT = (By.ID, 'id_last_name')
    USERNAME_INPUT = (By.ID, 'id_username')
    EMAIL_INPUT = (By.ID, 'id_email')
    PASSWORD1_INPUT = (By.ID, 'id_password1')
    PASSWORD2_INPUT = (By.ID, 'id_password2')
    BUTTONS = (By.TAG_NAME, 'button')

    def __init__(self, browser, config, invite_key):
        url = f'{SERVER}/users/invite/?key={invite_key}'
        super().__init__(browser, url)
        self.invite_key = invite_key
        self.config = config

    def registrate(self):
        first_name_input = self.browser.find_element(*self.FIRST_NAME_INPUT)
        first_name_input.send_keys(self.config.first_name)

        last_name_input = self.browser.find_element(*self.LAST_NAME_INPUT)
        last_name_input.send_keys(self.config.last_name)

        username_input = self.browser.find_element(*self.USERNAME_INPUT)
        username_input.send_keys(self.config.username)

        email_input = self.browser.find_element(*self.EMAIL_INPUT)
        email_input.send_keys(self.config.email)

        password1_input = self.browser.find_element(*self.PASSWORD1_INPUT)
        password1_input.send_keys(self.config.password)

        password2_input = self.browser.find_element(*self.PASSWORD2_INPUT)
        password2_input.send_keys(self.config.password)

        buttons = self.browser.find_elements(*self.BUTTONS)
        sign_up_button = buttons[-1]
        sign_up_button.send_keys(Keys.RETURN)
