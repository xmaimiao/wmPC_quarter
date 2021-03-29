from common.contants import create_quarter_dir, quarterPage_dir
from page.base.basepage import BasePage
from page.quarter.quarter_management.choice_question_detail import Choice_Question_Detail
from page.quarter.quarter_management.publish_preview import Publish_Preview
from page.quarter.quarter_management.subjective_question_detail import Subjective_Question_Detail


class Create_Quarter(BasePage):

    def wait_sleep(self,sleeps):
        self.sleep(sleeps)
        return self

    def quarter_name(self,quarter_name):
        '''
        問卷名稱
        '''
        self._params["quarter_name"] = quarter_name
        self.step(create_quarter_dir,"quarter_name")
        return self

    def quarter_remark(self,quarter_remark):
        '''
        問卷説明
        '''
        self._params["quarter_remark"] = quarter_remark
        self.step(create_quarter_dir,"quarter_remark")
        return self

    def add_choice_question(self):
        '''
        添加選擇題
        '''
        js="window.scrollTo(10000,10000);"
        self._driver.execute_script(js)
        self.sleep(1)
        self.step(create_quarter_dir,"add_choice_question")
        return Choice_Question_Detail(self._driver)

    def add_subjective_question(self):
        '''
        添加主觀題
        '''
        js="window.scrollTo(10000,10000);"
        self._driver.execute_script(js)
        self.sleep(1)
        self.step(create_quarter_dir,"add_subjective_question")
        return Subjective_Question_Detail(self._driver)

    def mult_and_required(self,mult__re):
        '''
        多选题、必答题，传进来一个字典，根据true/false去判断是否勾选必答题、多选题
        '''
        if mult__re["mult"] == True:
            mult_eles = self.step(create_quarter_dir,"mult")
            mult_eles[-1].click()
        if mult__re["required"] == False:
            # 默认为必填项，若传进来是False，则为不必填
            srequired_eles = self.step(create_quarter_dir,"required")
            srequired_eles[-1].click()
        return self

    def save_draft(self):
        '''
        點擊”暫存“，返回toast：保存成功
        '''
        js = "window.scrollTo(0,0);"
        self._driver.execute_script(js)
        self.sleep(1)
        self.step(create_quarter_dir, "click_save_draft")
        return self

    def get_save_draft_toast(self):
        '''
        獲取保存成功的toast
        '''
        return self.step(create_quarter_dir, "get_save_draft_toast")


    def click_next(self):
        '''
        點擊”下一步“
        '''
        js = "window.scrollTo(0,0);"
        self._driver.execute_script(js)
        self.sleep(1)
        self.step(create_quarter_dir,"click_next")
        return Publish_Preview(self._driver)

    def back_to_mangement_list(self):
        '''
        返回管理列表
        '''
        self.step(quarterPage_dir,"goto_quarter_management")
        from page.quarter.quarter_management.quarter_management import Quarter_Management
        return Quarter_Management(self._driver)