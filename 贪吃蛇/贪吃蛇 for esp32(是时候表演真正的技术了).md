# 贪吃蛇 for esp32(是时候表演真正的技术了) 



## 效果图：



## 连线图：

查看esp32 驱动ssd1306

## 代码：



```


import random
import machine
from machine import Pin,I2C,ADC
import ssd1306
from time import sleep
import framebuf


i2c = I2C(scl=Pin(18), sda=Pin(19), freq=900000)
oled = ssd1306.SSD1306_I2C(128,64, i2c)
oled.poweron()
oled.init_display()
oled.fill(0)
oled.show()

w=8
h=8
st=8

base_x=20
base_y=20
snoke=[[10,10],[20,10],[30,10]]
by="right"
oled.fill(0)
oled.fill_rect(snoke[0][0],snoke[0][1],w,h,1)
oled.fill_rect(snoke[1][0],snoke[1][1],w,h,1)
oled.fill_rect(snoke[2][0],snoke[2][1],w,h,1)
oled.show()
  
def suiji():
  global base_x
  global base_y
  base_x = random.randint(10,100)
  base_y = random.randint(10,50)

def base():
  oled.fill_rect(base_x,base_y,w,h,1)
def check():

  if (abs(base_x-snoke[0][0]))<=2 and (abs(base_y-snoke[0][1]))<=2:
    if by=="up":
      new=[snoke[-1][0],snoke[-1][1]+st]
      snoke.append(new)
      suiji()
    if by=="down":
        new=[snoke[-1][0],snoke[-1][1]-st]
        snoke.append(new)
        suiji()
    if by=="left":
        new=[snoke[-1][0]+st,snoke[-1][1]]
        snoke.append(new)
        suiji()
    if by=="right":
        new=[snoke[-1][0]-st,snoke[-1][1]]
        snoke.append(new)
        suiji()
def right():
  global snoke
  oled.fill(0)
  base()
  new=[snoke[0][0]+st,snoke[0][1]]
  snoke.insert(0,new)
  snoke.pop()
  for x in range(len(snoke)):
    oled.fill_rect(snoke[x][0],snoke[x][1],w,h,1)
  oled.show()
  
def up():
  global snoke
  oled.fill(0)
  base()
  new=[snoke[0][0],snoke[0][1]-st]
  snoke.insert(0,new)
  snoke.pop()
  for x in range(len(snoke)):
    oled.fill_rect(snoke[x][0],snoke[x][1],w,h,1)
  oled.show()
    
  
  
def down():
  global snoke
  oled.fill(0)
  base()
  new=[snoke[0][0],snoke[0][1]+st]
  snoke.insert(0,new)
  snoke.pop()
  for x in range(len(snoke)):
    oled.fill_rect(snoke[x][0],snoke[x][1],w,h,1)
  oled.show()
def left():
  global snoke
  oled.fill(0)
  base()
  new=[snoke[0][0]-st,snoke[0][1]]
  snoke.insert(0,new)
  snoke.pop()
  for x in range(len(snoke)):
    oled.fill_rect(snoke[x][0],snoke[x][1],w,h,1)
  oled.show()  

a1=ADC(Pin(35))
a2=ADC(Pin(34))
  
def test():
  global by
  x=a1.read()
  y=a2.read()
  if x==0:
    by="left"
  elif x==4095:
    by="right"
  elif y==0:
    by="up"
  elif y==4095:
    by="down"


while 1:
  check()
  test()
  if by=="right":
    right()
  elif by=="left":
    left()
  elif by=="up":
    up()
  elif by=="down":
    down()
  sleep(0.5)
  print('snoke:%s,%s' %(snoke[0][0],snoke[0][1]))
  print('base:%s,%s' %(base_x,base_y))


```

 





