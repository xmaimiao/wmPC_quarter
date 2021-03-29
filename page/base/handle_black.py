from selenium.webdriver.common.by import By

def handlie_blacklist(func):
    def wrapper(*args, **kwargs):
        _blacklist = [
            (By.XPATH, '//*[@class="ivu-drawer-wrap we-drawer"]/div/div/div/div[3]/i'),
            # 登陆页面“确认”按钮
            (By.XPATH, '//*[@name="submit"]'),
            # 请假/加班弹出框的“确认”按钮
            (By.XPATH, '//*[@class="layui-layer-btn0"]'),
            # 针对HR请假弹出“已超過請假人可請假天數，是否繼續提交”捕获“是”元素
            (By.XPATH, '//*[@class="layui-layer-btn0"]')
        ]
        # “提交”表单元素
        _leave_confirm = (By.XPATH,'//*[@class="subbox"]/input[@class="submit"]')
        # 获取弹出框的文本信息
        _pop_text = (By.XPATH, '//*[@class="layui-layer-content"]')
        _max_err_num = 3
        _error_num = 0
        # 裝飾器會默認把self當第0個參數傳進來
        from page.base.basepage import BasePage
        instance : BasePage = args[0]
        try:
            result = func(*args, **kwargs)
            _error_num = 0
            # 恢復為等待3s
            instance._set_implicitly_wait(3)
            return result
        except Exception as e:
            # 等待時間過長，先處理為1s
            instance._set_implicitly_wait(1)
            # 如果没找到，就进行黑名单处理
            if _error_num > _max_err_num:
                # 如果 erro 次数大于指定指，清空 error 次数并报异常
                _error_num = 0
                raise e
            _error_num += 1
            for ele in _blacklist:
                eles = instance._finds(*ele)
                if len(eles) > 0:
                    if ele[1] in _blacklist[3][1]:
                        pop = instance._find(*_pop_text).text
                        print(f"温馨提示：{pop}")
                    eles[0].click()
                    return wrapper(*args, **kwargs)
            raise ValueError("元素不在黑名單中")
    return wrapper