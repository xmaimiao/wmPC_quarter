import datetime
import random

import pytest
import yaml

from common.contants import basepage_dir, test_uat_bug28972_dir
from page.base.basepage import _get_working
from page.base.main import Main


def get_env():
    '''
    获取环境变量：uat、dev、mo正式站
    '''
    with open(basepage_dir, encoding="utf-8") as f:
        datas = yaml.safe_load(f)
        # 获取basepage.yaml中设置的环境变量
        wm_env = datas["default"]
        # 根据环境变量取对应的账号和密码
        user_env = datas["user"][wm_env]
        # 根据环境变量取对应的睡眠时间
        sleep_env = datas["sleeps"][wm_env]
        return user_env, sleep_env


def get_data(option):
    '''
    读取yaml文件里的测试数据
    '''
    with open(test_uat_bug28972_dir, encoding="utf-8") as f:
        datas = yaml.safe_load(f)[option]
        return datas


def get_date(type, num):
    '''
    获取修改后的时间
    '''
    now_date = datetime.datetime.now()
    if num >= 1:
        if type == "hours":
            date = str((now_date - datetime.timedelta(hours=abs(num))).strftime("%H:%M"))
        elif type == "minutes":
            date = str((now_date + datetime.timedelta(minutes=abs(num))).strftime("%H:%M"))
        else:
            date = str((now_date + datetime.timedelta(days=abs(num))).strftime("%Y/%m/%d"))
    elif num < 0:
        date = str((now_date - datetime.timedelta(hours=abs(num))).strftime("%H:%M"))
    else:
        date = str(now_date.strftime("%Y/%m/%d"))
    return date


