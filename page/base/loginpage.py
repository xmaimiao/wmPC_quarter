from common.contants import loginpage_dir
from page.base.basepage import BasePage
from page.base.index import Index


class Login(BasePage):

    def username(self,username = None):
        self._params["username"] = username
        self.step(loginpage_dir,"username")
        return self

    def password(self,password = None):
        self._params["password"] = password
        self.step(loginpage_dir, "password")
        return self

    def save(self):
        self.step(loginpage_dir, "save")
        return Index(self._driver)


