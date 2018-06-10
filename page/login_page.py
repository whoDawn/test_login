import os,sys

from selenium.webdriver.common.by import By
sys.path.append(os.getcwd())
from base.base_action import BaseAction

class LoginPage(BaseAction):

    user_button = By.XPATH,["text,我的","resource-id,com.tpshop.malls:id/tab_txtv,1"]
    login1_button = By.XPATH, "text,登录"
    user_name_button = By.XPATH,'text,输入手机号码'
    password_button = By.ID,'com.tpshop.malls:id/edit_password'
    login_button = By.ID,'com.tpshop.malls:id/btn_login'

    def __init__(self,driver):
        BaseAction.__init__(self, driver)
        self.jump_2_click_login()

    def jump_2_click_login(self):
        self.click(self.user_button)
        self.click(self.login1_button)
    def input_username(self,text):
        self.input_text(self.user_name_button,text)
    def input_password(self,text):
        self.input_text(self.password_button,text)
    def click_login_1(self):
        self.click(self.login_button)