class Test_Uat_Bug28972:
    _setup_datas = get_env()
    _working = _get_working()
    # 獲取隨機數
    _num = str(random.randint(0, 999))
    # 獲取當前日期
    _now_date = get_date("hours", 0)
    # 獲取當前時間，多加5min
    _after_five_time = get_date("minutes", 5)
    # 獲取當前時間，多加2min
    _after_two_time = get_date("minutes", 2)
    # 獲取當前時間，減少1h
    _pre_five_time = get_date("hours", -1)
    # 獲取當前日期，多加2天
    _after_two_date = get_date("days", 2)
    # 獲取當前日期，多加3天
    _after_three_date = get_date("days", 3)
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

    @pytest.mark.parametrize("data", get_data("test_stop_publishing_for_name"))
    def test_stop_publishing_for_name(self, data):
        '''
        验证通過問卷名稱停止發佈
        '''
        result = self.main.goto_quarter_management().simple_search(data["keys"]). \
            wait_sleep(1).view_quarter_for_name(data["keys"]["quarter_name"]). \
            stop_publishing().wait_sleep(1).back_to_quarter_management().simple_search(data["keys"]). \
            wait_sleep(1).get_quarter_status_for_name(data["keys"]["quarter_name"])
        assert result == data["expect"]

    @pytest.mark.parametrize("data", get_data("test_edit_endtime"))
    def test_edit_endtime(self, data):
        '''
        验证编辑到期时间，停止发布状态
        '''
        result = self.main.goto_quarter_management().simple_search(data["keys"]). \
            wait_sleep(1).edit_quarter_the_fir().click_next().click_next(). \
            endtime(data["enddate"], data["endtime"]).click_save().get_add_quarter_ele()
        assert result == True

    @pytest.mark.parametrize("data", get_data("test_copy_quarter"))
    def test_copy_quarter(self, data):
        '''
        验证複製問卷teacher_person_input(data["range_t"]).\
        '''
        result = self.main.goto_quarter_management().simple_search(data["keys"]). \
            wait_sleep(1).copy_quarter_the_fir().quarter_name(data["quarter_name"] + "學生,教職工，外部人員" + self._num). \
            click_next().click_next(). \
            starttime(self._now_date, self._after_two_time).endtime(data["enddate"], data["endtime"]). \
            cycle(data["cycle"]["cycle2"]).click_save().get_add_quarter_ele()
        assert result == True

    @pytest.mark.parametrize("data", get_data("test_stop_and_copy_edit_endtime"))
    def test_stop_and_copy_edit_endtime(self, data):
        '''
        1.停止發佈  2.且复制该问卷
        '''
        result = self.main.goto_quarter_management().simple_search(data["keys"]). \
            wait_sleep(1).view_quarter_for_name(data["keys"]["quarter_name"]). \
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
        result = self.main.goto_quarter_management().simple_search(data["keys"]). \
            wait_sleep(1).view_quarter_for_name(data["keys"]["quarter_name"]). \
            stop_publishing().wait_sleep(1).back_to_quarter_management().simple_search(data["keys"]). \
            wait_sleep(1).edit_quarter_the_fir().click_next().click_next(). \
            endtime(data["enddate"], data["endtime"]).click_save().get_add_quarter_ele()
        assert result == True

    @pytest.mark.parametrize("data", get_data("test_relseased_not_edit"))
    def test_relseased_not_edit(self, data):
        '''
        验证不修改參數直接發佈，停止发布状态
        '''
        result = self.main.goto_quarter_management().simple_search(data["keys"]). \
            wait_sleep(1).edit_quarter_the_fir().click_next().click_next(). \
            click_save().get_add_quarter_ele()
        assert result == True

    # bug29062存在多選題且為必填題目，僅選擇一個選項提交，外部人員提交會報錯
    @pytest.mark.parametrize("data", get_data("test_creat_quarter_base"))
    def test_creat_quarter_t_s_and_outsider(self, data):
        '''
        發佈範圍：學生、教師、外部人員
        '''
        # result = self.main.goto_quarter_management().create_quarter(). \
        #     quarter_name(data["quarter_name"] + "學生、教師、外部人員" + self._num).quarter_remark(data["quarter_remark"]). \
        #     add_choice_question().choice_question(data["subject_name1"], data["option_list1"]).mult_and_required(
        #     data["mult_re1"]). \
        #     add_choice_question().choice_question(data["subject_name2"], data["option_list2"]).mult_and_required(
        #     data["mult_re2"]). \
        #     add_choice_question().choice_question(data["subject_name3"], data["option_list3"]).mult_and_required(
        #     data["mult_re3"]). \
        #     add_subjective_question().subjective_question(data["subjective_name1"], data["tips1"],
        #                                                   data["words1"]).mult_and_required(data["mult_re3"]). \
        #     click_next().click_next().quarter_type(data["quarter_type"]["type1"]).teacher_all_cancel(). \
        #     click_teacher_person().teacher_person_input(data["range_t"], data["excel_path"]).click_student(). \
        #     click_student_person().student_person_input(data["range_s"]). \
        #     outsidervolist(data["outsider_path"]).administrator(data["admin"]). \
        #     starttime(self._now_date, self._after_two_time).endtime(self._now_date, self._after_five_time). \
        #     cycle(data["cycle"]["cycle2"]).click_save().get_create_ele()
        # assert result == True

        result = self.main.goto_quarter_management().create_quarter(). \
            quarter_name(data["quarter_name"] + "學生、教師、外部人員" + self._num).quarter_remark(data["quarter_remark"]). \
            add_subjective_question().subjective_question(data["subjective_name1"], data["tips1"],
                                                          data["words1"]).mult_and_required(data["mult_re3"]). \
            click_next().click_next().quarter_type(data["quarter_type"]["type1"]).teacher_all_cancel(). \
            click_teacher_person().teacher_person_input(data["range_t"], data["excel_path"]).click_student(). \
            click_student_person().student_person_input(data["range_s"]). \
            outsidervolist(data["outsider_path"]).administrator(data["admin"]). \
            starttime(self._now_date, self._after_two_time).endtime(self._now_date, self._after_five_time). \
            cycle(data["cycle"]["cycle2"]).click_save().get_create_ele()
        assert result == True

    @pytest.mark.parametrize("data", get_data("test_creat_quarter_base"))
    def test_creat_quarter_unlimited(self, data):
        '''
        创建者：deke1704
        1.不限人群
        2.admin: "deke1700,deke1703,deke1704,deke1705,gray,tao"
        '''
        result = self.main.goto_quarter_management().create_quarter(). \
            quarter_name(data["quarter_name"] + self._num + "【不限人群】").quarter_remark(
            data["quarter_remark"]). \
            add_subjective_question().subjective_question(data["subjective_name1"], data["tips1"],
                                                          data["words1"]).mult_and_required(data["mult_re1"]). \
            click_next().click_next().quarter_type(data["quarter_type"]["type2"]).administrator(data["admin"]). \
            starttime(self._now_date, self._after_two_time).endtime(self._now_date, self._after_five_time). \
            cycle(data["cycle"]["cycle2"]).click_save()
        assert result == True
