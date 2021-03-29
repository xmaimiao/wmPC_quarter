import pytest
import yaml

from common.contants import basepage_dir,test_quarter_statistic_dir
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
    with open(test_quarter_statistic_dir, encoding="utf-8") as f:
        datas = yaml.safe_load(f)[option]
        return datas


class Test_Quarter_Statistic:

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

    @pytest.mark.parametrize("data", get_data("test_get_releasedrange"))
    def test_get_releasedrange(self, data):
        '''
        獲取發佈範圍詳情
        '''
        result = self.main.goto_quarter_statistics().wait_sleep(1).simple_search(data["keys"]).\
            wait_sleep(1).view_the_fir(data["keys"]["quarter_name"]).\
            view_releasedrange().releasedrange_detail()
        assert result == True

    @pytest.mark.parametrize("data", get_data("test_advanced_search"))
    def test_advanced_search(self, data):
        '''
        验证高級查詢,狀態已結束、回收數量>1的數據，有“統計”按鈕
        '''
        result = self.main.goto_quarter_statistics().advanced_search(data["keys"]).\
                wait_sleep(1).get_quarter_status_the_fir()
        assert result == "已結束"