import win32con
import win32gui

from common.contants import choice_question_detail_dir, img_dir
from page.base.basepage import BasePage

class Choice_Question_Detail(BasePage):

    def choice_question(self,subject_name,option_list):
        '''
        題目標題\選項
        '''
        self._params["subject_name"] = subject_name
        self.step(choice_question_detail_dir, "subject_name")
        i=0
        for option in option_list:
            i += 1
            # self._params["item"] = option["item"]
            eles = self.step(choice_question_detail_dir,"get_item_eles")
            eles[-1].clear()
            eles[-1].send_keys(option["item"])
            if option["is_other"] == True:
                # 勾選支持文本輸入框
                self.sleep(1)
                other_ele = self.step(choice_question_detail_dir, "get_other_eles")
                other_ele[-1].click()

            if option["tips"]["switch"] == True:
                # 輸入選項説明
                # self.sleep(1)
                other_ele = self.step(choice_question_detail_dir, "get_tips_eles")
                other_ele[-1].click()
                self._params["option_tips"] = option["tips"]["option_tips"]
                self.step(choice_question_detail_dir,"input_options_tips")

            if option["is_img"] == True:
                print(f"i:{i}")
                # 上傳圖片
                self.sleep(1)
                img_eles = self.step(choice_question_detail_dir, "get_img_eles")
                img_eles[i-1].click()
                self.sleep(2)
                # 找元素
                # 一级窗口"#32770","打开"
                dialog = win32gui.FindWindow("#32770", "打开")
                # 向下传递
                ComboBoxEx32 = win32gui.FindWindowEx(dialog, 0, "ComboBoxEx32", None)  # 二级
                comboBox = win32gui.FindWindowEx(ComboBoxEx32, 0, "ComboBox", None)  # 三级
                # 编辑按钮
                edit = win32gui.FindWindowEx(comboBox, 0, 'Edit', None)  # 四级
                # 打开按钮
                button = win32gui.FindWindowEx(dialog, 0, 'Button', "打开(&O)")  # 二级

                # 输入文件的绝对路径，点击“打开”按钮
                win32gui.SendMessage(edit, win32con.WM_SETTEXT, None, img_dir)  # 发送文件路径
                win32gui.SendMessage(dialog, win32con.WM_COMMAND, 1, button)  # 点击打开按钮
                self.sleep(2)
            if i < len(option_list):
                # 點擊添加選項符號
                # 不等待会被遮挡元素
                self.sleep(1)
                add_eles = self.step(choice_question_detail_dir,"get_add_eles")
                add_eles[-1].click()
        # 不等待会被遮挡元素
        self.sleep(1)
        self.step(choice_question_detail_dir, "click_save")
        from page.quarter.quarter_management.create_quarter import Create_Quarter
        return Create_Quarter(self._driver)
