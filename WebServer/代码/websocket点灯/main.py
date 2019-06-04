import time
from microWebSrv import MicroWebSrv
from microbit import *


def _acceptWebSocketCallback(webSocket, httpClient) :
	print("WS ACCEPT")
	webSocket.RecvTextCallback   = _recvTextCallback
	webSocket.RecvBinaryCallback = _recvBinaryCallback
	webSocket.ClosedCallback 	 = _closedCallback


def _recvTextCallback(webSocket, msg) :
  
  if msg=="on":
    display.show(Image.HAPPY)
  elif msg=="off":
    display.off()
  else:
    pass
  print("WS RECV TEXT : %s" % msg)
  webSocket.SendText("Reply for %s" % msg)


def _recvBinaryCallback(webSocket, data) :
	print("WS RECV DATA : %s" % data)

def _closedCallback(webSocket) :
	print("WS CLOSED")

  
srv = MicroWebSrv(webPath="/")
srv.MaxWebSocketRecvLen     = 256
srv.WebSocketThreaded		= True
srv.AcceptWebSocketCallback = _acceptWebSocketCallback
srv.Start(threaded=True)