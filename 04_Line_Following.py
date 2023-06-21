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
# DC Motors generate electrical noise when running that can reset the microcontroller in extreme
# cases. A capacitor can be used to help prevent this.
pwm_1a = pwmio.PWMOut(PWM_M1A, frequency=10000)
pwm_1b = pwmio.PWMOut(PWM_M1B, frequency=10000)
motorL = motor.DCMotor(pwm_1a, pwm_1b)
pwm_2a = pwmio.PWMOut(PWM_M2A, frequency=10000)
pwm_2b = pwmio.PWMOut(PWM_M2B, frequency=10000)
motorR = motor.DCMotor(pwm_2a, pwm_2b)

# Sensors
SA = analogio.AnalogIn(board.GP26)

def Robot_Movement(sL, sR):
    motorL.throttle = sL
    motorR.throttle = sR

while True:
    
    an =  (SA.value * 3.3) / 65536
    print(an)
    
    if (an>1.4 and an<1.5):  #1.4 - 1.7v
        print("move forward")
        Robot_Movement(0.5, 0.53)
    elif (an>1.8 and an<2.2): # 1.7 - 2.2v
        Robot_Movement(0.5, 0.3)
    elif (an>0.8 and an<1.4): # 0.8 - 1.4v
        Robot_Movement(0.3, 0.53)
    elif (an>2.2 and an<2.85): # 2.2 - 2.85v
        Robot_Movement(0.6, 0.2)
    elif (an>0.4 and an<0.8): # 0.6 - 0.8v
        Robot_Movement(0.2, 0.63)
    elif (an>2.85 and an<3.0): # 2.85 - 3.0v
        Robot_Movement(0.6, 0)
    elif (an>0.3 and an<0.4): # 0.3 - 0.4v
        Robot_Movement(0, 0.64)
    elif (an<0.3 or an>3): # <0.3v or >3V
        #Robot_Movement(0, 0)
        continue 