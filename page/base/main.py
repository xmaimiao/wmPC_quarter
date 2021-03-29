import yaml

from common.contants import basepage_dir, main1_dir, quarterPage_dir, publish_preview_dir
from page.base.basepage import BasePage, _get_working
from page.base.index import Index
from page.base.loginpage import Login
from page.quarter.my_quarter.my_quarter import My_Quarter
from page.quarter.quarter_management.publishing_setting import Publishing_Setting
from page.quarter.quarter_management.quarter_management import Quarter_Management
from page.quarter.quarter_statistic.quarter_statistic import Quarter_Statistic


class Main(BasePage):
    '''
    首頁面po
    '''
    _working = _get_working()

    with open(basepage_dir, encoding="utf-8") as f:
        env = yaml.safe_load(f)
        if _working != "port":
            _base_url = env["docker_env"][env["default"]]

    def goto_login(self):
        '''
        進去登錄頁面
        '''
        return Login(self._driver)

    def goto_index(self):
        '''
        打開首頁
        '''
        return Index(self._driver)

    def goto_quarter_management(self):
        '''
        打開問卷管理
        '''
        self.step(quarterPage_dir, "goto_quarter_management")
        return Quarter_Management(self._driver)

    def goto_my_quarter(self):
        '''
        打開我的問卷
        '''
        self.step(quarterPage_dir, "goto_my_quarter")
        return My_Quarter(self._driver)

    def goto_quarter_statistics(self):
        '''
        打開問卷統計
        '''
        self.step(quarterPage_dir,"goto_quarter_statistics")
        return Quarter_Statistic(self._driver)

    def OA_goto_index(self):
        '''
        OA/一期應用進入首頁
        '''
        self.step(main1_dir,"OA_goto_index")
        return Index(self._driver)


    def logout_for_fir(self):
        '''
        一期應用中退出登錄
        '''
        self.step(main1_dir,"logout_for_fir")
        return Login(self._driver)

    def logout_for_sec(self):
        '''
        二期應用中退出登錄
        '''
        self.step(main1_dir,"logout_for_sec")
        return Login(self._driver)


    def click_next(self):
        self.step(publish_preview_dir, "click_next")
        return Publishing_Setting(self._driver)

    def the_sec_goto_index(self):
        '''
        在二期應用中打開首頁
        '''
        self.step(main1_dir,"the_sec_goto_index")
        return Index(self._driver)

