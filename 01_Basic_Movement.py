'''
Basic Robot Movement using Maker Drive and CircuitPython on Pi Pico W.

Libraries required from bundle (https://circuitpython.org/libraries):
  - adafruit_motor
  
References:
  - https://learn.adafruit.com/circuitpython-essentials/circuitpython-pwm
  - https://my.cytron.io/tutorial/control-dc-motor-using-maker-drive-and-circuitpython-on-rp2040
  
'''

import time
import board
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

while True:
    Robot_Movement(0, 0) #Stop
    time.sleep(2)
    Robot_Movement(0.5, 0.54) #Forward
    time.sleep(3)
    Robot_Movement(-0.5, -0.52) #Backward
    time.sleep(3)
    Robot_Movement(0.1, 0.5) #Turn Left
    time.sleep(3)
    Robot_Movement(0.5, 0.1) #Turn Right
    time.sleep(3)