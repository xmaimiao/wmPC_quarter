import re
from common.contants import quarter_management_dir
from page.base.basepage import BasePage
from page.quarter.quarter_management.create_quarter import Create_Quarter
from page.quarter.quarter_management.quarter_preview import Quarter_Preview


class Quarter_Management(BasePage):

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
            self.step(quarter_management_dir,"quarter_type")
        self.step(quarter_management_dir,"search_input")
        return self

    def advanced_search(self,keys):
        '''
        高级查詢，傳進來一個字典
        {startTime:{switch:False,value:2020/01/05},endStartTime:{switch:False,value:2020/01/05},
        startPlanExpireTime:{switch:False,value:2020/01/05},endPlanExpireTime:{switch:False,value:2020/01/05},
        startFinishedNumber:{switch:False,value:0},endFinishedNumber:{switch:False,value:0},
        startPushNumber:{switch:False,value:0},endPushNumber:{switch:False,value:0},
        createdName:{switch:False,value:xxx},
        telOrEmail:{switch:False,value:xxx},
        frequency:{switch:False,value:每天},
        peopleOriented:{switch:False,value:限定人群},
        status:{switch:False,value:進行中},
        '''
        self.step(quarter_management_dir, "click_advanced_search")
        if keys["startTime"]["switch"] == True:
            self._params["startTime"] = keys["startTime"]["value"]
            self.step(quarter_management_dir,"startTime")
        if keys["endStartTime"]["switch"] == True:
            self._params["endStartTime"] = keys["endStartTime"]["value"]
            self.step(quarter_management_dir,"endStartTime")
        if keys["startPlanExpireTime"]["switch"] == True:
            self._params["startPlanExpireTime"] = keys["startPlanExpireTime"]["value"]
            self.step(quarter_management_dir,"startPlanExpireTime")
        if keys["endPlanExpireTime"]["switch"] == True:
            self._params["endPlanExpireTime"] = keys["endPlanExpireTime"]["value"]
            self.step(quarter_management_dir,"endPlanExpireTime")
        if keys["startFinishedNumber"]["switch"] == True:
            self._params["startFinishedNumber"] = keys["startFinishedNumber"]["value"]
            self.step(quarter_management_dir,"startFinishedNumber")
        if keys["endFinishedNumber"]["switch"] == True:
            self._params["endFinishedNumber"] = keys["endFinishedNumber"]["value"]
            self.step(quarter_management_dir,"endFinishedNumber")
        if keys["startPushNumber"]["switch"] == True:
            self._params["startPushNumber"] = keys["startPushNumber"]["value"]
            self.step(quarter_management_dir,"startPushNumber")
        if keys["endPushNumber"]["switch"] == True:
            self._params["endPushNumber"] = keys["endPushNumber"]["value"]
            self.step(quarter_management_dir,"endPushNumber")
        # 查詢問卷名稱
        if keys["title"]["switch"] == True:
            self._params["title"] = keys["title"]["value"]
            self.step(quarter_management_dir,"title")
        # 查詢問卷創建人
        if keys["createdName"]["switch"] == True:
            self._params["createdName"] = keys["createdName"]["value"]
            self.step(quarter_management_dir,"createdName")
        # 查詢電話/郵箱
        if keys["telOrEmail"]["switch"] == True:
            self._params["telOrEmail"] = keys["telOrEmail"]["value"]
            self.step(quarter_management_dir,"startTime")
        # 查詢推送週期
        if keys["frequency"]["switch"] == True:
            self._params["frequency"] = keys["frequency"]["value"]
            self.step(quarter_management_dir, "frequency")
        # 查詢問卷類型
        if keys["peopleOriented"]["switch"] == True:
            self._params["peopleOriented"] = keys["peopleOriented"]["value"]
            self.step(quarter_management_dir, "peopleOriented")
        # 查询問卷状态
        if keys["status"]["switch"] == True:
            self._params["status"] = keys["status"]["value"]
            self.step(quarter_management_dir, "status")
        self.step(quarter_management_dir,"click_search")
        return self



    def create_quarter(self):
        '''
        創建問卷
        '''
        self.step(quarter_management_dir,"create_quarter")
        return Create_Quarter(self._driver)

    def get_create_ele(self):
        '''
        獲取 創建問卷 按鈕元素，判斷判斷創建成功
        '''
        return self.step(quarter_management_dir,"get_create_ele")

    def delete_quarter_for_name(self,quarter_name):
        '''
        刪除問卷,通過問卷名稱刪除第一行數據
        返回1
        '''
        self._params["quarter_name"] = quarter_name
        before = self.step(quarter_management_dir,"get_quarter_total")
        before = int(re.search("(\d+).*?(\d+).*", before).group(2))
        try:
            self.step(quarter_management_dir,"delete_quarter_for_name")
            after = self.step(quarter_management_dir, "get_quarter_total")
            after = int(re.search("(\d+).*?(\d+).*", after).group(2))
            return before - after
        except Exception as e:
            print("數據沒有“刪除”按鈕！")
            raise e

    def delete_quarter_the_fir(self):
        '''
        刪除問卷列表第一行數據
        '''
        before = self.step(quarter_management_dir,"get_quarter_total")
        before = int(re.search("(\d+).*?(\d+).*", before).group(2))
        try:
            self.step(quarter_management_dir,"delete_quarter_the_fir")
            after = self.step(quarter_management_dir, "get_quarter_total")
            after = int(re.search("(\d+).*?(\d+).*", after).group(2))
            return before - after
        except Exception as e:
            print("數據沒有“刪除”按鈕！")
            raise e

    def get_quarter_auths_the_fir(self):
        '''
        獲取問卷第一行數據操作權限，驗證管理員無刪除操作
        '''
        return self.step(quarter_management_dir,"get_quarter_auths_the_fir")

    def edit_quarter_the_fir(self):
        '''
        編輯第一行問卷數據
        '''
        self.step(quarter_management_dir,"edit_quarter_the_fir")
        return Create_Quarter(self._driver)

    def copy_quarter_the_fir(self):
        '''
        复制第一行問卷數據
        '''
        self.step(quarter_management_dir,"copy_quarter_the_fir")
        return Create_Quarter(self._driver)

    def view_quarter_the_fir(self):
        '''
        查看第一行問卷數據
        '''
        self.step(quarter_management_dir,"view_quarter_the_fir")
        return Quarter_Preview(self._driver)

    def view_quarter_for_name(self,quarter_name):
        '''
        通過傳入的問卷名稱，查看問卷數據
        '''
        self._params["quarter_name"] = quarter_name
        self.step(quarter_management_dir,"view_quarter_for_name")
        return Quarter_Preview(self._driver)

    def get_quarter_name_the_fir(self):
        '''
        获取第一行問卷的名稱
        '''
        try:
            quarter_name = self.step(quarter_management_dir,"get_quarter_name_the_fir")
            print(f"quarter_name:{quarter_name}")
            return quarter_name
        except Exception as e:
            print("暫無數據!")
            raise e

    def get_quarter_status_the_fir(self):
        '''
        獲取第一行問卷的狀態
        '''
        return self.step(quarter_management_dir,"get_quarter_status_the_fir")

    def get_quarter_status_for_name(self,quarter_name):
        '''
        通過問卷名稱獲取問卷的狀態
        '''
        self._params["quarter_name"] = quarter_name
        return self.step(quarter_management_dir,"get_quarter_status_for_name")

    def get_add_quarter_ele(self):
        '''
        獲取“添加問卷”元素，驗證返回問卷管理頁面
        '''
        try:
            return self.step(quarter_management_dir,"get_add_quarter_ele")
        except Exception as e:
            raise e


