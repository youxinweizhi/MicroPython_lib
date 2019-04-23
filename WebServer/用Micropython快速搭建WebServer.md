# 用Micropython快速搭建WebServer

## 1、介绍

​	之前我们介绍过在python中写socket，当然那样还是太麻烦，有没有像pc端apache一样的支持n多功能，牛逼的现成服务器软件呢？ 这时MicroWebSrv闪亮登场！！！

​	**MicroWebSrv** 是一个在MicroPython平台上支持websocket，html/python，路由功能的微型http服务器

核心文件是"microWebSrv.py"，在开发板中引入这个py文件即可快速搭建自己的webserver服务器。



## 2、搭建webserver

```
#编辑main.py修改内容如下

from microWebSrv import MicroWebSrv

@MicroWebSrv.route('/test/','GET')
def test(httpClient,httpResponse):
  t=httpClient.GetRequestMethod()
  print(t)

  content="""\

  <!DOCTYPE html>
  <html lang="en">
  <head>
      <meta charset="UTF-8">
      <title>Title</title>
  </head>
  <body>
	<h1>
        Hello world!
      </h1>



  </body>
  </html>
  """

  httpResponse.WriteResponseOk( headers         = None,
                                contentType     = "text/html",
                                contentCharset  = "UTF-8",
                                content         = content )

srv = MicroWebSrv(webPath="/")
srv.Start(threaded=True)


```

