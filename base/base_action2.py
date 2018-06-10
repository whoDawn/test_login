from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait


class BaseAction():
    #定位常用操作

    def __init__(self, driver):
        self.driver = driver

    def click(self, loc):
        #点击
        self.find_element(loc).click()

    def input_text(self, loc, text):
        #输入文本
        self.find_element(loc).send_keys(text)

    def find_element(self, loc,time=10,poll=0.5):
        # 把传入的元组拆分开
        loc_by = loc[0]
        loc_value = loc[1]
        # 因为传的参数变了格式，判断是不是xpath
        if loc_by == By.XPATH:
            # xpath 使用包装函数还原成python能够识别的格式
            loc_value = self.make_xpath_with_feature(loc_value)
        # 查找元素添加了，显示等待
        return  WebDriverWait(self.driver,time,poll).until(lambda x:x.find_element(loc_by,loc_value))

    def make_xpath_with_unit_feature(self,loc):
        """
        拼接xpath中间的部分
        :param loc:
        :return:
        """
        # 定义下标 阅读代码更直观
        key_index = 0
        value_index = 1
        option_index = 2
        # 分割开传递的参数，变成列表的形式
        args = loc.split(",")
        feature = ""
        # 判断传递参数的个数，2个默认使用模糊匹配
        if len(args) == 2:
            # 实现拼接，默认模糊匹配
            feature = "contains(@" + args[key_index] + ",'" + args[value_index] + "')"
            # 传递参数为3个时，判断是否使用模糊匹配和准确匹配
        elif len(args) == 3:
            if args[option_index] == "1":
                # 为True 即准确匹配
                feature = "@" + args[key_index] + "='" + args[value_index] + "'"

            elif args[option_index] == "0":
                # 为False 模糊匹配
                feature = "contains(@" + args[key_index] + ",'" + args[value_index] + "')"
        # 返回拼接结果
        return feature

    def make_xpath_with_feature(self,loc):
        feature_start = "//*["
        feature_end = "]"
        feature = ""
        # 判断是否是字符串
        if isinstance(loc, str):
            # 如果是正常的xpath（即格式为原格式）
            if loc.startswith("//"):
                # 返回原值
                return loc

            # loc str
            # 结果为find_element的value值
            feature = self.make_xpath_with_unit_feature(loc)
        else:
            # loc 列表
            # 遍历列表，再添加+and+连接
            for i in loc:
                feature += self.make_xpath_with_unit_feature(i)+ "and "
        # 剪切掉多余的and
        feature = feature.rstrip("and ")
        loc = feature_start + feature + feature_end
        # 返回拼接结果
        return loc
