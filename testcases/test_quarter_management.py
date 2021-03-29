import datetime
import random

import pytest
import yaml

from common.contants import basepage_dir, test_quarter_management_dir
from page.base.basepage import _get_working
from page.base.main import Main


def get_env():
    '''
    获取环境变量：uat、dev、mo正式站
    '''
    with open(basepage_dir, encoding="utf-8") as f:
        datas = yaml.safe_load(f)
        # 获取basepage.yaml中设置的环境变量
        wm_env =  datas["default"]
        # 根据环境变量取对应的账号和密码
        user_env = datas["user"][wm_env]
        # 根据环境变量取对应的睡眠时间
        sleep_env = datas["sleeps"][wm_env]
        return user_env,sleep_env

def get_data(option):
    '''
    读取yaml文件里的测试数据
    '''
    with open(test_quarter_management_dir, encoding="utf-8") as f:
        datas = yaml.safe_load(f)[option]
        return datas

def get_date(type,num):
    '''
    获取修改后的时间
    '''
    now_date = datetime.datetime.now()
    if num >= 1:
        if type == "hours":
            date = str((now_date - datetime.timedelta(hours=abs(num))).strftime("%H:%M"))
        elif type == "minutes" :
            date = str((now_date + datetime.timedelta(minutes=abs(num))).strftime("%H:%M"))
        else:
            date = str((now_date + datetime.timedelta(days=abs(num))).strftime("%Y/%m/%d"))
    elif num < 0:
            date = str((now_date - datetime.timedelta(hours=abs(num))).strftime("%H:%M"))
    else:
        date = str(now_date.strftime("%Y/%m/%d"))
    return date


