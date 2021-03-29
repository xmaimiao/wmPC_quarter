import pytest
from common.contants import basepage_dir, test_login_dir

import yaml

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

# def get_data(option):
#     with open(test_login_dir, encoding="utf-8") as f:
#         datas = yaml.safe_load(f)[option]
#         return datas

class Test_Goto:

    _setup_datas = get_env()
    _working = _get_working()
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
                goto_leave(self._setup_datas[0]["application"])

        def teardown_class(self):
            '''
            非調試端口啓用
            '''
            self.main.close()

    def test_sec_goto_index(self):
        result = self.main.the_sec_goto_index(). \
            wait_sleep(1).get_imformation_ele_index()
        assert result == True

    def test_index_goto_quarter(self):
        result = self.main.goto_index().goto_application(). \
            wait_sleep(1).\
            goto_quarter(self._setup_datas[0]["application"]).\
            goto_quarter_management().get_create_ele()
        assert result == True