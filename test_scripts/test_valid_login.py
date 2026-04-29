from generics.base_test import BaseTest
from pages.login_page import LoginPage
from pages.home_page import HomePage
from generics.utility import Utility
import  pytest
class Test_ValidLogin(BaseTest):
    @pytest.mark.order(1)
    def test_valid_login(self):
        un = Utility.read_xl(self.xl_path,"ValidLogin",2,1)
        pw = Utility.read_xl(self.xl_path,"ValidLogin",2,2)
        # 1. enter valid username
        login_page=LoginPage(self.page)
        login_page.set_username(un)
        # 2. enter valid password
        login_page.set_password(pw)
        # 3. click on go button
        login_page.click_go_button()
        # 4. verify that home page is displayed
        home_page=HomePage(self.page)
        result=home_page.verify_homepage_is_displayed()
        assert False