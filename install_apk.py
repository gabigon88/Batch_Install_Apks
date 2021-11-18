# -*- encoding=utf8 -*-
from time import sleep
from threading import Thread
from airtest.core.api import *
from airtest.cli.parser import cli_setup
from airtest.core.android import Android
from inputter import Inputter

def input_pwd():
    global brand_name, inputter

    while brand_name == '':
        sleep(1.0)
        
    inputter.set_input_type(brand_name)
    inputter.run()

def install_apk(uninstall_first: bool = False):
    global brand_name, inputter

    package_list = ['com.test.v1'] # 要移除的apk package名字
    apk_path = 'C:/apk/' # 放apk的資料夾路徑
    apks_list = ['test.apk'] # 要安裝的apk檔名

    android = Android()
    brand_name = android.shell('getprop ro.product.brand')
    
    if uninstall_first:
        for package in package_list:
            try:
                android.uninstall_app(package)
            except:
                pass
    
    for apk in apks_list:
        android.install_app(f'{apk_path}/{apk}', replace=True, install_options=['-g'])

    inputter.stop()

if not cli_setup():
    auto_setup(__file__, logdir=False)

brand_name = ''
inputter = Inputter()

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