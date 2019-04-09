
# coding: gb2312
from machine import Pin,UART,I2C
import time
from dht import DHT11
from sht25 import SHT25

u=UART(1,rx=16,tx=17,baudrate=9600)
def get_wsd():
  scl=Pin(22)
  sda=Pin(21)
  res=SHT25(I2C(scl=scl,sda=sda))
  return res.getTemperature(),res.getHumidity()


class TJC3224T024(object):
    def __init__(self,uart=None):
        if uart is None:
            self.uart = UART(1, 9600) # UART on 
            self.uart.init(9600, bits=8, parity=None, stop=1)
        else:
            self.uart = uart
    def send_text(self,tn,text):
        txt='{0}.txt="{1}"'.format(tn,text)
        self.exec_cmd(txt)

    def send_line(self,tn,text):
        txt='{0}.txt=t0.txt+"{1}"'.format(tn,text)
        self.exec_cmd(txt)

    def send_enter(self,tn):
        txt='{0}.txt={1}.txt+"\\r"'.format(tn,tn)
        self.exec_cmd(txt)
    def cls(self,tn):
        txt='{0}.txt=""'.format(tn)
        self.exec_cmd(txt)

    def exec_cmd(self,txt):
        self.uart.write(txt)
        self.uart.write(b'\xff\xff\xff')
        self.read_all()

    def read_all(self):
        data=self.uart.read()
        print(data)
        
if __name__ == '__main__':
    test=TJC3224T024(u)
    while 1:
      wendu,shidu=get_wsd()
      test.send_text('t0','%0.2f'%wendu)
      test.send_text('t1','%0.2f'%shidu)
      time.sleep(1)    