#  从焊接到刷固件打造micropython最小系统

## 效果图：





## **打造步骤：**

#####    **材料：                            成本：**

​      **电烙铁加焊锡               （10元）**
​      **esp12E模组                （11元）**
​      **电阻（10K）               （1元）**
​      **CH340模块                 （3元）**
​      **其他（按键、排针、杜邦线） （1元）**

#####    **原理图：**

​           **（网上转的忘记出处）**

​	

![]()

#####     **焊接：**
        **en   vcc接口之间加电阻**
        **gpio2  vcc接口之间加电阻**
        **rst   gnd接口之间加重启按键**
        **gpio0 gnd接口之间加刷固件按键**

##### **开机模式：**
           **运行模式：**
                **vcc     接3.3v电源**
                **gnd    接地**
           **刷固件模式：**
                **vcc     接3.3v电源**
                **gnd    接地**
                **TX RX  接CH340**
                **按住刷固件按键，然后按一下重启按键，松开刷固件按键即可进入刷固件模式**
     **开始刷固件：**
          **1、安装python环境（https://www.python.org/downloads/****）**
          **2、安装pip（****https://pypi.python.org/pypi/pip）**
          **2、安装esptool（pip install esptool）**
          **3、下载micropython固件（http://micropython.org/download#esp8266****）**
          **4、进入刷固件模式**
          **5、****python esptool.py --port com口 erase_flash 清除掉原来的固件**
          **6、python esptool.py --port com口 --baud 
115200 write_flash --flash_size=detect 0 esp8266-                       
     20170108-v1.8.7.bin 刷新固件。**
           **7、重启进入运行模式。**