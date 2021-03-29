from common.contants import subjective_question_detail_dir
from page.base.basepage import BasePage


class Subjective_Question_Detail(BasePage):
    def subjective_question(self,subjective_name,tips,words):
        '''
        主觀題標題\提示語\字數,并单击保存按钮
        '''
        self._params["subjective_name"] = subjective_name
        self._params["tips"] = tips["text"]
        self._params["words"] = words["text"]
        self.step(subjective_question_detail_dir,"subjective_name")
        if tips["switch"] == True:
            self.step(subjective_question_detail_dir,"tips")
        if words["switch"] == True:
            self.step(subjective_question_detail_dir,"words")
        self.step(subjective_question_detail_dir,"click_save")
        from page.quarter.quarter_management.create_quarter import Create_Quarter
        return Create_Quarter(self._driver)

