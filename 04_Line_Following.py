'''
Maker Line Following Robot

Reference:
    - https://my.cytron.io/p-maker-line-simplifying-line-sensor-for-beginner
'''
import time
import board
import analogio
import digitalio
import pwmio
from adafruit_motor import motor

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

# Sensors
SA = analogio.AnalogIn(board.GP26)

# Button setup
execute_button = digitalio.DigitalInOut(board.GP20)
execute_button.direction = digitalio.Direction.INPUT
execute_button.pull = digitalio.Pull.UP

def Robot_Movement(sL, sR):
    motorL.throttle = sL
    motorR.throttle = sR

print("Press GP20 button to start...")

while True:
    if not execute_button.value:  # Button pressed (active low)
        print("Button pressed! Starting line-following robot...")
        while True:
            an = (SA.value * 3.3) / 65536
            print(an)
            
            if 1.4 < an < 1.5:  # 1.4 - 1.7v
                print("move forward")
                Robot_Movement(0.5, 0.53)
            elif 1.8 < an < 2.2:  # 1.7 - 2.2v
                Robot_Movement(0.5, 0.3)
            elif 0.8 < an < 1.4:  # 0.8 - 1.4v
                Robot_Movement(0.3, 0.53)
            elif 2.2 < an < 2.85:  # 2.2 - 2.85v
                Robot_Movement(0.6, 0.2)
            elif 0.4 < an < 0.8:  # 0.6 - 0.8v
                Robot_Movement(0.2, 0.63)
            elif 2.85 < an < 3.0:  # 2.85 - 3.0v
                Robot_Movement(0.6, 0)
            elif 0.3 < an < 0.4:  # 0.3 - 0.4v
                Robot_Movement(0, 0.64)
            elif an < 0.3 or an > 3:  # <0.3v or >3V
                # Continue without movement
                continue
