import datetime
import random

import pytest
import yaml

from common.contants import basepage_dir, test_uat_fir_dir
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
    with open(test_uat_fir_dir, encoding="utf-8") as f:
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


class Test_Uat_Fir:

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
    _pre_one_hour = get_date("hours",-1)
    # 獲取當前時間，多加1h
    _after_one_hour = get_date("hours",1)
    # 獲取當前日期，多加1天
    _after_one_date = get_date("days",1)
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
                goto_quarter(self._setup_datas[0]["application"])

        def teardown_class(self):
            '''
            非調試端口啓用
            '''
            self.main.close()

    # 驗證暫存
    @pytest.mark.parametrize("data", get_data("test_save_success"))
    def test_save_success(self, data):
        '''
        验证只有問卷名稱保存成功
        '''
        result = self.main.goto_quarter_management().create_quarter().\
            quarter_name(data["quarter_name"]).save_draft().get_save_draft_toast()
        assert result == True
        # 刪除草稿數據
        # result = self.main.goto_quarter_management().delete_quarter_the_fir()
        # assert result == 0

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
        assert result == 0

    def test_quarter_auths_the_fir(self):
        '''
        验证第一行數據只有查看/編輯、複製權限
        前提條件：登錄其他賬號管理員
        '''
        result = self.main.goto_quarter_management().get_quarter_auths_the_fir()
        assert result == 2

    @pytest.mark.parametrize("data", get_data("test_creat_quarter_base"))
    def test_publish_setting_save(self,data):
        '''
        验证创建问卷，发布设置填写完后保存
        '''
        result = self.main.goto_quarter_management().create_quarter(). \
            quarter_name(str(self._now_date) + data["quarter_name"] + "全部師生，外部人員" + self._num).quarter_remark(
            data["quarter_remark"]). \
            add_subjective_question().subjective_question(data["subjective_name1"], data["tips1"],
                                                          data["words1"]).mult_and_required(data["mult_re3"]). \
            click_next().click_next().quarter_type(data["quarter_type"]["type1"]). \
            click_student().click_student_all().administrator(data["admin"]). \
            starttime(self._now_date, self._after_two_time).endtime(self._after_three_date, self._after_five_time). \
            cycle(data["cycle"]["cycle1"]).click_save().get_create_ele()
        assert result == True

    def test_edit_and_save(self):
        '''
        驗證管理員編輯且保存草稿成功，編輯標題
        '''

    # 發送範圍測試
    @pytest.mark.parametrize("data", get_data("test_creat_quarter_base"))
    def test_creat_quarter_for_all_ts_and_outsiders(self, data):
        '''
        验证問卷發佈-全校師生，外部人員
        '''
        result = self.main.goto_quarter_management().create_quarter(). \
            quarter_name(str(self._now_date) + data["quarter_name"] + "全部師生，外部人員"+ self._num).quarter_remark(
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
            starttime(self._now_date, self._after_two_time).endtime(self._after_three_date, self._after_five_time). \
            cycle(data["cycle"]["cycle1"]).click_save().get_create_ele()
        assert result == True

    @pytest.mark.parametrize("data", get_data("test_creat_quarter_base"))
    def test_creat_quarter_t_s(self, data):
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

    @pytest.mark.parametrize("data", get_data("test_creat_quarter_base"))
    def test_creat_quarter_s_all_outsider(self, data):
        '''
        验证問卷發佈-學生全部，外部人員
        '''
        result = self.main.goto_quarter_management().create_quarter(). \
            quarter_name(str(self._now_date) + data["quarter_name"] + "全部學生，外部人員" + self._num).quarter_remark(
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
            starttime(self._now_date, self._after_two_time).endtime(self._after_three_date, self._after_five_time). \
            cycle(data["cycle"]["cycle1"]).click_save().get_create_ele()
        assert result == True

    @pytest.mark.parametrize("data", get_data("test_creat_quarter_base"))
    def test_creat_quarter_t_all_and_outsider(self, data):
        '''
        验证問卷發佈-教職工全部，外部人員
        '''
        result = self.main.goto_quarter_management().create_quarter(). \
            quarter_name(str(self._now_date) + data["quarter_name"] + "全部教職工，外部人員" + self._num).quarter_remark(
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
            starttime(self._now_date, self._after_two_time).endtime(self._after_three_date, self._after_five_time). \
            cycle(data["cycle"]["cycle1"]).click_save().get_create_ele()
        assert result == True

    @pytest.mark.parametrize("data", get_data("test_creat_quarter_base"))
    def test_creat_quarter_t_group_and_outsider(self, data):
        '''
        验证問卷發佈-教職工部門、 +外部人員
        '''
        result = self.main.goto_quarter_management().create_quarter(). \
            quarter_name(str(self._now_date) + data["quarter_name"] + "教師部門，外部人員" + self._num).quarter_remark(
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
            starttime(self._now_date, self._after_two_time).endtime(self._after_three_date, self._after_five_time). \
            cycle(data["cycle"]["cycle1"]).click_save().get_create_ele()
        assert result == True

    @pytest.mark.parametrize("data", get_data("test_creat_quarter_base"))
    def test_creat_quarter_stu_multi_cond_and_outsider(self, data):
        '''
        验证問卷發佈-學生多條件組合， +外部人員
        '''
        result = self.main.goto_quarter_management().create_quarter(). \
            quarter_name(str(self._now_date) + data["quarter_name"] + "學生多條件組合，外部人員" + self._num).quarter_remark(
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

    @pytest.mark.parametrize("data", get_data("test_creat_quarter_base"))
    def test_creat_quarter_unlimited(self, data):
        '''
        创建者：deke1704
        1.不限人群
        '''
        result = self.main.goto_quarter_management().create_quarter(). \
            quarter_name(str(self._now_date) + data["quarter_name"] + self._num+"【不限人群】").quarter_remark(
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

    # 檢查周期發佈問卷
    @pytest.mark.parametrize("data", get_data("test_creat_quarter_base"))
    def test_creat_quarter_unlimited_tomorrow_end(self, data):
        '''
        1.不限人群
        '''
        result = self.main.goto_quarter_management().create_quarter(). \
            quarter_name(str(self._now_date) + data["quarter_name"] + self._num+"【不限人群】,周期發佈隔天結束").quarter_remark(
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
            starttime(self._now_date, self._after_two_time).endtime(self._after_one_date, self._after_two_time). \
            cycle(data["cycle"]["cycle1"]).click_save()
        assert result == True

    @pytest.mark.parametrize("data", get_data("test_creat_quarter_base"))
    def test_creat_quarter_unlimited_00(self, data):
        '''
        1.不限人群,3天后結束問卷00：00
        '''
        result = self.main.goto_quarter_management().create_quarter(). \
            quarter_name(str(self._now_date) + data["quarter_name"] + self._num+"【不限人群】,結束問卷00：00").quarter_remark(
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
            starttime(self._now_date, self._after_two_time).endtime(self._after_three_date, "00:00"). \
            cycle(data["cycle"]["cycle1"]).click_save()
        assert result == True

    @pytest.mark.parametrize("data", get_data("test_creat_quarter_base"))
    def test_creat_quarter_t_s_and_outsider2(self, data):
        '''
        發佈範圍：學生、教師、外部人員,時間點>發佈時間點
        '''
        result = self.main.goto_quarter_management().create_quarter(). \
            quarter_name(str(self._now_date) + data["quarter_name"] + "學生、教師、外部人員,時間點>發佈時間點" + self._num).quarter_remark(
            data["quarter_remark"]). \
            add_choice_question().choice_question(data["subject_name1"], data["option_list1"]).mult_and_required(
            data["mult_re1"]). \
            add_choice_question().choice_question(data["subject_name2"], data["option_list2"]).mult_and_required(
            data["mult_re2"]). \
            add_choice_question().choice_question(data["subject_name3"], data["option_list3"]).mult_and_required(
            data["mult_re3"]). \
            add_subjective_question().subjective_question(data["subjective_name1"], data["tips1"],
                                                          data["words1"]).mult_and_required(data["mult_re3"]). \
            click_next().click_next().quarter_type(data["quarter_type"]["type1"]).teacher_all_cancel(). \
            click_teacher_person(data["range_t"], data["excel_path"]).click_student().wait_sleep(1).click_student_person(
            data["range_s"]). \
            outsidervolist(data["outsider_path"]).administrator(data["admin"]). \
            starttime(self._now_date, self._after_two_time).endtime(self._after_three_date, self._after_one_hour). \
            cycle(data["cycle"]["cycle1"]).click_save().get_create_ele()
        assert result == True

    @pytest.mark.parametrize("data", get_data("test_creat_quarter_base"))
    def test_creat_quarter_t_s_and_outsider3(self, data):
        '''
        發佈範圍：學生、教師、外部人員,時間點<發佈時間點
        '''
        result = self.main.goto_quarter_management().create_quarter(). \
            quarter_name(str(self._now_date) + data["quarter_name"] + "學生、教師、外部人員,時間點<發佈時間點" + self._num).quarter_remark(
            data["quarter_remark"]). \
            add_choice_question().choice_question(data["subject_name1"], data["option_list1"]).mult_and_required(
            data["mult_re1"]). \
            add_choice_question().choice_question(data["subject_name2"], data["option_list2"]).mult_and_required(
            data["mult_re2"]). \
            add_choice_question().choice_question(data["subject_name3"], data["option_list3"]).mult_and_required(
            data["mult_re3"]). \
            add_subjective_question().subjective_question(data["subjective_name1"], data["tips1"],
                                                          data["words1"]).mult_and_required(data["mult_re3"]). \
            click_next().click_next().quarter_type(data["quarter_type"]["type1"]).teacher_all_cancel(). \
            click_teacher_person(data["range_t"], data["excel_path"]).click_student().wait_sleep(1).click_student_person(
            data["range_s"]). \
            outsidervolist(data["outsider_path"]).administrator(data["admin"]). \
            starttime(self._now_date, self._after_two_time).endtime(self._after_three_date, self._pre_one_hour). \
            cycle(data["cycle"]["cycle1"]).click_save().get_create_ele()
        assert result == True

    # 檢查僅一次發佈問卷，全部非必填題目，均不填提交
    @pytest.mark.parametrize("data", get_data("test_creat_quarter_base"))
    def test_creat_quarter_t_s_and_outsider4(self, data):
        '''
        發佈範圍：學生、教師、外部人員,全部非必選題目，隔天失效
        '''
        result = self.main.goto_quarter_management().create_quarter(). \
            quarter_name(str(self._now_date) + data["quarter_name"] + "學生、教師、外部人員,全部非必選題目,隔天失效" + self._num).quarter_remark(
            data["quarter_remark"]). \
            add_choice_question().choice_question(data["subject_name1"], data["option_list1"]).mult_and_required(
            data["mult_re2"]). \
            add_choice_question().choice_question(data["subject_name2"], data["option_list2"]).mult_and_required(
            data["mult_re3"]). \
            add_choice_question().choice_question(data["subject_name3"], data["option_list3"]).mult_and_required(
            data["mult_re3"]). \
            add_subjective_question().subjective_question(data["subjective_name1"], data["tips1"],
                                                          data["words1"]).mult_and_required(data["mult_re3"]). \
            click_next().click_next().quarter_type(data["quarter_type"]["type1"]).teacher_all_cancel(). \
            click_teacher_person(data["range_t"], data["excel_path"]).click_student().wait_sleep(1).click_student_person(
            data["range_s"]). \
            outsidervolist(data["outsider_path"]).administrator(data["admin"]). \
            starttime(self._now_date, self._after_two_time).endtime(self._after_one_date, self._pre_one_hour). \
            cycle(data["cycle"]["cycle1"]).click_save().get_create_ele()
        assert result == True

    # 檢查僅一次發佈問卷，全部必填題目，單選+主觀
    @pytest.mark.parametrize("data", get_data("test_creat_quarter_base"))
    def test_creat_quarter_t_s_and_outsider5(self, data):
        '''
        發佈範圍：學生、教師、外部人員,全部非必選題目，隔天失效
        '''
        result = self.main.goto_quarter_management().create_quarter(). \
            quarter_name(str(self._now_date) + data["quarter_name"] + "學生、教師、外部人員,全部必填題目，單選+主觀,隔天00：00失效" + self._num).quarter_remark(
            data["quarter_remark"]). \
            add_choice_question().choice_question(data["subject_name1"], data["option_list1"]).mult_and_required(
            data["mult_re4"]). \
            add_choice_question().choice_question(data["subject_name2"], data["option_list2"]).mult_and_required(
            data["mult_re4"]). \
            add_choice_question().choice_question(data["subject_name3"], data["option_list3"]).mult_and_required(
            data["mult_re4"]). \
            add_subjective_question().subjective_question(data["subjective_name1"], data["tips1"],
                                                          data["words1"]).mult_and_required(data["mult_re4"]). \
            click_next().click_next().quarter_type(data["quarter_type"]["type1"]).teacher_all_cancel(). \
            click_teacher_person(data["range_t"], data["excel_path"]).click_student().wait_sleep(1).click_student_person(
            data["range_s"]). \
            outsidervolist(data["outsider_path"]).administrator(data["admin"]). \
            starttime(self._now_date, self._after_two_time).endtime(self._after_one_date, "00:00"). \
            cycle(data["cycle"]["cycle1"]).click_save().get_create_ele()
        assert result == True

    # 檢查僅一次發佈問卷，存在單選題非必填，不填提交（其他題已填）
    @pytest.mark.parametrize("data", get_data("test_creat_quarter_base"))
    def test_creat_quarter_t_s_and_outsider6(self, data):
        '''
        發佈範圍：學生、教師、外部人員,全部非必選題目
        '''
        result = self.main.goto_quarter_management().create_quarter(). \
            quarter_name(str(self._now_date) + data["quarter_name"] + "學生、教師、外部人員,存在單選題非必填" + self._num).quarter_remark(
            data["quarter_remark"]). \
            add_choice_question().choice_question(data["subject_name1"], data["option_list1"]).mult_and_required(
            data["mult_re3"]). \
            add_choice_question().choice_question(data["subject_name2"], data["option_list2"]).mult_and_required(
            data["mult_re3"]). \
            add_choice_question().choice_question(data["subject_name3"], data["option_list3"]).mult_and_required(
            data["mult_re3"]). \
            add_subjective_question().subjective_question(data["subjective_name1"], data["tips1"],
                                                          data["words1"]).mult_and_required(data["mult_re4"]). \
            click_next().click_next().quarter_type(data["quarter_type"]["type1"]).teacher_all_cancel(). \
            click_teacher_person(data["range_t"], data["excel_path"]).click_student().wait_sleep(1).click_student_person(
            data["range_s"]). \
            outsidervolist(data["outsider_path"]).administrator(data["admin"]). \
            starttime(self._now_date, self._after_two_time).endtime(self._after_one_date, self._after_three_date). \
            cycle(data["cycle"]["cycle1"]).click_save().get_create_ele()
        assert result == True

    # 檢查僅一次發佈問卷，存在多選題非必填，不填提交（其他題已填）
    @pytest.mark.parametrize("data", get_data("test_creat_quarter_base"))
    def test_creat_quarter_t_s_and_outsider7(self, data):
        '''
        發佈範圍：學生、教師、外部人員,全部非必選題目
        '''
        result = self.main.goto_quarter_management().create_quarter(). \
            quarter_name(str(self._now_date) + data["quarter_name"] + "學生、教師、外部人員,存在多選題非必填" + self._num).quarter_remark(
            data["quarter_remark"]). \
            add_choice_question().choice_question(data["subject_name1"], data["option_list1"]).mult_and_required(
            data["mult_re2"]). \
            add_choice_question().choice_question(data["subject_name2"], data["option_list2"]).mult_and_required(
            data["mult_re2"]). \
            add_choice_question().choice_question(data["subject_name3"], data["option_list3"]).mult_and_required(
            data["mult_re2"]). \
            add_subjective_question().subjective_question(data["subjective_name1"], data["tips1"],
                                                          data["words1"]).mult_and_required(data["mult_re4"]). \
            click_next().click_next().quarter_type(data["quarter_type"]["type1"]).teacher_all_cancel(). \
            click_teacher_person(data["range_t"], data["excel_path"]).click_student().wait_sleep(1).click_student_person(
            data["range_s"]). \
            outsidervolist(data["outsider_path"]).administrator(data["admin"]). \
            starttime(self._now_date, self._after_two_time).endtime(self._after_one_date, self._after_three_date). \
            cycle(data["cycle"]["cycle1"]).click_save().get_create_ele()
        assert result == True

    # 檢查僅一次發佈問卷，存在主觀題非必填，不填提交（其他題已填）
    @pytest.mark.parametrize("data", get_data("test_creat_quarter_base"))
    def test_creat_quarter_t_s_and_outsider8(self, data):
        '''
        發佈範圍：學生、教師、外部人員,全部非必選題目
        '''
        result = self.main.goto_quarter_management().create_quarter(). \
            quarter_name(str(self._now_date) + data["quarter_name"] + "學生、教師、外部人員,存在主觀題非必填" + self._num).quarter_remark(
            data["quarter_remark"]). \
            add_choice_question().choice_question(data["subject_name1"], data["option_list1"]).mult_and_required(
            data["mult_re2"]). \
            add_choice_question().choice_question(data["subject_name2"], data["option_list2"]).mult_and_required(
            data["mult_re2"]). \
            add_choice_question().choice_question(data["subject_name3"], data["option_list3"]).mult_and_required(
            data["mult_re2"]). \
            add_subjective_question().subjective_question(data["subjective_name1"], data["tips1"],
                                                          data["words1"]).mult_and_required(data["mult_re3"]). \
            click_next().click_next().quarter_type(data["quarter_type"]["type1"]).teacher_all_cancel(). \
            click_teacher_person(data["range_t"], data["excel_path"]).click_student().wait_sleep(1).click_student_person(
            data["range_s"]). \
            outsidervolist(data["outsider_path"]).administrator(data["admin"]). \
            starttime(self._now_date, self._after_two_time).endtime(self._after_one_date, self._after_three_date). \
            cycle(data["cycle"]["cycle1"]).click_save().get_create_ele()
        assert result == True

    # bug28692 檢查教職員-學生為全部發佈設置顯示正確
    @pytest.mark.parametrize("data", get_data("test_get_publish_setting_for_name"))
    def test_get_publish_setting_for_name(self, data):
        '''
        验证通過問卷名稱獲取發佈設置信息
        '''
        result = self.main.goto_quarter_management().view_quarter_for_name(data["quarter_name"]).\
                get_publish_setting_information(data["quarter_name"]).back_to_quarter_management().\
            get_add_quarter_ele()
        assert result == True

    # bug28670 驗證創建問卷到期時間不能小於當天日期
    @pytest.mark.parametrize("data", get_data("test_creat_quarter_base"))
    def test_get_endtime_error_tips(self, data):
        '''
        验证通過問卷名稱獲取發佈設置信息
        '''
        result = self.main.goto_quarter_management().create_quarter(). \
            quarter_name(str(self._now_date) + data["quarter_name"] + self._num).quarter_remark(
            data["quarter_remark"]). \
            add_choice_question().choice_question(data["subject_name2"], data["option_list2"]).mult_and_required(
            data["mult_re1"]).click_next().click_next().quarter_type(data["quarter_type"]["type1"]). \
            click_student().click_student_all().administrator(data["admin"]). \
            starttime(self._now_date, self._after_five_time).endtime(self._now_date, self._after_five_time). \
            click_save_no_pop().get_endtime_error_tips()
        assert result == "問卷到期時間不能小於當前日期"

    @pytest.mark.parametrize("data", get_data("test_edit_publish_setting"))
    def test_edit_publish_setting_stu_multi_cond(self, data):
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

    @pytest.mark.parametrize("data", get_data("test_edit_publish_setting"))
    def test_edit_publish_setting_t_group(self, data):
        '''
        验证编辑發佈設置
        '''
        result = self.main.goto_quarter_management().simple_search(data["keys"]).\
                wait_sleep(1).edit_quarter_the_fir().click_next().click_next(). \
                quarter_type(data["quarter_type"]["type1"]).teacher_all_cancel().\
                click_teacher_group(data["group_list"]). \
                administrator(data["admin"]). \
                starttime(self._now_date, self._after_two_time).endtime(self._after_three_date, self._after_five_time). \
                cycle(data["cycle"]["cycle1"]).click_save().get_create_ele()
        assert result == True