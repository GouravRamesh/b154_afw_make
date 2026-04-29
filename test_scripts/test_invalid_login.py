from generics.base_test import BaseTest
from pages.login_page import LoginPage
from generics.utility import Utility
import pytest
class Test_InvalidLogin(BaseTest):
    @pytest.mark.order(2)
    def test_invalid_login(self):
        un = Utility.read_xl(self.xl_path,"InvalidLogin",2,1)
        pw = Utility.read_xl(self.xl_path,"InvalidLogin",2,2)
        # 1. enter invalid username
        login_page=LoginPage(self.page)
        login_page.set_username(un)
        # 2. enter invalid password
        login_page.set_password(pw)
        # 3. click on go button
        login_page.click_go_button()
        # 4. verify that error message is displayed
        result=login_page.verify_errmsg_is_displayed()
        assert result