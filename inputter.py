from time import sleep
from airtest.core.api import *
from poco.drivers.android.uiautomation import AndroidUiautomationPoco

class Inputter():
    is_complete = False

    # 各家廠牌帳號的密碼，apk安裝時帳號驗證用
    oppo_pwd = ''
    vivo_pwd = ''
    realme_pwd = ''
    xiaomi_pwd = ''

    def __init__(self):
        self.poco = AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=False)

    def color_os_input_password(self, password):
        if self.poco("com.coloros.safecenter:id/et_login_passwd_edit").exists():
            self.poco("com.coloros.safecenter:id/et_login_passwd_edit").click()
            self.poco("com.coloros.safecenter:id/et_login_passwd_edit").set_text(password)
            self.poco("android:id/button1").click()

    def origin_os_input_password(self, password):
        if self.poco("com.bbk.account:id/edit_Text").exists():
            self.poco("com.bbk.account:id/edit_Text").click()
            self.poco("com.bbk.account:id/edit_Text").set_text(password)
            self.poco("android:id/button1").click()       

    def oppo_confirm(self):
        while not self.is_complete:
            self.color_os_input_password(self.oppo_pwd)
            
            # colorOS的安裝提示窗不知道為什麼poco無法正確擷取element，只好用影像辨識
            if exists(Template(r"image/oppo_install_btn.png")):
                touch(Template(r"image/oppo_install_btn.png"))
            
            # 安全提示窗
            if self.poco("com.android.packageinstaller:id/virus_warning").exists():
                self.poco("com.android.packageinstaller:id/virus_warning").click()
            
            # 覆蓋安裝
            if self.poco(textMatches="重新安装|重新安裝").exists():
                self.poco(textMatches="重新安装|重新安裝").click()
            
            sleep(5.0)

    def vivo_confirm(self):
        while not self.is_complete:
            self.origin_os_input_password(self.vivo_pwd)
            
            # vivo 首次安裝與覆蓋安裝確認窗一樣
            if self.poco(textMatches="继续安装|繼續安裝").exists():
                self.poco(textMatches="继续安装|繼續安裝").click()

            # 安全提示窗
            if self.poco(textMatches="無視風險安裝|无视风险安装").exists():
                self.poco(textMatches="無視風險安裝|无视风险安装").click()
            
            sleep(5.0)

    def realme_confirm(self):
        while not self.is_complete:
            self.color_os_input_password(self.realme_pwd)
            
            # colorOS的安裝提示窗不知道為什麼poco無法正確擷取element，只好用影像辨識
            if exists(Template(r"image/realme_install_btn.png")):
                touch(Template(r"image/realme_install_btn.png"))
            
            # realme 覆蓋安裝時沒有確認窗

            sleep(5.0)

    def general_confirm(self):
        while not self.is_complete:
            if self.poco(text="安装|安裝").exists():
                self.poco(text="安装|安裝").click()
                
            if self.poco(textMatches="继续安装|繼續安裝").exists():
                self.poco(textMatches="继续安装|繼續安裝").click()
            
            if self.poco(textMatches="重新安装|重新安裝").exists():
                self.poco(textMatches="重新安装|重新安裝").click()

            sleep(5.0)

    def set_input_type(self, brand_name:str):
        brand = brand_name.lower().strip()
        
        if brand == 'huawei' or brand == 'honor':
            # 華為家族目前不會跳驗證窗
            self.runner = self.general_confirm

        elif brand == 'oppo':
            self.runner = self.oppo_confirm

        elif brand == 'vivo':
            self.runner = self.vivo_confirm

        elif brand == 'realme':
            self.runner = self.realme_confirm
            pass

        elif brand == 'xiaomi':
            self.runner = self.general_confirm

        else: # 如果沒有對應的品牌，使用泛用規則
            self.runner = self.general_confirm

    def run(self):
        self.runner()

    def stop(self):
        self.is_complete = True
