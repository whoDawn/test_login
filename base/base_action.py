from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

class BaseAction():

    def __init__(self,driver):
        self.driver = driver

    def click(self,loc):
        self.find_element(loc).click()


    def input_text(self,loc,text):
        self.find_element(loc).send_keys(text)

    def swipe_to(self):
        height =  self.driver.get_window_size()['height']
        width =  self.driver.get_window_size()['width']
        start_x = height * 0.5
        start_y = width * 0.75
        end_x = start_x
        end_y = width * 0.25
        return self.driver.swipe(start_x, start_y, end_x, end_y, 5000)


    def find_element(self, loc, time=10.0, poll=1.0):
        # 封装 单个元素
        by = loc[0]
        value = loc[1]
        if by == By.XPATH:
            value = self.make_xpath_with_feature(value)
            print(value)
        return WebDriverWait(self.driver, time, poll).until(lambda x:x.find_element(by, value))

    def find_elements(self, loc,time = 10.0,poll = 1.0):
        # 封装 查找多个元素
        by = loc[0]
        value = loc[1]
        if by == By.XPATH:
            value = self.make_xpath_with_feature(value)
        return WebDriverWait(self.driver, time, poll).until(lambda x: x.find_elements(by,value))

    def make_xpath_with_unit_feature(self,loc):
        # 封装 拼接xpath的中间部分
        by_index = 0
        value_index = 1
        option_index = 2

        args = loc.split(',')
        if len(args) == 2:
            feature = "contains(@" + args[by_index] + ",'" + args[value_index] + "')"
        elif len(args) == 3:
            if args[option_index]:
                feature = "@" + args[by_index] + "='" + args[value_index] + "'"
            else:
                feature = "contains(@" + args[by_index] + ",'" + args[value_index] + "')"
        return feature
    def make_xpath_with_feature(self, loc):

        # 封装 xpath 拼接成一个完整的xpath
        start_element = '//*['
        end_element = ']'
        feature = ''
        if isinstance(loc,str):
            # 判断是不是一个字符串
            if loc.startswith('//'):
                return loc

            else:
                feature =  self.make_xpath_with_unit_feature(loc)
        elif isinstance(loc,list):
            # 判断是不是列表
            for i in loc:
                feature +=self.make_xpath_with_unit_feature(i) + 'and '
            feature = feature.strip('and ')
        else:
            print('输入的格式不正确，列表或者字符串，字符串后面加1，为精确查找，为0，模糊查找')
        loc = start_element + feature + end_element
        return loc

    def find_toast(self, mass,is_screenshot = False, screen =None,time = 5, poll = 0.1):
        # 封装toast，获取吐司的文本值
        mass = "//*[contains(@text,'" + mass +"')]"
        element = self.find_element((By.XPATH, mass), time, poll)
        if is_screenshot:
            self.driver.get_screenshot_as_file("./screen/" + screen + ".png")
        return element.text
    def is_toast_exist(self, mass, is_screenshot = False, screen =None, time=3, poll = 0.1):
        try:
            self.find_toast(mass, is_screenshot = False, screen =None, )
            return True
        except Exception:
            return False

