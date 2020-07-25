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
from selenium.webdriver import DesiredCapabilities
import csv
#ddt是实现数据驱动测试的一个库
from ddt import ddt,data,unpack


'''
author:wukaizhong
date:20200716
备注:此脚本展示selenium的常用方法，相关参数和方法可以查看源代码进行深入了解。
'''

#获取csv文件函数，给unittest类使用
def get_csv_data(csv_path):
    rows = []
    csv_data = open(str(csv_path),'r')
    content = csv.reader(csv_data)
    for row in content:
        rows.append(row)
    return  rows

@ddt
class MyTestCase(unittest.TestCase):
    #这里的装饰器只能用classmethod，否则会报错的
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        print('setUpClass')
        cls.driver = webdriver.Chrome(executable_path='chromedriver')
        cls.driver.get('https://www.baidu.com')
        cls.driver.maximize_window()
        #隐性等待，全局有效
        cls.driver.implicitly_wait(10)

    def setUp(self) -> None:
        super().setUp()
        # print('setup')

    def tearDown(self) -> None:
        super().tearDown()
        # print('tearDown')

    @classmethod
    def tearDownClass(cls) -> None:
        super().tearDownClass()
        print('tearDownClass')
        cls.driver.quit()

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

    # def test_B1_remote(self):
    #     '''
    #     1、远程执行的默认路径也是：http://127.0.0.1:4444/wd/hub/，现实中根据部署的selenium-server-standalone-xxx.jar服务部署的服务IP和端口来确定执行路径；
    #     2、可通过 http://127.0.0.1:4444/wd/hub/static/resource/hub.html 来监控服务的请求内容
    #     3、desired_capabilities的参数
    #     'acceptInsecureCerts',
    #     'browserName',
    #     'browserVersion',
    #     'platformName',
    #     'pageLoadStrategy',
    #     'proxy',
    #     'setWindowRect',
    #     'timeouts',
    #     'unhandledPromptBehavior',
    #     '''
    #     # 传递执行服务器的信息
    #     caps = {}
    #     # 平台，可选择：ANY、WINDOWS、MAC、ANDROID等
    #     caps['platformName'] = "MAC"
    #     # 浏览器，可选择：safari、chrome、firefox、internet explorer、MicrosoftEdge、android、iPhone等
    #     caps['browserName'] = 'chrome'
    #     caps['browserVersion'] = '83.0.4103.116'
    #     driver = webdriver.Remote(command_executor='http://127.0.0.1:4444/wd/hub', desired_capabilities=caps)
    #     # 发出请求
    #     driver.get('https://www.baidu.com')
    #     input_data = driver.find_element_by_id('kw')
    #     input_data.send_keys('selenium-server-standalone')
    #     btn = driver.find_element_by_id('su')
    #     btn.click()
    #     sleep(2)
    #     #断言
    #     assert 'selenium-server-standalone' in driver.title
    #     driver.quit()

    def test_B2_remote_grid(self):
        '''
        分布式测试grid：通过通过部署hub节点和node代理节点，我可以通过一个ip操作多个不同机器上的不同浏览器
        grid部署：
        1）hub:java -jar selenium-server-standalone-3.141.59.jar -role hub -maxSession 10 -port 4444 &
        2）第一个node节点：java -jar selenium-server-standalone-3.141.59.jar  -role node -port 5555 -hub http://127.0.0.1:4444/grid/register -maxSession 5 \
        -browser “browserName=chrome,browserVersion='83.0.4103.116',seleniumProtocol=WebDriver,maxInstances=5,platform=MAC,platformName=MAC” &
        3）第二个node节点:java -jar selenium-server-standalone-3.141.59.jar  -role node -port 6666 -hub http://127.0.0.1:4444/grid/register -maxSession 5  \
        -browser “browserName=safari,seleniumProtocol=WebDriver,maxInstances=5,platform=MAC,version=13.1” &
        ps:若部署的时候调用失败，可尝试去掉-browser参数，使用默认参数(提交的capabilities不匹配导致无法调用)
        部署后，代码还是需要Remote链接到hub，然后需要导入DesiredCapabilities，使desired_capabilities=DesiredCapabilities.CHROME即可（CHROME为对应的浏览器名）
        ps:分布式测试grid与远程调用部署方式不一样，desired_capabilities调用的也不一样，其余一样。所以test_B1_remote和test_B2_remote_grid不能够同时运行（都独立部署对应环境除外）
        '''
        #使用from selenium.webdriver import DesiredCapabilities
        driver = webdriver.Remote(command_executor='http://127.0.0.1:4444/wd/hub',
                                       desired_capabilities=DesiredCapabilities.CHROME)
        # 发出请求
        driver.get('https://www.baidu.com')
        input_data = driver.find_element_by_id('kw')
        input_data.send_keys('selenium-server-standalone')
        btn = driver.find_element_by_id('su')
        btn.click()
        sleep(2)
        # 断言
        assert 'selenium-server-standalone' in driver.title
        driver.quit()
    def test_C1_ActionChains(self):
        '''
        鼠标事件，操作鼠标的函数
        1、单击：click()
        2、双击：double_click()
        3、右击：context_click()
        4、移动鼠标至某个元素上方：context_click()
        5、执行ActionChains中所有的事件：perform()
        :return:
        '''
        self.driver.get('http://sahitest.com/demo/clicks.htm')
        #单击
        simple_click = self.driver.find_element_by_xpath('/html/body/form/input[3]')
        ActionChains(self.driver).click(simple_click).perform()
        #双击
        double_click = self.driver.find_element_by_xpath('/html/body/form/input[2]')
        ActionChains(self.driver).double_click(double_click).perform()
        #右击
        right_click = self.driver.find_element_by_xpath('/html/body/form/input[4]')
        ActionChains(self.driver).context_click(right_click).perform()
        #将鼠标移动到某个元素上面,然后点击
        sleep(1)
        move_mounse = self.driver.find_element_by_xpath('/html/body/form/input[1]')
        ActionChains(self.driver).move_to_element(move_mounse).click().perform()
        sleep(2)
    def test_C2_drag_and_drop(self):
        '''
        鼠标拖延函数：drag_and_drop(source, target)
        '''
        self.driver.get('http://sahitest.com/demo/dragDropMooTools.htm')
        drag_me = self.driver.find_element_by_id('dragger')
        item_1 = self.driver.find_element_by_xpath('/html/body/div[2]')
        item_4 = self.driver.find_element_by_xpath('/html/body/div[5]')
        sleep(1)
        ActionChains(self.driver).drag_and_drop(drag_me,item_1).perform()
        sleep(1)
        ActionChains(self.driver).drag_and_drop(drag_me, item_4).perform()
        sleep(3)

    def test_C3_keyboard(self):
        '''
        键盘事件：
        1、按下按钮：key_down()
        2、释放已按下的键盘按键：key_up()
        3、键盘内容输入：send_keys(),内容直接输入字符串内容即可
        4、按键：
        回车键 Keys.ENTER
        删除键 Keys.BACK_SPACE
        空格键 Keys.SPACE
        制表键 Keys.TAB
        回退键 Keys.ESCAPE
        刷新键 Keys.F5
        ctrl  Keys.CONTROL
        '''
        self.driver.get('http://sahitest.com/demo/keypress.htm')
        sleep(1)
        data_input = self.driver.find_element_by_name('t2')
        data_input.send_keys('input data...')
        sleep(3)
        self.driver.find_element_by_xpath('/html/body/form/input[4]').click()
        #输入键盘值command+a,全选框内数据,复制粘贴（mac是command，windows是ctl）
        data = self.driver.find_element_by_name('t3')
        data.send_keys(Keys.TAB,Keys.TAB)
        sleep(1)
        key_down1 = self.driver.find_element_by_id('r2')
        ActionChains(self.driver).click(key_down1).perform()
        # control+单击，最后释放按键control
        ActionChains(self.driver).key_down(Keys.CONTROL).click(key_down1).key_up(Keys.CONTROL).perform()
        sleep(1)

    def test_C4_scrollbar(self):
        '''
        selenuim 可实现滚动条：
        # 移动到元素element对象的“顶端”与当前窗口的“顶部”对齐
        driver.execute_script("arguments[0].scrollIntoView();", element);
        driver.execute_script("arguments[0].scrollIntoView(true);", element);
        # 移动到元素element对象的“底端”与当前窗口的“底部”对齐
        driver.execute_script("arguments[0].scrollIntoView(false);", element);
        # 移动到页面最底部
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight)");
        # 移动到指定的坐标(相对当前的坐标移动)
        driver.execute_script("window.scrollBy(0, 700)");
        # 结合上面的scrollBy语句，相当于移动到700+800=1500像素位置
        driver.execute_script("window.scrollBy(0, 800)");
        # 移动到窗口绝对位置坐标，如下移动到纵坐标1600像素位置
        driver.execute_script("window.scrollTo(0, 1600)");
        # 结合上面的scrollTo语句，仍然移动到纵坐标1200像素位置
        driver.execute_script("window.scrollTo(0, 1200)");
        '''
        self.driver.get('https://baidu.com')
        input_data = self.driver.find_element_by_id('kw')
        input_data.send_keys("python")
        btn_ensure = self.driver.find_element_by_id('su')
        ActionChains(self.driver).click(btn_ensure).perform()
        #定位到body
        element = self.driver.find_element_by_xpath('/html/body')
        sleep(2)
        # 移动到指定的坐标(相对当前的坐标移动)
        self.driver.execute_script("window.scrollBy(0, 700)")
        sleep(1)
        # 移动到元素element对象的“底端”与当前窗口的“底部”对齐
        self.driver.execute_script("arguments[0].scrollIntoView(false);", element)
        sleep(1)
        # 移动到元素element对象的“顶端”与当前窗口的“顶部”对齐
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        sleep(2)


    def test_C5_js(self):
        '''
        执行javascript两个方法，一个是同步执行，一个是异步执行
        1、同步执行：execute_script(js,args)
        2、异步执行：execute_async_script(js,args)
        :return:
        '''
        self.driver.get('http://sahitest.com/demo/jsPopup.htm')
        h2 = self.driver.find_element_by_tag_name('h2')
        #编写js脚本
        sleep(1)
        js = 'arguments[0].style.color="red"'
        #执行js脚本
        self.driver.execute_script(js,h2)
        sleep(2)
        #给出一个提示
        alert = 'alert(arguments[0])'
        #执行alert脚本
        self.driver.execute_async_script(alert,'alert info!!!')
        sleep(2)
        #将alert脚本的弹窗确定，以免印象后面用例
        alt = self.driver.switch_to.alert
        alt.accept()

    def test_D1_frame_or_iframe(self):
        '''
        如果元素在frame或者iframe内的，我们需要先将frame/iframe转至该frame/iframe
        函数可用:switch_to.frame(iframe_location)
        '''
        self.driver.get("http://sahitest.com/demo/docWriteIFrame.htm")
        sleep(1)
        self.driver.find_element_by_xpath('/html/body/form/input[2]').click()
        #转换至该iframe，相当于转至该页面了
        self.driver.switch_to.frame(self.driver.find_element_by_xpath('//*[@id="iframe1"]'))
        frame_href = self.driver.find_element_by_xpath('/html/body/a')
        #鼠标点击
        ActionChains(self.driver).move_to_element(frame_href).click().perform()

        sleep(3)

    def test_D2_upload_files(self):
        '''
        selenium 上传文件分三步：
        1、定位到input type=file元素；
        2、send_keys 文件路径；
        3、submit提交
        '''
        self.driver.get('http://sahitest.com/demo/php/fileUpload.htm')
        sleep(1)
        #1、定位到input type=file元素；
        file_path = self.driver.find_element_by_id('file')
        #2、send_keys 文件路径；
        file_path.send_keys(r'/Users/walter/Pictures/IMG_20191005_181507.jpg')
        #3、submit提交
        submit_btn = self.driver.find_element_by_xpath('/html/body/form[1]/input[3]')
        ActionChains(self.driver).click(submit_btn).perform()
        sleep(3)

    def test_D3_no_interface(self):
        '''
        selenium 存在不想查看页面的场景，此功能只要在driver实例化是调用headless参数，并在driver实例化时赋予options参数即可
        '''
        options = webdriver.ChromeOptions()
        #给chrome添加参数
        options.add_argument('headless')
        #将设置的参数赋予给实例
        driver = webdriver.Chrome(executable_path='chromedriver',options=options)
        driver.get("https://www.baidu.com")
        input_data = driver.find_element_by_id('kw')
        input_data.send_keys(u"知乎")
        btn_ensure = driver.find_element_by_id('su')
        ActionChains(driver).click(btn_ensure).perform()
        print("title:",driver.title)
        print("current_url:",driver.current_url)
        driver.quit()

    # #注意代理ip需要调用得了
    # def test_D4_proxy(self):
    #     '''
    #     可以对请求ip设置代理，防止ip被限；
    #     方法也是在ChromeOptions 中添加--proxy-server 参数
    #     '''
    #     options = webdriver.ChromeOptions()
    #     #给chrome添加参数,由于代理ip问题，脚本不一定能够调通，实际使用中使用可用的ip即可
    #     options.add_argument('--proxy-server=http://60.13.42.36:9999')
    #     #将设置的参数赋予给实例
    #     driver = webdriver.Chrome(options=options)
    #     driver.get("https://www.baidu.com")
    #     input_data = driver.find_element_by_id('kw')
    #     input_data.send_keys(u"知乎")
    #     btn_ensure = driver.find_element_by_id('su')
    #     ActionChains(driver).click(btn_ensure).perform()
    #     print("title:",driver.title)
    #     print("current_url:",driver.current_url)
    #     driver.quit()

    def test_E1_xml(self):
        '''
        读取xml文件信息：
        可使用使用xml.etree来读取
        '''
        # 为了兼容不同的版本，所以对两种情况进行兼容
        try:
            import xml.etree.cElementTree as ET
        except Exception as e:
            import xml.etree.ElementTree as ET

        tree = ET.ElementTree(file='infor.xml')
        root = tree.getroot()
        print("*"*100)
        print("user's info:")
        for user in root:
            print(user[0].text, user[1].text)
        print("*" * 100)

    #实现数据驱动测试,@data 是从test.csv中获取数据,unpack是将返回的list数据分解成函数对应的参数
    @data(*get_csv_data('test.csv'))
    @unpack
    def test_F1_ddt(self,targer_url,elem_id,search_name):
        '''
        ddt是实现数据驱动测试的一个库
        '''
        self.driver.get(targer_url)
        sleep(1)
        input_elem = self.driver.find_element_by_id(elem_id)
        input_elem.clear()
        input_elem.send_keys(search_name)
        input_elem.submit()
        sleep(3)



