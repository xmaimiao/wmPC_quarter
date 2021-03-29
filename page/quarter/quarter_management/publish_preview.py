from common.contants import publish_preview_dir
from page.base.basepage import BasePage
from page.quarter.quarter_management.publishing_setting import Publishing_Setting


class Publish_Preview(BasePage):
    def click_next(self):
        self.step(publish_preview_dir,"click_next")
        return Publishing_Setting(self._driver)

    def get_save_draft_toast(self):
        return self.step(publish_preview_dir,"get_save_draft_toast")