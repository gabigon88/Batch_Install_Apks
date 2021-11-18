# Batch_Install_Apks
用Airtest手機自動化框架，批次安裝apk

## 說明
做測試的大家應該多少都有遇過需要批次安裝apk的情況  
例如: 公司產品app大更版，不能熱更要重裝，但測試機有十幾二十支  
所以其實一直都有打算寫一支tool方便做這件事  

本篇使用的手機自動化框架不是大家熟悉的Appium，而是Airtest  
關於Airtest，它是由網易游戲自行研發的一款手機自動化框架  
官網(https://airtest.netease.com/)  
我記得當初查資料好像他們公司內部也是用這款做測試的樣子  
與Appium相比，最大的差異就是Airtest有集成影像辨識功能  
所以腳本上可以做到 文字定位 + 影像辨識 的超級組合技，基本上是無敵了  
自己也用了一段時間了，使用上也相當人性化，偶爾有會用這款快速開發來刷手遊XD  

回歸正題，本code的解決邏輯是，建立兩個線程  
一個負責批次安裝apk (因為安裝還沒結束前，該行code算還沒結束，所以要用雙線程)  
一個負責判斷畫面是否有確認彈窗，有就點擊確認  

## 使用
(2021-11-12記) 但airtest目前的套件poco，1.0.0.43版有bug  
有機會明明畫面上文字有定位到，但執行的時候就會跳element沒抓到，不知道什麼時候才會修正  

官方有說 如果不用官方IDE執行腳本，而是用python直接run的話  
python環境要安裝以下兩個套件airtest、pocoui  
```python
  pip install airtest==1.2.0
  pip install pocoui
```
註記: airtest指定1.2.0版是因為上面寫的element定位bug  

## 後記
這個Repo其實是個long story (淚)  
原本以為這用adb會很簡單，因為沒學過adb shell 所以先學了如何用  
學完後發現adb是command line指令，再去查如何用python執行command line  
最後萬萬沒想到在Android 8 以後的版本安全度越來越高了  
單純執行adb install，很多手機上都會跳出確認安裝的視窗  
你不點確認 它就卡在那不裝(嘿!這樣一點都批次)  

原先還查到資料，以為用別種方式可以繞過確認裝  
結果自己把完整的程式碼刻出來後，發現執行還是一樣不行  
回頭檢查文章日期，才突然發現也是非常久以前的文章  
文章用的安卓版本 八成也是很舊的 (吐血...)  

在嘗試了各種花式adb安裝指令後，最後還是只能乖乖繞回  
一邊自動安裝app，一邊靠現有手機自動化框架，自動點擊允許安裝  

參考文件:  
[常用 adb 指令及實用小技巧](https://ithelp.ithome.com.tw/articles/10241811)  
[常用adb 和 adb shell 命令](https://www.itread01.com/content/1548785710.html)  
[ADB Shell 指令大全](https://adbshell.com/commands/adb-install)  

[python執行cmd命令](https://www.jianshu.com/p/d732fa4217d9)  
[python執行多行adb shell命令](https://www.cnblogs.com/wztshine/p/13445520.html)  

↓確認新版安卓不可行↓  
[手動把包 push 到手機上，再pm install，沒有彈窗](https://testerhome.com/topics/2601)  
[apk静默安装遇到坑的解决](https://www.jianshu.com/p/ee4cd3183b0e)  
[Android P使用pm install安装apk报错](https://blog.csdn.net/xuebijun/article/details/82852414)  

↓乖乖用自動化框架點擊確認窗↓  
[如何解决“自动装包”过程中oppo、vivo等手机需要输入密码的问题](https://blog.csdn.net/AirtestProject/article/details/109623566)  
[MIUI確認彈窗](https://github.com/AirtestProject/AirtestIDE/issues/85)  