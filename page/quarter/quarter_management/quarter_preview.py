import json

from common.contants import quarter_preview_dir
from page.base.basepage import BasePage


class Quarter_Preview(BasePage):

    def wait_sleep(self,sleeps):
        self.sleep(sleeps)
        return self

    def stop_publishing(self):
        '''
        點擊停止發佈
        '''
        self.step(quarter_preview_dir,"stop_publishing")
        return self

    def get_publish_setting_information(self,quarter_name):
        '''
        僅針對“進行中、已結束”狀態
        '''
        information = {}
        self.step(quarter_preview_dir,"click_publish_setting")
        information["問卷名稱"] = quarter_name
        information["發佈類型"] = self.step(quarter_preview_dir,"get_publish_type")
        # 教職員-個人
        information["教職員-個人"] = self.step(quarter_preview_dir,"get_t_personal")
        # 教職員-部門
        information["教職員-部門"] = self.step(quarter_preview_dir,"get_t_section")
        #學生-個人
        information["學生-個人"] = self.step(quarter_preview_dir,"get_s_personal")
        # 學生-多條件選擇
        # 判断是否为无
        is_null = self.step(quarter_preview_dir,"is_null")
        if is_null == "無":
            s_Multi_Condition = self.step(quarter_preview_dir,"is_null")
        else:
            tds = self.step(quarter_preview_dir,"get_s_Multi_Condition_num")
            mult_condi = {}
            for i in range(1,tds+1):
                self._params["i"] = i
                title = self.step(quarter_preview_dir,"get_title")
                value = self.step(quarter_preview_dir,"get_value")
                mult_condi[title] = value
            s_Multi_Condition = mult_condi
        information["學生-多條件選擇"] = s_Multi_Condition
        information["外部人員"] = self.step(quarter_preview_dir,"get_outsiders")
        information["问卷管理人员"] = self.step(quarter_preview_dir,"get_quarter_admin")
        # 點擊關閉抽屜頁面
        self.step(quarter_preview_dir,"close_publish_setting")
        print(json.dumps(information,indent=4,ensure_ascii=False))
        return self

    def back_to_quarter_management(self):
        '''
        返回問卷股那裏列表
        '''
        self.step(quarter_preview_dir,"back_to_quarter_management")
        from page.quarter.quarter_management.quarter_management import Quarter_Management
        return Quarter_Management(self._driver)