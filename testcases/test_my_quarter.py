import pytest
import yaml

from common.contants import basepage_dir, test_my_quarter_dir
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
    with open(test_my_quarter_dir, encoding="utf-8") as f:
        datas = yaml.safe_load(f)[option]
        return datas


class Test_My_Quarter:

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

    @pytest.mark.parametrize("data", get_data("test_reply_quarter"))
    def test_reply_quarter(self, data):
        '''
        驗證回復問卷 停止發佈測試/測試可見範圍-學生教師/測試到期不可填寫-學生教師/問卷統計測試
        '''
        result = self.main.goto_my_quarter().view_quarter_for_name(data["quarter_name"]).\
            question(data["subject"]).click_save().get_save_toast()
        assert result == True

    @pytest.mark.parametrize("data", get_data("test_simple_search"))
    def test_simple_search(self, data):
        '''
        验证简易查询
        '''
        result = self.main.goto_my_quarter().simple_search(data["keys"]).\
                wait_sleep(1).get_quarter_name_the_fir()
        assert data["keys"]["quarter_name"] in result




