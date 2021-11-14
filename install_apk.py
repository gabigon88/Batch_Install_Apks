# -*- encoding=utf8 -*-

import os, subprocess
from time import sleep
from threading import Thread
from airtest.core.api import *
from airtest.cli.parser import cli_setup
from airtest.core.android import Android

if not cli_setup():
    auto_setup(__file__, logdir=False)

from poco.drivers.android.uiautomation import AndroidUiautomationPoco
poco = AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=False)


is_complete = False

def vivo_input():
    global is_complete
    vivo_pwd = '' # vivo帳號的密碼，apk安裝時帳號驗證用
    while not is_complete:
        if poco("com.coloros.safecenter:id/et_login_passwd_edit").exists():
            poco("com.coloros.safecenter:id/et_login_passwd_edit").click()
            poco("com.coloros.safecenter:id/et_login_passwd_edit").set_text(vivo_pwd)
            poco("android:id/button1").click()
                            
        if poco(text="安装|安裝").exists():
            poco(text="安装|安裝").click()

        if poco("com.android.packageinstaller:id/virus_warning").exists():
            poco("com.android.packageinstaller:id/virus_warning").click()
            
        if poco(textMatches="重新安装|重新安裝").exists():
            poco(textMatches="重新安装|重新安裝").click()
        
        sleep(5.0)

def huawei_input():
    global is_complete
    oppo_pwd = '' # oppo帳號的密碼，apk安裝時帳號驗證用
    while not is_complete:
        if poco(text="安装|安裝").exists():
            poco(text="安装|安裝").click()
            
        if poco(textMatches="继续安装|繼續安裝").exists():
            poco(textMatches="继续安装|繼續安裝").click()
        
        sleep(5.0)

def install_apk(uninstall_first: bool = False):
    global is_complete

    package_list = ['com.test.v1'] # 要移除的apk package名字
    apk_path = 'C:/apk_folder' # 放apk的資料夾路徑
    apks_list = ['test.apk'] # 要安裝的apk檔名

    android = Android()

    if uninstall_first:
        for package in package_list:
            try:
                android.uninstall_app(package)
            except:
                pass
    
    for apk in apks_list:
        android.install_app(f'{apk_path}/{apk}', replace=True, install_options=['-g'])
        
    is_complete = True

input_pwd = huawei_input

# 新建用於等待彈窗輸入帳號密碼的執行緒
thread1 = Thread(target=input_pwd)
thread2 = Thread(target=install_apk, args=(False,))

# 啟動兩個執行緒
thread1.start()
thread2.start()

# 設定執行緒阻塞
thread1.join()
thread2.join()

print('end')