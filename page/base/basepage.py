import json
import logging
import os
from time import sleep
import yaml
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from common.contants import basepage_dir
from page.base.handle_black import handlie_blacklist


def _get_working():
    '''
    读入配置文件,判断是启用调试端口 还是启用docker-grid
    '''
    with open(basepage_dir, encoding="utf-8") as f:
        data = yaml.safe_load(f)
        working = data["switch"][data["switch_default"]]
        return working

class BasePage:

    _driver = None
    _params={}
    _base_url = ""
    _working = _get_working()
    _chrome_options = Options()
    # 清理已有 handlers
    root_logger = logging.getLogger()
    for h in root_logger.handlers[:]:
        root_logger.removeHandler(h)
    logging.basicConfig(level=logging.INFO)

    def __init__(self,driver:WebDriver = None):

        if driver is None:
            if self._working == "port":
                # 和瀏覽器打開的調試端口進行通信，瀏覽器要使用 --remote-debugging-port=9222 開啟調試
                self._chrome_options.debugger_address = "127.0.0.1:9222"
                self._driver = webdriver.Chrome(options=self._chrome_options)

            elif self._working == "headless":
                # 無界面方式打开浏览器
                self._chrome_options.add_argument("--headless")
                self._chrome_options.add_argument("--window-size=1920,1080")
                self._driver = webdriver.Chrome(chrome_options=self._chrome_options)

            elif self._working == "brower":
                # 有界面方式打开浏览器
                self._driver = webdriver.Chrome()

            elif self._working == "docker":
                #Docker+Selenium Grid+Python搭建分布式测试环境
                chrome_driver = os.path.abspath("D:\Program Files (x86)\Google Chrome\chromedriver.exe")
                os.environ["webdriver.chrome.driver"] = chrome_driver
                chrome_capabilities = {
                    "browserName": "chrome",
                    "version": "",
                    "platform": "ANY",
                    "javascriptEnabled": True,
                    "webdriver.chrome.driver": chrome_driver
                }
                self._driver = webdriver.Remote(
                    command_executor='http://192.168.99.100:5555/wd/hub',
                    desired_capabilities=chrome_capabilities)

            self._driver.maximize_window()
            self._driver.implicitly_wait(3)
        else:
            self._driver = driver

        if self._base_url != "":
            self._driver.get(self._base_url)

    @handlie_blacklist
    def _find(self,by,locator):
        # 调用find函数即打印日志
        logging.info(f"find：{locator}")
        if by == None:
            result=self._driver.find_element(*locator)
        else:
            result = self._driver.find_element(by,locator)
        return result

    def _finds(self,by,locator):
        logging.info(f"finds：{locator}")
        return self._driver.find_elements(by,locator)

    def _move_to_ele(self,by,locator):
        '''
        模擬鼠標懸停
        '''
        logging.info(f"move_to_ele：{locator}")
        return ActionChains(self._driver).move_to_element(self._find(by,locator)).perform()

    def _find_and_click(self,by,locator):
        logging.info(f"click：{locator}")
        self._find(by,locator).click()

    def _find_and_sendkeys(self,by,locator,value):
        logging.info(f"sendkeys：{value}")
        self._find(by,locator).send_keys(value)

    def _action_click(self,by,locator):
        '''
        模拟鼠标点击
        '''
        logging.info(f"action_click：{locator}")
        ActionChains(self._driver).click(self._find(by,locator)).perform()

    def _ctrl_a(self,by,locator):
        '''
        通过键盘全选达到清空效果，即模拟发起ctrl+a( 用於element.clear()清空输入框失效)
        '''
        logging.info(f"ctrl_a：{locator}")
        self._find(by,locator).send_keys(Keys.CONTROL, 'a')

    def _webdriver_wait(self,by,locator,timeout=10):
        '''
        等待元素出現
        '''
        logging.info(f"action_click：{locator}")
        logging.info(f"wait：{locator},timeout：{timeout}")
        # WebDriverWait(self._driver, timeout).until(lambda x:x.find_element(by,locator))
        WebDriverWait(self._driver, timeout).until(expected_conditions.visibility_of_element_located((by,locator)))

    def _wait_for_click(self,by,locator,timeout=10):
        ''''
        等待元素可出現且可點擊
        '''
        logging.info(f"wait_click：{locator},timeout：{timeout}")
        WebDriverWait(self._driver,timeout).until(expected_conditions.element_to_be_clickable((by,locator)))

    def _wait_for_display(self,by,locator,timeout=10):
        '''
        等待元素出現，一旦出現就不斷查找元素，用於獲取toast
        '''
        logging.info(f"wait_display：{locator},timeout：{timeout}")
        stutas = WebDriverWait(self._driver, timeout).until(expected_conditions.visibility_of_element_located((by,locator)))
        if stutas:
            ele= self._find(by,locator)
            return ele
        return ValueError("元素不存在")

    def _find_ele_status(self,by,locator):
        '''
        用来判断元素标签是否存在
        '''
        logging.info(f"find_ele_status：{locator}")
        try:
            self._find(by, locator)
        except Exception as e:
            # 发生了NoSuchElementException异常，说明页面中未找到该元素，返回False
            return False
        else:
            # 没有发生异常，表示在页面中找到了该元素，返回True
            return True

    def sleep(self,time):
        logging.info(f"sleep：{time}")
        sleep(time)

    def _execute_script(self,script):
        '''
        通过js查找元素
        '''
        logging.info(f"execute_js：{script}")
        self._driver.execute_script(f'{script}')

    def _execute_script_click(self,script):
        '''
        通过js查找元素，并click
        '''
        logging.info(f"execute_js_click：{script}")
        ele = self._driver.execute_script(f'{script}')
        ele.click()


    def _wait_for_condition(self,condition,timeout=10):
        '''
        等待直到xxx條件成立
        '''
        WebDriverWait(self._driver, timeout).until(condition)

    # def click_until_next_ele_display(self,by,locator,by_next,locator_next,timeout=10):
    #     '''
    #     不斷點擊當前元素直到下一個元素出現，停止點擊。調用wait_for_condition方法
    #     '''
    #     elements_len = len(self.finds(by_next,locator_next))
    #     if elements_len <= 0:
    #         self.find_and_click(by,locator)
    #     return elements_len >0
    # wait_for_condition(click_until_next_ele_display):

    def execute_script_scroll(self,script):
        '''
        滑動到元素可見
        '''
        logging.info(f"execute_script_scroll：{script}")
        ele = self._driver.execute_script(f'{script}')
        js4 = "arguments[0].scrollIntoView();"
        self._driver.execute_script(js4, ele)

    def find_ele_scroll(self,by, locator):
        '''
        滑動到元素可見
        '''
        logging.info(f"find_ele_scroll：{locator}")
        ele = self._driver.find_element(by, locator)
        js4 = "arguments[0].scrollIntoView();"
        self._driver.execute_script(js4, ele)

    def move_to_element(self,by, locator):
        '''
        懸浮在元素上
        '''
        logging.info(f"move_to_element：{locator}")
        ele = self._driver.find_element(by, locator)
        ActionChains(self._driver).move_to_element(ele).perform()

    def _wait_swith_to_iframe(self,by,locator,timeout=10):
        '''
        等待直到找到iframe元素才切换
        '''
        logging.info(f"wait_swith_to_iframe：{locator},timeout：{timeout}")
        iframe_ele = self._find(by, locator)
        WebDriverWait(self._driver, timeout).until(expected_conditions.frame_to_be_available_and_switch_to_it(iframe_ele))

    # driver.switch_to.frame(0)  # 1.用frame的index来定位，第一个是0
    # driver.switch_to.frame("frame1")  # 2.用id来定位
    # driver.switch_to.frame("myframe")  # 3.用name来定位
    # driver.switch_to.frame(driver.find_element_by_tag_name("iframe"))  # 4.用WebElement对象来定位

    def _set_implicitly_wait(self,second):
        '''
        顯性等待
        '''
        self._driver.implicitly_wait(second)

    def close(self):
        self._driver.quit()

    def step(self,path,name):
        with open(path, encoding="utf-8") as f:
            steps = yaml.safe_load(f)[name]
        # ${}的參數轉化
        raw_data = json.dumps(steps)
        for key,value in self._params.items():
            raw_data = raw_data.replace("${"+key+"}",str(value))
        steps = json.loads(raw_data)
        for step in steps:
            if "action" in step.keys():
                action = step["action"]
                if "wait_click" == action:
                    self._wait_for_click(step["by"],step["locator"])
                if "wait" == action:
                    self._webdriver_wait(step["by"], step["locator"])
                if "send" == action:
                    self._find_and_sendkeys(step["by"], step["locator"], step["value"])
                if "click" == action:
                    self._find_and_click(step["by"],step["locator"])
                if "len" == action:
                    eles = self._finds(step["by"], step["locator"])
                    return len(eles)
                if "text" == action:
                    text = self._find(step["by"], step["locator"]).text
                    return text
                if "clear" == action:
                    self._find(step["by"], step["locator"]).clear()
                if "wait_display" == action:
                    ele = self._wait_for_display(step["by"], step["locator"])
                    return ele
                if "move" == action:
                    self._move_to_ele(step["by"], step["locator"])
                if "ele_status" == action:
                    return self._find_ele_status(step["by"], step["locator"])
                if "sleep" == action:
                    sleep(step["locator"])
                if "action_click" == action:
                    self._action_click(step["by"], step["locator"])
                if "eles" == action:
                    return self._finds(step["by"], step["locator"])
                if "execute_js_click" == action:
                    self._execute_script_click(step["locator"])
                if "execute_js" == action:
                    self._execute_script(step["locator"])
                if "execute_js_scroll" == action:
                    self.execute_script_scroll(step["locator"])
                if "find_scroll" == action:
                    self.find_ele_scroll(step["by"], step["locator"])
                if "wait_and_iframe" == action:
                    self._wait_swith_to_iframe(step["by"], step["locator"])
                if "move_to_ele" == action:
                    self.move_to_element(step["by"], step["locator"])
                if "ctrl_a" == action:
                    self._ctrl_a(step["by"], step["locator"])

if __name__ == '__main__':
    BasePage()
