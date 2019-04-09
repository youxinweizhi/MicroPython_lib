
#!/usr/bin/env python
# coding: utf-8
'''
@File   :main.py
@Author :youxinweizhi
@Date   :2019/4/9
@Github :https://github.com/youxinweizhi
'''
from machine import Pin,I2C
import time
from sht25 import SHT25

def get_wsd():
  scl=Pin(22)
  sda=Pin(21)
  res=SHT25(I2C(scl=scl,sda=sda))
  return res.getTemperature(),res.getHumidity()



if __name__ == '__main__':
    while 1:
      print('温度：%s, 湿度：%s'%(get_wsd())
      time.sleep(1)    