if __name__ == "__main__":
    '''
    在pycharm中运行程序，测试用例能够正常执行，但是在report文件夹中，没有生成测试报告；
    这是因为编辑器为了方便用户执行测试，都有一项功能，可以用编辑器来调用unittest或者nose来执行测试用例，
    这种情况下，执行的只是用例或者套件，而不是整个文件，写在main里的代码是不会被执行的，自然无法生成报告。
    解决办法:可以先删掉之前的运行方式。
    在Edit Configurations 中点击减号删除多余的配置，删除之前的运行文件，后点加号重新添加需要执行的问题，再次执行即可；
    '''
    # 运行方法1，不过没有测试报告
    # unittest.main()
    # 运行方法2，同样没有测试报告
    # testcases = unittest.TestLoader().loadTestsFromTestCase(MyTestCase)
    # test_suite = unittest.TestSuite([testcases])
    # unittest.TextTestRunner(verbosity=2).run(test_suite)
    #方法3，输出测试报告
    # suite = unittest.suite()
    # suite.addTests(unittest.TestLoad().loadTestSFromTestCase(MyTestCase))
    # with open(filename, 'wb') as fp:
    #     runner = HTMLTestRunner(stream=fp, title='Selenium_report', description='selenium测试用例')
    # runner.run(suite)
    # #方法4，生成测试报告
    unittest.main(testRunner=HtmlTestRunner.HTMLTestRunner(
        #目录
        output='report',
        #文件前缀名
        report_name='Selenium_report',
        #报告标题
        report_title='Report'
    ))