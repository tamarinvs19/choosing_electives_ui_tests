import string
from random import sample
from dataclasses import dataclass


@dataclass
class UserConfig():
    def __init__(self):
        suffix = ''.join(sample(string.ascii_letters, 5))
        self.first_name = '__test_first_name' + suffix
        self.last_name = '__test_last_name' + suffix
        self.username = '__test_username' + suffix
        self.email = suffix + 'test_email@test.com'
        self.password = 'psw1' + ''.join(
            sample(string.ascii_letters + string.digits, 10)
        )
