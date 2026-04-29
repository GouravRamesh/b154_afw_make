from playwright.sync_api._generated import  Page

class LoginPage:

    __username:str #declare the variable as private
    __password:str
    __go_button:str
    __err_msg:str

    def __init__(self,page:Page):
        self.page=page
        self.__username="#input-username" #initialization
        self.__password="#input-password"
        self.__go_button="//button[text()='Go']"
        self.__err_msg="//div[contains(text(),'Invalid username and/or password.')]"


    def set_username(self,un):
        print("enter the username:",un)
        self.page.locator(self.__username).fill(un) #utilzation

    def set_password(self,pw):
        print("enter the password:", pw)
        self.page.locator(self.__password).fill(pw)

    def click_go_button(self):
        print("click on go button")
        self.page.locator(self.__go_button).click()


    def verify_errmsg_is_displayed(self)->bool:
        try:
            self.page.locator( self.__err_msg).wait_for()
            print("Err Msg is Displayed")
            return True
        except:
            print("Err Msg is Not Displayed")
            return False
