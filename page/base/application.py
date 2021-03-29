from common.contants import application_dir
from page.base.basepage import BasePage
from page.quarter.quarterPage import QuarterPage


class Application(BasePage):

    def wait_sleep(self,sleeps):
        self.sleep(sleeps)
        return self

    def goto_quarter(self, application):
        '''
        進入問卷應用
        '''
        self._params["application"] = application
        self.step(application_dir, "goto_quarter")
        return QuarterPage(self._driver)


