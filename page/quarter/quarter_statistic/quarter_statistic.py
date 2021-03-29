from common.contants import quarter_statistic_dir
from page.base.basepage import BasePage
from page.quarter.quarter_statistic.quarter_statistic_detail import Quarter_Statistic_Detail


class Quarter_Statistic(BasePage):

    def wait_sleep(self,sleeps):
        self.sleep(sleeps)
        return self

    def simple_search(self,keys):
        '''
        簡易查詢，傳進來一個字典{quarter_type:"全部",keywords:xxxx}
        '''
        self._params["quarter_name"] = keys["quarter_name"]
        self.step(quarter_statistic_dir,"search_input")
        return self

    def advanced_search(self,keys):
        '''
        高级查詢，傳進來一個字典
        {startTime:{switch:False,value:2020/01/05},endStartTime:{switch:False,value:2020/01/05},
        startPlanExpireTime:{switch:False,value:2020/01/05},endPlanExpireTime:{switch:False,value:2020/01/05},
        startFinishedNumber:{switch:False,value:0},endFinishedNumber:{switch:False,value:0},
        startPushNumber:{switch:False,value:0},endPushNumber:{switch:False,value:0},
        frequency:{switch:False,value:每天},
        peopleOriented:{switch:False,value:限定人群},
        status:{switch:False,value:進行中},
        '''
        self.step(quarter_statistic_dir, "click_advanced_search")
        # if keys["startTime"]["switch"] == True:
        #     self._params["startTime"] = keys["startTime"]["value"]
        #     self.step(quarter_statistic_dir,"startTime")
        # if keys["endStartTime"]["switch"] == True:
        #     self._params["endStartTime"] = keys["endStartTime"]["value"]
        #     self.step(quarter_statistic_dir,"endStartTime")
        # if keys["startPlanExpireTime"]["switch"] == True:
        #     self._params["startPlanExpireTime"] = keys["startPlanExpireTime"]["value"]
        #     self.step(quarter_statistic_dir,"startPlanExpireTime")
        # if keys["endPlanExpireTime"]["switch"] == True:
        #     self._params["endPlanExpireTime"] = keys["endPlanExpireTime"]["value"]
        #     self.step(quarter_statistic_dir,"endPlanExpireTime")
        # 回收數量-前置
        if keys["startFinishedNumber"]["switch"] == True:
            self._params["startFinishedNumber"] = keys["startFinishedNumber"]["value"]
            self.step(quarter_statistic_dir,"startFinishedNumber")
        # 回收數量-後置
        if keys["endFinishedNumber"]["switch"] == True:
            self._params["endFinishedNumber"] = keys["endFinishedNumber"]["value"]
            self.step(quarter_statistic_dir,"endFinishedNumber")
        # if keys["startPushNumber"]["switch"] == True:
        #     self._params["startPushNumber"] = keys["startPushNumber"]["value"]
        #     self.step(quarter_statistic_dir,"startPushNumber")
        # if keys["endPushNumber"]["switch"] == True:
        #     self._params["endPushNumber"] = keys["endPushNumber"]["value"]
        #     self.step(quarter_statistic_dir,"endPushNumber")
        # 查詢問卷名稱
        if keys["title"]["switch"] == True:
            self._params["title"] = keys["title"]["value"]
            self.step(quarter_statistic_dir,"title")
        # # 查詢推送週期
        # if keys["frequency"]["switch"] == True:
        #     self._params["frequency"] = keys["frequency"]["value"]
        #     self.step(quarter_statistic_dir, "frequency")
        # # 查詢問卷類型
        # if keys["peopleOriented"]["switch"] == True:
        #     self._params["frequency"] = keys["peopleOriented"]["value"]
        #     self.step(quarter_statistic_dir, "peopleOriented")
        # 查询問卷状态
        if keys["status"]["switch"] == True:
            self._params["status"] = keys["status"]["value"]
            self.step(quarter_statistic_dir, "status")
        self.step(quarter_statistic_dir,"click_search")
        return self


    def view_the_fir(self,quarter_name):
        '''
        點擊第一行數據“查看”按鈕
        '''
        self._params["quarter_name"] = quarter_name
        self.step(quarter_statistic_dir,"view_the_fir")
        return Quarter_Statistic_Detail(self._driver)

    def get_quarter_name_the_fir(self):
        '''
        編輯第一行問卷的名稱
        '''
        try:
            return self.step(quarter_statistic_dir,"get_quarter_name_the_fir")
        except Exception as e:
            print("暫無數據!")
            raise e

    def get_quarter_status_the_fir(self):
        '''
        編輯第一行問卷的狀態
        '''
        try:
            return self.step(quarter_statistic_dir,"get_quarter_status_the_fir")
        except Exception as e:
            print("暫無數據!")
            raise e