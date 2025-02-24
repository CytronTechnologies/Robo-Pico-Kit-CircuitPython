'''
Simple Light Searching Robot using only ONE Light Dependent Resistor (LDR)
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

# Press the GP20 push button on the ROBOPICO to execute the code
execute_button = digitalio.DigitalInOut(board.GP20)
execute_button.direction = digitalio.Direction.INPUT
execute_button.pull = digitalio.Pull.UP

# DC motor setup
# DC Motors generate electrical noise when running that can reset the microcontroller in extreme
# cases. A capacitor can be used to help prevent this.
pwm_1a = pwmio.PWMOut(PWM_M1A, frequency=10000)
pwm_1b = pwmio.PWMOut(PWM_M1B, frequency=10000)
motorL = motor.DCMotor(pwm_1a, pwm_1b)
pwm_2a = pwmio.PWMOut(PWM_M2A, frequency=10000)
pwm_2b = pwmio.PWMOut(PWM_M2B, frequency=10000)
motorR = motor.DCMotor(pwm_2a, pwm_2b)

ldr = analogio.AnalogIn(board.GP27)

def Robot_Movement(sL, sR):
    motorL.throttle = sL
    motorR.throttle = sR
    
print("Press GP20 button to start...")


while True:
    if not execute_button.value:  # Button pressed (logic is active low)
        while True:
            raw = ldr.value
            print("raw = {:5d}".format(raw))
            time.sleep(0.1)
            if (raw < 29000):            # << Please changed HERE
                Robot_Movement(0.5, 0.53) # Forward
                print("Move Forward")
            else:
                Robot_Movement(0.1, 0.3) # Turn Left
                print("Stop")
