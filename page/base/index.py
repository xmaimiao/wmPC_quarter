from common.contants import index_dir
from page.base.application import Application
from page.base.basepage import BasePage


class Index(BasePage):

    def wait_sleep(self,sleeps):
        self.sleep(sleeps)
        return self

    def goto_application(self):
        self.step(index_dir,"goto_application")
        return Application(self._driver)


    def quit(self):
        '''
        推出當前登陸賬號
        :return:
        '''
        self.step(index_dir,"quit")

    def get_index_ele_fir(self):
        '''
        獲取應用-“首頁”元素，驗證登錄成功，一期
        '''
        return self.step(index_dir,"get_index_ele_fir")

    def get_index_ele_sec(self):
        '''
        獲取應用-“首頁”元素，驗證登錄成功，二期
        '''
        return self.step(index_dir,"get_index_ele_sec")

    def get_imformation_ele_index(self):
        '''
        獲取"系統消息"ele，驗證跳轉首頁正確
        '''
        return self.step(index_dir,"get_imformation_ele_index")

