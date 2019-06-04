



'''
@File   :beike.py
@Author :youxinweizhi
@Date   :2019/5/23
@Github :https://github.com/youxinweizhi

#redeme
#main.py
from beike import Device
#此处需要修改
ID = "xxx"                       # 设备ID
API_KEY = "xxxxxx"              # 设备APIKEY

# 回调函数
def say_cb(msg):  
  print(msg) #写自己的处理逻辑

#构建实例
device = Device(ID, API_KEY)        # 构建bigiot设备
device.say_callback(say_cb)         # 设置回调函数
device.main()

'''
import socket
import json
import time

Server_IP = "121.42.180.30"
Server_Port = 8282

class Device:
    def __init__(self, id, api_key):
        self.ID = str(id)
        self.K = api_key
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.setblocking(True)
        self.say_cb = None
        self.wdog=WDOG()
        self.wdog.init(60000)
        
    def say_callback(self, f):
        """
        接收设备通讯的回调函数
        """
        self.say_cb = f
    def _ping(self):
        """
        心跳检测
        """
        obj = b'{"M":"beat"}\n'
        print('Response to server heartbeat detection')
        self.s.send(obj)
        
    def check_in(self):
        """
        设备登录
        """
        obj = {"M": "checkin", "ID": self.ID, "K": self.K}
        obj = json.dumps(obj) + "\n"
        obj=obj.encode()
        self.s.send(obj)
        
    def check_out(self):
        """
        设备退出
        """
        obj = {"M": "checkout", "ID": self.ID, "K": self.K}
        obj = json.dumps(obj) + "\n"
        obj = obj.encode()
        self.s.send(obj)
    def update(self,ID,id,data):
        """
        向接口发送数据。先在平台新增并设置接口。
        :param id(int): 接口ID,类型为整形
        :param data(str): 发送数据,类型为字符串,一般用于上传传感器数据。
        """
        dict_data = {}
        dict_data[str(id)] = data
        obj = json.dumps(obj) + "\n"
        obj = obj.encode()
        self.s.send(obj)        
    def main(self):
        while 1:
            self.s.connect((Server_IP, Server_Port))
            while 1:
                rec=self.s.recv(512).decode()
                if len(rec) == 0:
                    continue
                res_json=json.loads(rec)
                #print(res_json)                        
                if res_json['M']=="WELCOME TO BIGIOT":
                  print(res_json['M'])
                  self.check_out()
                  self.check_in()             
                  continue
                if res_json['M']=='b':
                  self._ping()
                  continue                       
                if res_json['M']=="checkinok":
                  print('................login...................')
                  continue                  
                if res_json['M'] == 'say'and res_json['C'] is not None:                           
                    self.say_cb(res_json)



