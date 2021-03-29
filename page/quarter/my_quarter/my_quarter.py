from common.contants import my_quarter_dir
from page.base.basepage import BasePage
from page.quarter.my_quarter.quarter_detial import Quarter_Detial


class My_Quarter(BasePage):

    def wait_sleep(self,sleeps):
        self.sleep(sleeps)
        return self

    def simple_search(self,keys):
        '''
        簡易查詢，傳進來一個字典{quarter_type:"全部",keywords:xxxx}
        '''
        self._params["quarter_name"] = keys["quarter_name"]
        if keys["quarter_type"] != "全部":
            self._params["quarter_type"] = keys["quarter_type"]
            self.step(my_quarter_dir,"quarter_type")
        self.step(my_quarter_dir,"search_input")
        return self

    def view_quarter_for_name(self,name):
        '''
        通過問卷名稱打開問卷詳情頁
        '''
        self._params["name"] = name
        self.step(my_quarter_dir,"view_quarter_for_name")
        return Quarter_Detial(self._driver)

    def get_save_toast(self):
        '''
        獲取toast
        '''
        return self.step(my_quarter_dir,"get_save_toasts")

    def get_quarter_name_the_fir(self):
        '''
        編輯第一行問卷的名稱
        '''
        try:
            return self.step(my_quarter_dir,"get_quarter_name_the_fir")
        except Exception as e:
            print("暫無數據!")
            raise e