#-*- coding:utf-8 -*-
from selenium import webdriver
from selenium.webdriver import  ActionChains
from time import sleep
import unittest
import HtmlTestRunner
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions

'''
author:wukaizhong
date:20200716
备注:此脚本展示selenium的常用方法，相关参数和方法可以查看源代码进行深入了解。
'''

class MyTestCase(unittest.TestCase):
    #这里的装饰器只能用classmethod，否则会报错的
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        print('setUpClass')
        cls.driver = webdriver.Chrome(executable_path='chromedriver')
        cls.driver.get('https://www.baidu.com')
        cls.driver.maximize_window()
        #隐形等待，全局有效
        cls.driver.implicitly_wait(10)

    def setUp(self) -> None:
        super().setUp()
        # print('setup')

    def test_1(self):
        self.assertEqual(3,1+2)
        print('test_1')

    def test_2(self):
        #是否包含
        self.assertIn(1,[2,3,4,5,1])
        print('test_2')

    def test_3_zhihu(self):
        '''
        self.driver.name:驱动名字
        self.driver.page_source:页面源码
        self.driver.title:页面标题
        self.driver.current_url:当前页面url
        self.driver.current_window_handle:当前页面句柄
        self.driver.window_handles:现在所有页面句柄
        '''
        input_data = self.driver.find_element_by_id('kw')
        input_data.send_keys(u"知乎")
        btn_ensure = self.driver.find_element_by_id('su')
        ActionChains(self.driver).click(btn_ensure).perform()
        sleep(2)
        zhihu = self.driver.find_element_by_partial_link_text('知乎- 有问题,上知乎')
        ActionChains(self.driver).click(zhihu).perform()
        print("*" * 100)
        print(self.driver.name)
        # print(self.driver.page_source)
        print(self.driver.title)
        print(self.driver.current_url)
        print(self.driver.current_window_handle)
        print(self.driver.window_handles)
        print("*" * 100)
        sleep(2)
        #点击链接，页面已经切换至新页面，需要切换句柄到新页面
        windows = self.driver.window_handles
        self.driver.switch_to.window(windows[1])
        self.driver.close()
        #切换会原页面
        self.driver.switch_to.window(windows[0])
        sleep(2)

    def test_4_baidu_xpath(self):
        input_data = self.driver.find_element_by_xpath('//*[@id="kw"]')
        input_data.clear()
        input_data.send_keys('selenium')
        btn = self.driver.find_element_by_xpath('//*[@id="su"]')
        ActionChains(self.driver).click(btn).perform()
        sleep(2)

    def test_5_baidu_css(self):
        #  .代表类选择器，#代表ID选择器
        input_data = self.driver.find_element_by_css_selector('.s_ipt')
        input_data.clear()
        input_data.send_keys('find_element_by_css_selector')
        btn = self.driver.find_element_by_css_selector('#su')
        ActionChains(self.driver).click(btn).perform()
        sleep(2)

    def test_6_baidu_attribute(self):
        #浏览器向后返回
        self.driver.back()
        sleep(1)
        #刷新浏览器
        self.driver.refresh()
        sleep(1)
        #浏览器向前一步走
        self.driver.forward()
        sleep(1)

    def test_7_sahitest(self):
        '''
        h1.size:元素大小
        h1.text：元素内容
        h1.tag_name：元素标签
        :return:
        '''
        self.driver.get('http://sahitest.com/demo/headingsTest.htm')
        h1 = self.driver.find_element_by_tag_name('h1')
        print(h1.size)
        print(h1.text)
        print(h1.tag_name)
        sleep(3)

    def test_8_elements_attribute(self):
        '''
        input.get_attribute('malength'))
        input.is_displayed:是否显示
        input.is_enabled：是否可用
        input.is_selected：是否被选中
        input.value_of_css_property('color')：css的颜色属性
        input.value_of_css_property('font')：css的字体
        '''
        self.driver.get('https://www.baidu.com')
        input = self.driver.find_element_by_id('kw')
        print(input.get_attribute('malength'))
        print(input.is_displayed())
        print(input.is_enabled())
        print(input.is_selected())
        print(input.value_of_css_property('color'))
        print(input.value_of_css_property('font'))

    def test_9_form_and_checkbox(self):
        '''
        对于html中的form、checkbox、radio元素，存在难定位的问题，也许是相同name、class属性等，
        selenium有提供对应的方法来帮助定位元素，我们需要多定位几层，跟他们不同的属性来判断那个元素
        :return:
        '''
        self.driver.get('http://sahitest.com/demo/formTest.htm')
        sleep(3)
        #操作页面转至弹框
        alt = self.driver.switch_to.alert
        alt.accept()  #点击确定，dimiss()是取消
        input_data = self.driver.find_element_by_name('t1')
        input_data.send_keys('test')
        sleep(1)
        print(input_data.is_selected())  #False
        print(input_data.is_enabled())   #True
        print(input_data.get_attribute('name'))   #None
        #对于没有特殊属性的checkbox，我们可以这样去定位元素
        checkbox_list = self.driver.find_elements_by_tag_name('input')
        for i in checkbox_list:
            if i.get_attribute('type') == 'checkbox':
                if i.get_attribute('value') =='cv2' or i.get_attribute('value') == 'cv3':
                    i.click()
                    print('click cv2 or cv3!!!')
        sleep(2)
        #radio 存在相同的name属性
        radio_list = self.driver.find_elements_by_name('r1')
        for radio in radio_list:
            if radio.get_attribute('value') == 'rv2':
                #此处使用click会存在位置混淆
                ActionChains(self.driver).click(radio).perform()
                print("click rv2")
        sleep(1)

    #http://sahitest.com/demo/selectTest.htm
    def test_A10_select(self):
        '''
        操作下拉列表
        :return:
        '''
        self.driver.get('http://sahitest.com/demo/selectTest.htm')
        sleep(1)
        select1 = self.driver.find_element_by_id('s1Id')
        #根据第几个选择
        Select(select1).select_by_index(1)
        sleep(1)
        #根据value值选择
        Select(select1).select_by_value('o2')
        sleep(1)
        #根据显示内容选择
        Select(select1).select_by_visible_text('o3')
        sleep(1)
        #多选 方法一
        select2 = self.driver.find_element_by_id('s4Id')
        Select(select2).select_by_visible_text('o1')
        Select(select2).select_by_visible_text('o2')
        Select(select2).select_by_visible_text('o3')
        sleep(2)
        #取消选择一个选项
        Select(select2).deselect_by_visible_text('o2')
        sleep(1)
        #取消全部选项
        Select(select2).deselect_all()
        sleep(2)
        #多选方法二
        select3 = self.driver.find_element_by_id('s4Id')
        option1 = Select(select3).select_by_value('o1val')
        option2 = Select(select3).select_by_value('o2val')
        option3 = Select(select3).select_by_value('o3val')
        #模拟鼠标+键盘操作
        sleep(3)
        ActionChains(self.driver).key_down(Keys.CONTROL).click(option1).key_up(Keys.CONTROL).perform()
        ActionChains(self.driver).key_down(Keys.CONTROL).click(option2).key_up(Keys.CONTROL).perform()
        ActionChains(self.driver).key_down(Keys.CONTROL).click(option3).key_up(Keys.CONTROL).perform()
        sleep(3)

    def test_A11_alert(self):
        self.driver.get('http://sahitest.com/demo/confirmTest.htm')
        sleep(3)
        confirm = self.driver.find_element(By.NAME,'b1')
        confirm.click()
        sleep(3)
        alt = self.driver.switch_to.alert
        print('alert:',alt.text)
        alt.dismiss()
        sleep(3)
        # window = self.driver.window_handles
        # self.driver.switch_to.window(window[0])
        input = self.driver.find_element_by_name('t1')
        print("input data:",input.text)  #因为这个是点击后写入输入框的内容，html中的代码里t1是没有内容的，所以结果页是没有展示

    def test_A12_prompt(self):
        self.driver.get('http://sahitest.com/demo/promptTest.htm')
        sleep(2)
        btn = self.driver.find_element_by_name('b1')
        btn.click()
        #操作弹框prompt
        prompt = self.driver.switch_to.alert
        prompt.send_keys('这是弹框输入框')
        prompt.accept()
        sleep(3)

    def test_A13_wait(self):
        self.driver.get('http://sahitest.com/demo/waitFor.htm')
        #1、强制等待
        sleep(2)
        btn = self.driver.find_element_by_xpath('/html/body/form/input[2]')
        btn.click()
        #2、条件等待,需要注意的是expected_conditions的方法中需要输入的是元组，而非其他数据
        WebDriverWait(self.driver,5).until(expected_conditions.visibility_of_element_located((By.ID,'id2')))
        output = self.driver.find_element_by_id('id2').text
        #3、隐性等待
        self.driver.implicitly_wait(3)
        print(output)

    def tearDown(self) -> None:
        super().tearDown()
        # print('tearDown')

    @classmethod
    def tearDownClass(cls) -> None:
        super().tearDownClass()
        print('tearDownClass')
        cls.driver.quit()



if __name__ == "__main__":
    # unittest.main()
    #关于HtmlTestRunner的参数，最好自己看源代码
    unittest.main(testRunner=HtmlTestRunner.HTMLTestRunner(
        output='report',
        report_name='Selenium_report',
        report_title='Report'
    ))
