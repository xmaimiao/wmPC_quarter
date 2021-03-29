import win32con
import win32gui
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys

from common.contants import publishing_setting_dir
from page.base.basepage import BasePage


class Publishing_Setting(BasePage):

    def wait_sleep(self,sleeps):
        self.sleep(sleeps)
        return self

    def quarter_type(self,quarter_type):
        '''
        選擇問卷類型
        '''
        self._params["quarter_type"] = quarter_type
        type = self.step(publishing_setting_dir,"get_quarter_type")
        if type != "請選擇":
            self.step(publishing_setting_dir,"clear_quarter_type")
        self.step(publishing_setting_dir,"quarter_type")

        return self

    def teacher_cancel(self):
        '''
        取消勾選教職工
        '''
        self.step(publishing_setting_dir,"teacher_cancel")
        return self

    def teacher_all_cancel(self):
        '''
        取消勾選教職工-全部
        '''
        self.step(publishing_setting_dir,"teacher_all_cancel")
        return self

    def click_teacher_person(self):
        '''
        教職工發佈範圍：個人
        '''
        # 選擇發佈範圍：教職工-個人
        self.step(publishing_setting_dir, "click_teacher_person")
        return self

    def teacher_person_input(self,range_t,excel_path=None):
        '''
        教職工/學生發佈範圍：個人，傳進來一個字典類型 range_t:{input:True, staffNo:True,}，默認選擇 教職員，賬號
        '''
        if range_t["input"] == True:
            if range_t["staffNo"] == True:
                # 勾選“工號”
                self.step(publishing_setting_dir,"click_staffNo")
            # 輸入人員賬號 or 工號 ，點擊“檢查”
            self._params["staff"] = range_t["staff"]
            self.step(publishing_setting_dir,"input_staff")
        else:
        #     點擊“導入名單”
            self.step(publishing_setting_dir,"upload_list")
            self.sleep(1)
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
            win32gui.SendMessage(edit, win32con.WM_SETTEXT, None, excel_path)  # 发送文件路径
            win32gui.SendMessage(dialog, win32con.WM_COMMAND, 1, button)  # 点击打开按钮
            self.sleep(1)
        return self

    def click_teacher_group(self,group_list):
        '''
        選擇教職工-部門
        '''
        # 勾選部門、點擊“展開”按鈕
        self.step(publishing_setting_dir,"click_teacher_group")
        for group in group_list:
            self._params["group"] = group
            self.step(publishing_setting_dir,"input_group")
        return self

    def click_student(self):
        self.step(publishing_setting_dir,"click_student")
        return self

    def click_student_multi_cond(self,multi_cond):
        '''
        選擇學生-多條件組合，傳進來一個字典
        {college:{switch:False,value:[商學院，人文藝術學院]},
        major:{switch:False,value:[室內設計，廣告學]},
        program:{switch:False,value:[國際旅遊管理學士學位，]},
        term:{switch:False,value:[1907，]},
        student_type:{switch:False,value:[本科，]},
        student_status:{switch:False,value:[在讀生-ACTIVE，]},
        acco_type:{switch:False,value:[非住宿生，]},
        '''
        # 勾選多條件選擇
        self.step(publishing_setting_dir,"click_student_multi_cond")
        if multi_cond["college"]["switch"]== True:
            self.step(publishing_setting_dir, "click_college_select")
            for college in multi_cond["college"]["value"]:
                self._params["college"] = college
                self.step(publishing_setting_dir,"input_college")
        if multi_cond["major"]["switch"] == True:
            self.step(publishing_setting_dir, "click_major_select")
            for major in multi_cond["major"]["value"]:
                self._params["major"] = major
                self.step(publishing_setting_dir,"input_major")
        if multi_cond["program"]["switch"] == True:
            self.step(publishing_setting_dir, "click_program_select")
            for program in multi_cond["program"]["value"]:
                self._params["program"] = program
                self.step(publishing_setting_dir,"input_program")
        if multi_cond["term"]["switch"] == True:
            self.step(publishing_setting_dir, "click_term_select")
            for term in multi_cond["term"]["value"]:
                self._params["term"] = term
                self.step(publishing_setting_dir,"input_term")
        if multi_cond["student_type"]["switch"] == True:
            self.step(publishing_setting_dir, "click_student_type_select")
            for student_type in multi_cond["student_type"]["value"]:
                self._params["student_type"] = student_type
                self.step(publishing_setting_dir,"input_student_type")
        if multi_cond["student_status"]["switch"] == True:
            self.step(publishing_setting_dir, "click_student_status_select")
            for student_status in multi_cond["student_status"]["value"]:
                self._params["student_status"] = student_status
                self.step(publishing_setting_dir,"input_student_status")
        if multi_cond["acco_type"]["switch"] == True:
            self.step(publishing_setting_dir, "click_acco_type_select")
            for acco_type in multi_cond["acco_type"]["value"]:
                self._params["acco_type"] = acco_type
                self.step(publishing_setting_dir,"input_acco_type")
        return self


    def click_student_all(self):
        self.step(publishing_setting_dir,"click_student_all")
        return self

    def click_student_person(self):
        '''
        學生發佈範圍：個人
        '''
        # 選擇發佈範圍：學生-個人
        self.step(publishing_setting_dir, "click_student_person")
        return self

    def student_person_input(self, range_s, excel_path_s=None):
        '''
        教職工/學生發佈範圍：個人，傳進來一個字典類型 range_t:{input:True, staffNo:True,}，默認選擇 教職員，賬號
        '''
        if range_s["input"] == True:
            if range_s["staffNo"] == True:
                # 勾選“工號”
                self.step(publishing_setting_dir,"click_staffNo_s")
            # 輸入人員賬號 or 工號 ，點擊“檢查”
            self._params["staff"] = range_s["staff"]
            self.step(publishing_setting_dir,"input_staff_s")
        else:
        #     點擊“導入名單”
            self.step(publishing_setting_dir,"upload_list_s")
            self.sleep(1)
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
            win32gui.SendMessage(edit, win32con.WM_SETTEXT, None, excel_path_s)  # 发送文件路径
            win32gui.SendMessage(dialog, win32con.WM_COMMAND, 1, button)  # 点击打开按钮
            self.sleep(1)
        return self

    def outsidervolist(self,outsider_path):
        '''
        添加外部人員
        '''
        # 勾選外部人與那，點擊“導入名單”
        self.step(publishing_setting_dir, "upload_outsidervolist")
        self.sleep(1)
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
        win32gui.SendMessage(edit, win32con.WM_SETTEXT, None, outsider_path)  # 发送文件路径
        win32gui.SendMessage(dialog, win32con.WM_COMMAND, 1, button)  # 点击打开按钮
        self.sleep(5)
        self.step(publishing_setting_dir, "close_outsider_pop")
        return self

    def administrator(self,admin_list):
        '''
        選擇管理人員，傳進來一個數組
        '''
        # 滾動條滾動到頁面最下邊
        js="window.scrollTo(10000,10000);"
        self._driver.execute_script(js)
        self.sleep(1)
        # 輸入賬號 or 工號
        for admin in admin_list:
            self._params["admin"] = admin
            self.step(publishing_setting_dir,"input_staff_admin")
        return self

    def starttime(self,startdate,starttime):
        '''
        計劃發佈時間
        '''
        self._params["startdate"] = startdate
        self._params["starttime"] = starttime
        ele = self.step(publishing_setting_dir, "clear_starttime")
        self.sleep(1)
        # 以下同一條數據使用一次之後失效
        # ActionChains(self._driver).double_click(ele).perform()
        ele.send_keys(Keys.CONTROL, 'a')
        self.step(publishing_setting_dir,"starttime")
        return self

    def endtime(self,enddate,endtime):
        '''
        計劃發佈時間
        '''
        self._params["enddate"] = enddate
        self._params["endtime"] = endtime
        ele = self.step(publishing_setting_dir, "clear_endtime")
        self.sleep(1)
        # 以下同一條數據使用一次之後失效
        # ActionChains(self._driver).double_click(ele).perform()
        ele.send_keys(Keys.CONTROL, 'a')
        self.step(publishing_setting_dir,"endtime")
        return self

    def cycle(self,cycle):
        '''
        問卷周期
        '''
        self._params["cycle"] = cycle
        get_cycle = self.step(publishing_setting_dir,"get_quarter_type")
        if get_cycle != "請選擇":
            self.step(publishing_setting_dir,"clear_cycle")
        self.step(publishing_setting_dir,"cycle")
        return self

    def click_save_draft(self):
        '''
        點擊“暂存”
        '''
        self.step(publishing_setting_dir, "click_save_draft")
        return self

    def get_save_draft_toast(self):
        return self.step(publishing_setting_dir,"get_save_draft_toast")

    def click_save(self):
        '''
        1.點擊“完成”按鈕跳轉成功頁面，
        2.點擊“返回”按鈕到列表頁
        '''
        self.sleep(1)
        self.step(publishing_setting_dir, "click_save")
        from page.quarter.quarter_management.quarter_management import Quarter_Management
        return Quarter_Management(self._driver)

    def click_save_no_pop(self):
        '''
        點擊”保存“，無二次彈框確認，獲取錯誤提示語用
        '''
        self.sleep(1)
        self.step(publishing_setting_dir, "click_save_no_pop")
        return self


    def get_endtime_error_tips(self):
        '''
        獲取問卷到期時間必填提示語
        '''
        return self.step(publishing_setting_dir, "get_endtime_error_tips")