class Test_Quarter_Management:

    _setup_datas = get_env()
    _working = _get_working()
    # 獲取隨機數
    _num = str(random.randint(0,999))
    # 獲取當前日期
    _now_date = get_date("hours",0)
    # 獲取當前時間，多加5min
    _after_five_time = get_date("minutes",5)
    # 獲取當前時間，多加2min
    _after_two_time = get_date("minutes",2)
    # 獲取當前時間，減少1h
    _pre_five_time = get_date("hours",-1)
    # 獲取當前日期，多加2天
    _after_two_date = get_date("days",2)
    # 獲取當前日期，多加3天
    _after_three_date = get_date("days",3)
    if _working == "port":
        def setup(self):
            '''
            開啓調試端口啓用
            '''
            self.main = Main()
    else:
        def setup_class(self):
            '''
            非調試端口用
            '''
            self.main = Main().goto_login(). \
                username(self._setup_datas[0]["username"]).password(self._setup_datas[0]["password"]).save(). \
                goto_application(). \
                wait_sleep(1).goto_quarter(self._setup_datas[0]["application"])

        def teardown_class(self):
            '''
            非調試端口啓用
            '''
            self.main.close()

    @pytest.mark.parametrize("data", get_data("test_creat_quarter_base3"))
    def test_creat_quarter_unlimited(self, data):
        '''
        创建者：deke1704
        1.不限人群
        2.admin: "deke1700,deke1703,deke1704,deke1705,gray,tao"
        '''
        result = self.main.goto_quarter_management().create_quarter(). \
            quarter_name( data["quarter_name"] + self._num+"【不限人群】").quarter_remark(
            data["quarter_remark"]). \
            add_choice_question().choice_question(data["subject_name1"], data["option_list1"]).mult_and_required(
            data["mult_re4"]).\
            add_choice_question().choice_question(data["subject_name2"], data["option_list2"]).mult_and_required(
            data["mult_re4"]). \
            add_choice_question().choice_question(data["subject_name3"], data["option_list3"]).mult_and_required(
            data["mult_re4"]). \
            add_choice_question().choice_question(data["subject_name4"], data["option_list4"]).mult_and_required(
            data["mult_re4"]). \
            add_subjective_question().subjective_question(data["subjective_name1"], data["tips1"],
                                                          data["words1"]).mult_and_required(data["mult_re1"]). \
            click_next().click_next().quarter_type(data["quarter_type"]["type2"]).administrator(data["admin"]). \
            starttime(self._now_date, self._after_two_time).endtime(self._after_two_date, "00:00"). \
            cycle(data["cycle"]["cycle2"]).click_save()
        assert result == True

    @pytest.mark.parametrize("data", get_data("test_creat_quarter_base3"))
    def test_creat_quarter_t_s_and_outsider(self, data):
        '''
        發佈範圍：學生、教師、外部人員
        '''
        result = self.main.goto_quarter_management().create_quarter(). \
            quarter_name( data["quarter_name"]+"學生、教師、外部人員"+ self._num).quarter_remark(data["quarter_remark"]). \
            add_choice_question().choice_question(data["subject_name1"], data["option_list1"]).mult_and_required(
            data["mult_re1"]). \
            add_choice_question().choice_question(data["subject_name2"], data["option_list2"]).mult_and_required(
            data["mult_re2"]). \
            add_choice_question().choice_question(data["subject_name3"], data["option_list3"]).mult_and_required(
            data["mult_re3"]). \
            add_subjective_question().subjective_question(data["subjective_name1"], data["tips1"],
                                                          data["words1"]).mult_and_required(data["mult_re3"]). \
            click_next().click_next().quarter_type(data["quarter_type"]["type1"]).teacher_all_cancel().\
            click_teacher_person().teacher_person_input(data["range_t"],data["excel_path"]).click_student().\
            click_student_person().student_person_input(data["range_s"]).\
            outsidervolist(data["outsider_path"]).administrator(data["admin"]). \
            starttime(self._now_date, self._after_two_time).endtime(self._after_two_date, self._after_five_time). \
            cycle(data["cycle"]["cycle1"]).click_save().get_create_ele()
        assert result == True

    @pytest.mark.parametrize("data", get_data("test_creat_quarter_base3"))
    def test_creat_quarter_t_s_not_img(self, data):
        '''
        發佈範圍：學生、教師
        '''
        result = self.main.goto_quarter_management().create_quarter(). \
            quarter_name( data["quarter_name"]+"學生、教師"+ self._num).quarter_remark(data["quarter_remark"]). \
            add_choice_question().choice_question(data["subject_name1"], data["option_list1"]).mult_and_required(
            data["mult_re1"]). \
            add_choice_question().choice_question(data["subject_name2"], data["option_list2"]).mult_and_required(
            data["mult_re2"]). \
            add_subjective_question().subjective_question(data["subjective_name1"], data["tips1"],
                                                          data["words1"]).mult_and_required(data["mult_re3"]). \
            click_next().click_next().wait_sleep(1).quarter_type(data["quarter_type"]["type1"]).teacher_all_cancel().\
            click_teacher_person().teacher_person_input(data["range_t"],data["excel_path"]).wait_sleep(2).click_student().\
            click_student_person().student_person_input(data["range_s"]).\
            wait_sleep(2).administrator(data["admin"]). \
            wait_sleep(1).starttime(self._now_date, self._after_two_time).endtime(self._after_three_date, self._after_five_time). \
            cycle(data["cycle"]["cycle1"]).click_save().get_create_ele()
        assert result == True

    @pytest.mark.parametrize("data", get_data("test_creat_quarter_base3"))
    def test_creat_quarter_t_s_all_and_outsider(self, data):
        '''
        验证問卷發佈-全校師生，外部人員
        '''
        result = self.main.goto_quarter_management().create_quarter(). \
            quarter_name( data["quarter_name"] + "全部師生，外部人員" + self._num).quarter_remark(
            data["quarter_remark"]). \
            add_choice_question().choice_question(data["subject_name1"], data["option_list1"]).mult_and_required(
            data["mult_re1"]). \
            add_choice_question().choice_question(data["subject_name2"], data["option_list2"]).mult_and_required(
            data["mult_re2"]). \
            add_choice_question().choice_question(data["subject_name3"], data["option_list3"]).mult_and_required(
            data["mult_re3"]). \
            add_subjective_question().subjective_question(data["subjective_name1"], data["tips1"],
                                                          data["words1"]).mult_and_required(data["mult_re3"]). \
            click_next().click_next().quarter_type(data["quarter_type"]["type1"]). \
            click_student().click_student_all(). \
            outsidervolist(data["outsider_path"]).administrator(data["admin"]). \
            starttime(self._now_date, self._after_two_time).endtime(self._after_two_date, self._after_five_time). \
            cycle(data["cycle"]["cycle1"]).click_save().get_create_ele()
        assert result == True

    @pytest.mark.parametrize("data", get_data("test_creat_quarter_base3"))
    def test_creat_quarter_s_all_outsider(self, data):
        '''
        验证問卷發佈-學生全部，外部人員
        '''
        result = self.main.goto_quarter_management().create_quarter(). \
            quarter_name( data["quarter_name"] + "全部學生，外部人員" + self._num).quarter_remark(
            data["quarter_remark"]). \
            add_choice_question().choice_question(data["subject_name1"], data["option_list1"]).mult_and_required(
            data["mult_re1"]). \
            add_choice_question().choice_question(data["subject_name2"], data["option_list2"]).mult_and_required(
            data["mult_re2"]). \
            add_choice_question().choice_question(data["subject_name3"], data["option_list3"]).mult_and_required(
            data["mult_re3"]). \
            add_subjective_question().subjective_question(data["subjective_name1"], data["tips1"],
                                                          data["words1"]).mult_and_required(data["mult_re3"]). \
            click_next().click_next().quarter_type(data["quarter_type"]["type1"]). \
            teacher_cancel().click_student().click_student_all(). \
            outsidervolist(data["outsider_path"]).administrator(data["admin"]). \
            starttime(self._now_date, self._after_five_time).endtime(self._after_two_date, self._after_five_time). \
            cycle(data["cycle"]["cycle1"]).click_save().get_create_ele()
        assert result == True

    @pytest.mark.parametrize("data", get_data("test_creat_quarter_base3"))
    def test_creat_quarter_t_all_and_outsider(self, data):
        '''
        验证問卷發佈-教職工全部，外部人員
        '''
        result = self.main.goto_quarter_management().create_quarter(). \
            quarter_name( data["quarter_name"] + "全部教職工，外部人員" + self._num).quarter_remark(
            data["quarter_remark"]). \
            add_choice_question().choice_question(data["subject_name1"], data["option_list1"]).mult_and_required(
            data["mult_re1"]). \
            add_choice_question().choice_question(data["subject_name2"], data["option_list2"]).mult_and_required(
            data["mult_re2"]). \
            add_choice_question().choice_question(data["subject_name3"], data["option_list3"]).mult_and_required(
            data["mult_re3"]). \
            add_subjective_question().subjective_question(data["subjective_name1"], data["tips1"],
                                                          data["words1"]).mult_and_required(data["mult_re3"]). \
            click_next().click_next().quarter_type(data["quarter_type"]["type1"]). \
            outsidervolist(data["outsider_path"]).administrator(data["admin"]). \
            starttime(self._now_date, self._after_two_time).endtime(data["enddate"], self._after_five_time). \
            cycle(data["cycle"]["cycle1"]).click_save().get_create_ele()
        assert result == True

    @pytest.mark.parametrize("data", get_data("test_creat_quarter_base3"))
    def test_creat_quarter_t_group_and_outsider(self, data):
        '''
        验证問卷發佈-教職工部門：大學基金會，大學校董會 +外部人員
        '''
        result = self.main.goto_quarter_management().create_quarter(). \
            quarter_name( data["quarter_name"] + "教師部門，外部人員" + self._num).quarter_remark(
            data["quarter_remark"]). \
            add_choice_question().choice_question(data["subject_name1"], data["option_list1"]).mult_and_required(
            data["mult_re1"]). \
            add_choice_question().choice_question(data["subject_name2"], data["option_list2"]).mult_and_required(
            data["mult_re2"]). \
            add_choice_question().choice_question(data["subject_name3"], data["option_list3"]).mult_and_required(
            data["mult_re3"]). \
            add_subjective_question().subjective_question(data["subjective_name1"], data["tips1"],
                                                          data["words1"]).mult_and_required(data["mult_re3"]). \
            click_next().click_next().quarter_type(data["quarter_type"]["type1"]). \
            teacher_all_cancel().click_teacher_group(data["group_list"]).\
            outsidervolist(data["outsider_path"]).administrator(data["admin"]). \
            starttime(self._now_date, self._after_two_time).endtime(data["enddate"], self._after_five_time). \
            cycle(data["cycle"]["cycle1"]).click_save().get_create_ele()
        assert result == True

    @pytest.mark.parametrize("data", get_data("test_creat_quarter_base3"))
    def test_creat_quarter_stu_multi_cond_and_outsider(self, data):
        '''
        验证問卷發佈-學生多條件組合， +外部人員
        '''
        result = self.main.goto_quarter_management().create_quarter(). \
            quarter_name( data["quarter_name"] + "學生多條件組合，外部人員" + self._num).quarter_remark(
            data["quarter_remark"]). \
            add_choice_question().choice_question(data["subject_name1"], data["option_list1"]).mult_and_required(
            data["mult_re1"]). \
            add_subjective_question().subjective_question(data["subjective_name1"], data["tips1"],
                                                          data["words1"]).mult_and_required(data["mult_re3"]). \
            click_next().click_next().quarter_type(data["quarter_type"]["type1"]). \
            teacher_cancel().click_student().click_student_multi_cond(data["student_multi_cond"]).\
            outsidervolist(data["outsider_path"]).administrator(data["admin"]). \
            starttime(self._now_date, self._after_two_time).endtime(self._after_three_date, self._after_five_time). \
            cycle(data["cycle"]["cycle1"]).click_save().get_create_ele()
        assert result == True

    @pytest.mark.parametrize("data", get_data("test_save_success"))
    def test_save_success(self, data):
        '''
        验证只有問卷名稱保存成功
        '''
        result = self.main.goto_quarter_management().create_quarter().\
            quarter_name(data["quarter_name"]).save_draft().get_save_draft_toast()
        assert result == True
        # 刪除草稿數據
        result = self.main.goto_quarter_management().delete_quarter_the_fir()
        assert result == 1

    @pytest.mark.parametrize("data", get_data("test_save_success_for_next"))
    def test_save_success_for_next(self, data):
        '''
        验证點擊下一步保存草稿成功
        '''
        result = self.main.goto_quarter_management().create_quarter(). \
            quarter_name(data["quarter_name"]).add_choice_question().\
            choice_question(data["subject_name1"], data["option_list1"]). \
            click_next().get_save_draft_toast()
        assert result == True
        # 刪除草稿數據
        result = self.main.goto_quarter_management().delete_quarter_the_fir()
        assert result == 1

    @pytest.mark.parametrize("data", get_data("test_detele_quarter_for_name"))
    def test_detele_quarter_for_name(self, data):
        '''
        验证通過問卷名稱刪除數據
        '''
        result = self.main.goto_quarter_management().delete_quarter_for_name(data["quarter_name"])
        assert result == 1

    def test_detele_quarter_the_fir(self):
        '''
        验证刪除第一行數據
        '''
        result = self.main.goto_quarter_management().delete_quarter_the_fir()
        assert result == 1

    def test_quarter_auths_the_fir(self):
        '''
        验证第一行數據只有查看/編輯、複製權限
        前提條件：登錄其他賬號管理員
        '''
        result = self.main.goto_quarter_management().get_quarter_auths_the_fir()
        assert result == 2

    @pytest.mark.parametrize("data", get_data("test_edit_and_save"))
    def test_edit_and_save(self,data):
        '''
        驗證管理員編輯第一條數據且保存草稿成功，編輯標題
        驗證待發佈數據-》編輯-》暫存為草稿狀態
        前提：登錄管理員賬號
        '''
        quarter_name = self.main.goto_quarter_management().edit_quarter_the_fir().\
            quarter_name(data["quarter_name"]).save_draft().wait_sleep(1).back_to_mangement_list().\
            get_quarter_name_the_fir()
        quarter_status = self.main.goto_quarter_management().get_quarter_status_the_fir()
        pytest.assume( quarter_name == data["quarter_name"])
        pytest.assume( quarter_status == data["quarter_status"])

    @pytest.mark.parametrize("data", get_data("test_stop_publishing_for_name"))
    def test_stop_publishing_for_name(self, data):
        '''
        验证通過問卷名稱停止發佈
        '''
        result = self.main.goto_quarter_management().view_quarter_for_name(data["quarter_name"]).\
                stop_publishing().back_to_quarter_management().get_quarter_status_for_name(data["quarter_name"])
        assert result == data["expect"]

    @pytest.mark.parametrize("data", get_data("test_stop_publishing_for_name"))
    def test_stop_publishing_for_name(self, data):
        '''
        验证通過問卷名稱停止發佈
        '''
        result = self.main.goto_quarter_management().simple_search(data["keys"]).\
                wait_sleep(1).view_quarter_for_name(data["keys"]["quarter_name"]).\
                stop_publishing().wait_sleep(1).back_to_quarter_management().simple_search(data["keys"]).\
                wait_sleep(1).get_quarter_status_for_name(data["keys"]["quarter_name"])
        assert result == data["expect"]

    @pytest.mark.parametrize("data", get_data("test_get_publish_setting_for_name"))
    def test_get_publish_setting_for_name(self, data):
        '''
        验证通過問卷名稱獲取發佈設置信息
        '''
        result = self.main.goto_quarter_management().simple_search(data["keys"]).\
                wait_sleep(1).view_quarter_for_name(data["keys"]["quarter_name"]).\
                wait_sleep(1).get_publish_setting_information(data["keys"]["quarter_name"]).back_to_quarter_management().\
            get_add_quarter_ele()
        assert result == True

    @pytest.mark.parametrize("data", get_data("test_simple_search"))
    def test_simple_search(self, data):
        '''
        验证简易查询
        '''
        result = self.main.goto_quarter_management().simple_search(data["keys"]).\
                wait_sleep(1).get_quarter_name_the_fir()
        assert data["keys"]["quarter_name"] in result

    @pytest.mark.parametrize("data", get_data("test_simple_search"))
    def test_simple_search_mq(self, data):
        '''
        验证简易查询-我的問卷
        '''
        result = self.main.goto_my_quarter().simple_search(data["keys"]).\
                wait_sleep(1).get_quarter_name_the_fir()
        assert data["keys"]["quarter_name"] in result

    @pytest.mark.parametrize("data", get_data("test_simple_search"))
    def test_simple_search_qs(self, data):
        '''
        验证简易查询-問卷統計
        '''
        result = self.main.goto_quarter_statistics().simple_search(data["keys"]).\
                wait_sleep(1).get_quarter_name_the_fir()
        assert data["keys"]["quarter_name"] in result

    @pytest.mark.parametrize("data", get_data("test_advanced_search"))
    def test_advanced_search(self, data):
        '''
        验证高級查詢
        '''
        result = self.main.goto_quarter_management().advanced_search(data["keys"]).\
                wait_sleep(1).get_quarter_status_the_fir()
        # assert data["keys"]["status"]["value"] == result

    @pytest.mark.parametrize("data", get_data("test_edit_endtime"))
    def test_edit_endtime(self, data):
        '''
        验证编辑到期时间，停止发布状态
        '''
        result = self.main.goto_quarter_management().simple_search(data["keys"]).\
                wait_sleep(1).edit_quarter_the_fir().click_next().click_next(). \
                endtime(data["enddate"], data["endtime"]).click_save().get_add_quarter_ele()
        assert result == True

    @pytest.mark.parametrize("data", get_data("test_relseased_not_edit"))
    def test_relseased_not_edit(self, data):
        '''
        验证不修改參數直接發佈，停止发布状态
        '''
        result = self.main.goto_quarter_management().simple_search(data["keys"]).\
                wait_sleep(1).edit_quarter_the_fir().click_next().click_next(). \
                click_save().get_add_quarter_ele()
        assert result == True

    @pytest.mark.parametrize("data", get_data("test_edit_publish_setting"))
    def test_edit_publish_setting(self, data):
        '''
        验证编辑發佈設置
        '''
        result = self.main.goto_quarter_management().simple_search(data["keys"]).\
                wait_sleep(1).edit_quarter_the_fir().click_next().click_next(). \
                quarter_type(data["quarter_type"]["type1"]).teacher_cancel().\
                click_student().click_student_multi_cond(data["student_multi_cond"]). \
                administrator(data["admin"]). \
                starttime(self._now_date, self._after_two_time).endtime(self._after_three_date, self._after_five_time). \
                cycle(data["cycle"]["cycle1"]).click_save().get_create_ele()
        assert result == True


    @pytest.mark.parametrize("data", get_data("test_copy_quarter"))
    def test_copy_quarter(self, data):
        '''
        验证複製問卷teacher_person_input(data["range_t"]).\  student_person_input(data["range_s"]). \
        '''
        result = self.main.goto_quarter_management().simple_search(data["keys"]).\
            wait_sleep(1).copy_quarter_the_fir().quarter_name(data["quarter_name"] + "學生,教職工，外部人員" + self._num).\
            click_next().click_next(). \
            starttime(self._now_date, self._after_two_time).endtime(self._after_two_date, data["endtime"]).\
            cycle(data["cycle"]["cycle2"]).click_save().wait_sleep(1).get_add_quarter_ele()
        assert result == True

    @pytest.mark.parametrize("data", get_data("test_stop_and_copy_edit_endtime"))
    def test_stop_and_copy_edit_endtime(self, data):
        '''
        1.停止發佈  2.且复制该问卷
        '''
        result = self.main.goto_quarter_management().simple_search(data["keys"]).\
            wait_sleep(1).view_quarter_for_name(data["keys"]["quarter_name"]).\
            stop_publishing().wait_sleep(1).back_to_quarter_management().simple_search(data["keys"]). \
            wait_sleep(1).copy_quarter_the_fir().quarter_name(
            data["quarter_name"] + "學生,教職工，外部人員" + self._num).click_next().click_next(). \
            starttime(self._now_date, self._after_two_time).endtime(data["enddate"], data["endtime"]). \
            cycle(data["cycle"]["cycle2"]).click_save().get_add_quarter_ele()
        assert result == True

    @pytest.mark.parametrize("data", get_data("test_stop_and_edit_endtime"))
    def test_stop_and_edit_endtime(self, data):
        '''
        1.停止發佈  2.且编辑该问卷结束时间
        '''
        result = self.main.goto_quarter_management().simple_search(data["keys"]).\
            wait_sleep(1).view_quarter_for_name(data["keys"]["quarter_name"]).\
            stop_publishing().wait_sleep(1).back_to_quarter_management().simple_search(data["keys"]). \
            wait_sleep(1).edit_quarter_the_fir().click_next().click_next().\
            endtime(data["enddate"], data["endtime"]).click_save().get_add_quarter_ele()
        assert result == True







