


from microWebSrv import MicroWebSrv
from machine import Pin
from neopixel import NeoPixel


def set_led(rgb):
  pin = Pin(4, Pin.OUT)   # set GPIO0 to output to drive NeoPixels
  np = NeoPixel(pin, 30)   # create NeoPixel driver on GPIO0 for 8 pixels
  for x in range(30):
    np[x]=rgb
  np.write()              # write data to all pixels



import random
def set_random():
  pin = Pin(4, Pin.OUT)   # set GPIO0 to output to drive NeoPixels
  np = NeoPixel(pin, 30)   # create NeoPixel driver on GPIO0 for 8 pixels
  for x in range(30):
    r=random.randint(0,100)
    g=random.randint(0,100)
    b=random.randint(0,100)
    np[x]=(r,g,b)
  np.write()            # write data to all pixels



  
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
      <link rel="stylesheet" href="/style.css">
  </head>
  <body>
  <div class="colorpicker"></div>
  <script src="https://cdn.bootcss.com/jquery/3.3.1/jquery.min.js"></script>
  <script src='/tinycolor.min.js'></script>
  <script src="/index.js"></script>
  </body>
  </html>
  """
  
  httpResponse.WriteResponseOk( headers         = None,
                                contentType     = "text/html",
                                contentCharset  = "UTF-8",
                                content         = content )


@MicroWebSrv.route('/test/','POST')
def test_(httpClient,httpResponse):
  data=httpClient.ReadRequestContentAsJSON()
  r=int(data['code']['rgb']['r']/10)
  g=int(data['code']['rgb']['g']/10)
  b=int(data['code']['rgb']['b']/10)
  print(r,g,b)
  set_led((r,g,b))
  
  httpResponse.WriteResponseRedirect('/test/')



srv = MicroWebSrv(webPath="/")
srv.SetNotFoundPageUrl(url="/test")
srv.Start(threaded=True)




