"""
DESCRIPTION:
This example code will uses: Robo Pico and Raspberry Pi Pico W to control
2-wheel car through HTTP server connected between WiFi or Mobile Hotspot (local host).

CONNECTIONS:
Robo Pico M1A - Left Motor -ve
Robo Pico M1B - Left Motor +ve
Robo Pico M2A - Right Motor +ve
Robo Pico M2B - Right Motor -ve

COMPANY  : Cytron Technologies Sdn Bhd
WEBSITE  : www.cytron.io
EMAIL    : support@cytron.io

REFERENCE:
Code adapted from 2023 Liz Clark for Adafruit Industries:
https://learn.adafruit.com/pico-w-http-server-with-circuitpython/code-the-pico-w-http-server
"""
import os
import time
import ipaddress
import wifi
import socketpool
import board
import microcontroller
import digitalio
import pwmio
from adafruit_motor import motor
from digitalio import DigitalInOut, Direction
from adafruit_httpserver.server import HTTPServer
from adafruit_httpserver.request import HTTPRequest
from adafruit_httpserver.response import HTTPResponse
from adafruit_httpserver.methods import HTTPMethod
from adafruit_httpserver.mime_type import MIMEType


# Left Motor
PWM_M1A = board.GP8
PWM_M1B = board.GP9
# Right Motor
PWM_M2A = board.GP10
PWM_M2B = board.GP11

# DC motor setup
# DC Motors generate electrical noise when running that can reset the microcontroller in extreme
# cases. A capacitor can be used to help prevent this.
pwm_1a = pwmio.PWMOut(PWM_M1A, frequency=10000)
pwm_1b = pwmio.PWMOut(PWM_M1B, frequency=10000)
motorL = motor.DCMotor(pwm_1a, pwm_1b)
pwm_2a = pwmio.PWMOut(PWM_M2A, frequency=10000)
pwm_2b = pwmio.PWMOut(PWM_M2B, frequency=10000)
motorR = motor.DCMotor(pwm_2a, pwm_2b)

def Robot_Movement(sL, sR):
    motorL.throttle = sL
    motorR.throttle = sR
    
    
#  connect to network
print()
print("Connecting to WiFi")

#  set static IP address
# ipv4 =  ipaddress.IPv4Address("192.168.1.42")
# netmask =  ipaddress.IPv4Address("255.255.255.0")
# gateway =  ipaddress.IPv4Address("192.168.1.1")
# wifi.radio.set_ipv4_address(ipv4=ipv4,netmask=netmask,gateway=gateway)

#  connect to your SSID
wifi.radio.connect(os.getenv('CIRCUITPY_WIFI_SSID'), os.getenv('CIRCUITPY_WIFI_PASSWORD'))

print("Connected to WiFi")
pool = socketpool.SocketPool(wifi.radio)
server = HTTPServer(pool, "/static")

def move_forward():
    print ("Forward")
    Robot_Movement(0.5, 0.53)
    
def move_backward():
    print ("Backward")
    Robot_Movement(-0.5, -0.53)
    
def move_left():
    print ("Left")
    Robot_Movement(0, 0.5)
    
def move_right():
    print ("Right")
    Robot_Movement(0.5, 0)
    
def move_stop():
    print ("Stop")
    Robot_Movement(0, 0)
    
#  the HTML script
#  setup as an f string
#  this way, can insert string variables from code.py directly
#  of note, use {{ and }} if something from html *actually* needs to be in brackets
#  i.e. CSS style formatting
def webpage():
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <meta http-equiv="Content-type" content="text/html;charset=utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <script>
    function buttonDown(button) {{
        // Send a POST request to tell the Pico that the button was pressed
        var xhttp = new XMLHttpRequest();
        xhttp.open("POST", "/", true);
        xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
        xhttp.send(button + "=true");
    }}
    function buttonUp() {{
        // Send a POST request to tell the Pico that the button was released (stop)
        var xhttp = new XMLHttpRequest();
        xhttp.open("POST", "/", true);
        xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
        xhttp.send("stop=true");
    }}
    </script>
    <style>
      h1 {{
        text-align: center;
         }}
      body {{
          display: flex;
          flex-direction: column;
          align-items: center;
          justify-content: center;
          height: 80vh;
          margin: 0;
        }}
        .controls {{
          display: grid;
          grid-template-columns: repeat(3, 1fr);
          gap: 10px;
        }}
        .button {{
          font-size: 90px;
          display: flex;
          align-items: center;
          justify-content: center;
          //border: 2px solid black;
          //border-radius: 10px;
          background: white;
          padding: 10px;
          user-select: none;
          width: 80px;
          height: 80px;
        }}
    </style>

    </head>
    <body>
    <h1>Robo Pico Wifi Control Car</h1>
    <center><b>
    <div class="controls">
        <div></div>
        <div class="button" id="forward" ontouchstart="buttonDown(this.id)" ontouchend="buttonUp()" 
        onmousedown="buttonDown(this.id)" onmouseup="buttonUp()">⬆️</div>
        <div></div>
        
        <div class="button" id="left" ontouchstart="buttonDown(this.id)" ontouchend="buttonUp()" 
        onmousedown="buttonDown(this.id)" onmouseup="buttonUp()">⬅️</div>
        <div></div>
        <div class="button" id="right" ontouchstart="buttonDown(this.id)" ontouchend="buttonUp()" 
        onmousedown="buttonDown(this.id)" onmouseup="buttonUp()">➡️</div>
        
        <div></div>
        <div class="button" id="backward" ontouchstart="buttonDown(this.id)" ontouchend="buttonUp()" 
        onmousedown="buttonDown(this.id)" onmouseup="buttonUp()">⬇️</div>
        <div></div>
    </div>
    </body></html>
    
    """
    return html


#  route default static IP
@server.route("/")
def base(request: HTTPRequest):  # pylint: disable=unused-argument
    #  serve the HTML f string
    #  with content type text/html
    with HTTPResponse(request, content_type=MIMEType.TYPE_HTML) as response:
        response.send(f"{webpage()}")

#  if a button is pressed on the site
@server.route("/", method=HTTPMethod.POST)
def buttonpress(request: HTTPRequest):
    #  get the raw text
    raw_text = request.raw_request.decode("utf8")
    #print(raw_text)
    #  if the Forward button was pressed
    if "forward" in raw_text:
        #  move car forward
        move_forward()
    if "backward" in raw_text:
        #  move car forward
        move_backward()
    if "right" in raw_text:
        #  move car forward
        move_right()
    if "left" in raw_text:
        #  move car forward
        move_left()
    if "stop" in raw_text:
        #  move car forward
        move_stop()
    #  reload site
    with HTTPResponse(request, content_type=MIMEType.TYPE_HTML) as response:
        response.send(f"{webpage()}")

print("starting server..")
#  startup the server
try:
    server.start(str(wifi.radio.ipv4_address))
    print("Listening on http://%s" % wifi.radio.ipv4_address)
#  if the server fails to begin, restart the pico w
except OSError:
    time.sleep(5)
    print("restarting..")
    microcontroller.reset()


while True:
    try:
        #  poll the server for incoming/outgoing requests  
        server.poll()
    except Exception as e:
        print(e)
        continue




