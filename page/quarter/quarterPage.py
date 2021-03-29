from common.contants import quarterPage_dir
from page.base.basepage import BasePage
from page.quarter.my_quarter.my_quarter import My_Quarter
from page.quarter.quarter_management.quarter_management import Quarter_Management
from page.quarter.quarter_statistic.quarter_statistic import Quarter_Statistic


class QuarterPage(BasePage):
    def goto_quarter_management(self):
        '''
        打開問卷管理
        '''
        self.step(quarterPage_dir,"goto_quarter_management")
        return Quarter_Management(self._driver)

    def goto_my_quarter(self):
        '''
        打開我的問卷
        '''
        self.step(quarterPage_dir,"goto_my_quarter")
        return My_Quarter(self._driver)

    def goto_quarter_statistics(self):
        '''
        打開問卷統計
        '''
        self.step(quarterPage_dir,"goto_quarter_statistics")
        return Quarter_Statistic(self._driver)