from common.contants import quarter_detial_dir
from page.base.basepage import BasePage


class Quarter_Detial(BasePage):
    def question(self,subjects):
        '''
        根據傳進來的數組，若為true就去 ({num:1,text_switch:false,text:"測試數據"},{},{})
        '''
        self._driver.switch_to.frame(0)
        self.sleep(1)
        for subject in subjects:
            self._params["subject_num"] = subject["subject_num"]
            print("11111")
            if subject["is_choice"] == True:
                for option in subject["options"]:
                        print("2222")
                        self._params["item_num"] = option["item_num"]
                        if subject["is_single"] == True:
                            self.step(quarter_detial_dir,"choice_option")
                        else:
                            self.step(quarter_detial_dir, "choice_mult_option")
                        if option["is_other"] == True:
                            print("33333")
                            self._params["content"] = option["content"]
                            self.step(quarter_detial_dir,"input_content")
            else:
                print("4444")
                self._params["text"] = subject["text"]
                self.step(quarter_detial_dir,"subjective_input")
        return self


    def click_save(self):
        self.step(quarter_detial_dir,"click_save")
        from page.quarter.my_quarter.my_quarter import My_Quarter
        return My_Quarter(self._driver)

    def click_close(self):
        '''
        關閉抽屜頁面
        '''
        self.step(quarter_detial_dir,"click_close")
        from page.quarter.my_quarter.my_quarter import My_Quarter
        return My_Quarter(self._driver)

