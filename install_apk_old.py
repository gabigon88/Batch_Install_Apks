import os, subprocess
from time import sleep

# 由adb指令取得連接的手機
def readDevicesList():
    p = os.popen('adb devices')
    devicesList = p.read()
    p.close()
    
    lists = devicesList.split("\n")
    devicesNames = []
    for item in lists:
        if(item.strip() == ""):
            continue
        elif(item.startswith("List of")) :
            continue
        else:
            devicesNames.append(item.split("\t")[0])
    
    return devicesNames

def install_apk(device_id, path_to_apk):
    file_name = os.path.basename(path_to_apk)
    print(f'Installing {file_name} for device: {device_id}')
    os.system(f'adb -s {device_id} push {path_to_apk} /sdcard/tmp/{file_name}')
    
    ''' 安卓8以上，因為OS安全性 直接呼叫pm install 會報錯 '''
    file_size = os.path.getsize(path_to_apk)
    commands = (
        f'cat /sdcard/tmp/{file_name} | pm install -S {file_size}\n'
        f'rm /sdcard/tmp/{file_name}\n'
    )
    procId = subprocess.Popen(f'adb -s {device_id} shell', stdin = subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    output, error = procId.communicate(commands.encode())
    print(output.decode())
    
    ''' 安卓8以下，手動把apk包push到手機上，再pm install 沒有安裝提示彈窗 '''
    # 方法一，子線程先進入adb shell 再傳入指令
    # commands = (
    #     f'pm install -r -t -d -g /sdcard/tmp/{file_name}\n'
    #     f'rm /sdcard/tmp/{file_name}\n'
    # )
    # procId = subprocess.Popen(f'adb -s {device_id} shell', stdin = subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    # output, error = procId.communicate(commands.encode())
    # print(output.decode())
    
    # 方法二，硬A 每個命令前面都加adb shell
    # os.system(f'adb -s {device_id} shell pm install /sdcard/tmp/{apk}')
    # os.system(f'adb -s {device_id} shell rm /sdcard/tmp/{apk}')
    
    # 方法三，指令串在一起給Popen()
    # commands = f'adb -s {device_id} shell "pm install /sdcard/tmp/{apk};rm /sdcard/tmp/{apk}"'
    # result = subprocess.Popen(commands, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    # output, error = result.communicate()
    # print(output.decode())

def uninstall_apk(device_id, package):
    print(f'Uninstalling apk: {package} for device: {device_id}')
    subprocess.run(f'adb -s {device_id} uninstall {package}', shell=True)
    result = str().strip().lower()

    if result == 'failure':
        print(f'WARN: Uninstall apk: {package} for device: {device_id} has error, maybe not exists.')

    if result != 'success':
        print(f'Uninstall apk: {package} for device: {device_id} failed, msg: {result}')


if __name__ == "__main__":
    devices_list = readDevicesList()

    package_list = ['com.test.v1'] # 要移除的apk package名字
    apk_path = 'C:/apk_folder' # 放apk的資料夾路徑
    apks_list = ['test.apk'] # 要安裝的apk檔名

    for device_id in devices_list:
        for package in package_list:
            uninstall_apk(device_id, package)

        for apk in apks_list:
            install_apk(device_id, f'{apk_path}/{apk}')