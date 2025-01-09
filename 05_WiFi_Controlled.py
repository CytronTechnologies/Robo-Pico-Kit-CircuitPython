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
from adafruit_httpserver import Server, Request, Response, POST

# Left Motor
PWM_M1A = board.GP8
PWM_M1B = board.GP9
# Right Motor
PWM_M2A = board.GP10
PWM_M2B = board.GP11

# DC motor setup
pwm_1a = pwmio.PWMOut(PWM_M1A, frequency=10000)
pwm_1b = pwmio.PWMOut(PWM_M1B, frequency=10000)
motorL = motor.DCMotor(pwm_1a, pwm_1b)
pwm_2a = pwmio.PWMOut(PWM_M2A, frequency=10000)
pwm_2b = pwmio.PWMOut(PWM_M2B, frequency=10000)
motorR = motor.DCMotor(pwm_2a, pwm_2b)

def Robot_Movement(sL, sR):
    motorL.throttle = sL
    motorR.throttle = sR

def move_forward():
    print("Forward")
    Robot_Movement(0.5, 0.53)
    
def move_backward():
    print("Backward")
    Robot_Movement(-0.5, -0.53)
    
def move_left():
    print("Left")
    Robot_Movement(0, 0.5)
    
def move_right():
    print("Right")
    Robot_Movement(0.5, 0)
    
def move_stop():
    print("Stop")
    Robot_Movement(0, 0)

# Connect to network
print("Connecting to WiFi")
try:
    wifi.radio.connect(os.getenv('CIRCUITPY_WIFI_SSID'), os.getenv('CIRCUITPY_WIFI_PASSWORD'))
    print("Connected to WiFi")
    print("IP address:", wifi.radio.ipv4_address)
except Exception as e:
    print("Failed to connect to WiFi:", str(e))
    microcontroller.reset()

pool = socketpool.SocketPool(wifi.radio)
server = Server(pool, "/static", debug=False)  # Set debug to False to reduce output

def webpage():
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <meta http-equiv="Content-type" content="text/html;charset=utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Robo Pico Control</title>
    <script>
    function buttonDown(button) {{
        var xhttp = new XMLHttpRequest();
        xhttp.open("POST", "/", true);
        xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
        xhttp.send(button + "=true");
    }}
    function buttonUp() {{
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
    </body>
    </html>
    """
    return html

@server.route("/")
def base(request: Request):
    return Response(request, webpage(), content_type='text/html')

@server.route("/", POST)
def buttonpress(request: Request):
    raw_text = request.body.decode("utf8")  # Use .body instead of raw_request
    
    if "forward" in raw_text:
        move_forward()
    elif "backward" in raw_text:
        move_backward()
    elif "right" in raw_text:
        move_right()
    elif "left" in raw_text:
        move_left()
    elif "stop" in raw_text:
        move_stop()
        
    return Response(request, webpage(), content_type='text/html')

print("Starting server...")
try:
    server.start(str(wifi.radio.ipv4_address), port=80)
    print(f"Server running at http://{wifi.radio.ipv4_address}")
except Exception as e:
    print("Failed to start server:", str(e))
    time.sleep(5)
    microcontroller.reset()

while True:
    try:
        server.poll()
    except Exception as e:
        continue
