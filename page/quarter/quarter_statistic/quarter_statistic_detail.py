import json

from common.contants import quarter_statistic_detail_dir
from page.base.basepage import BasePage


class Quarter_Statistic_Detail(BasePage):
    def view_releasedrange(self):
        '''
        點擊 發佈範圍 按鈕
        '''
        self.step(quarter_statistic_detail_dir,"view_releasedrange")
        return self

    def releasedrange_detail(self):
        '''
        發佈範圍詳情
        '''
        releasedrange = {"教職員":{},"學生":{}}
        releasedrange["教職員"]["個人"] =(self.step(quarter_statistic_detail_dir,"get_teacher_person")).text
        releasedrange["教職員"]["部門"]= (self.step(quarter_statistic_detail_dir,"get_teacher_group")).text
        releasedrange["學生"]["個人"] = (self.step(quarter_statistic_detail_dir,"get_student_person")).text
        releasedrange["學生"]["多條件組合"] = self.step(quarter_statistic_detail_dir,"get_student_multi_cond").text
        releasedrange["外部人員"] = (self.step(quarter_statistic_detail_dir,"get_outsider")).text
        self.step(quarter_statistic_detail_dir,"close_page")
        print(json.dumps(releasedrange, indent=4, ensure_ascii=False))
        from page.quarter.quarter_statistic.quarter_statistic import Quarter_Statistic
        return Quarter_Statistic(self._driver)