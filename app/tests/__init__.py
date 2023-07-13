from app.tests.config import setup_env


def setup_package():
    '''Set up your environment for test package'''
    setup_env()


def teardown_package():
    '''revert the state '''