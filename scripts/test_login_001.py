import os,sys
import allure
import pytest
sys.path.append(os.getcwd())
from base.base_driver import init_driver
from page.login_page import LoginPage
from base.base_yml import yml_with_file
def t_data(key):
    return  yml_with_file('login_data',key)

class TestLogin():

    def setup(self):
        self.driver = init_driver()
        self.login_page = LoginPage(self.driver)
    @allure.step(title="测试登录脚本")
    @pytest.mark.parametrize('args', t_data("test_login"))
    def test_login(self,args):
        username = args['username']
        password = args['password']
        toast = args['toast']
        screen = args['screen']
        # 输入手机号码
        allure.attach("输入手机号码",username)
        self.login_page.input_username(username)
        # 输入密码
        allure.attach('输入密码',password)
        self.login_page.input_password(password)
        # 点击登录
        allure.attach('点击登录','')
        self.login_page.click_login_1()
        # 截图
        rse = self.login_page.is_toast_exist(toast, True, screen)
        allure.attach("toast图片", open("./screen/"+screen+".png",'rb').read(),allure.attach_type.PNG)
        # 添加断言，判断是否登录成功
        assert rse
