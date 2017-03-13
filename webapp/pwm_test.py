#!/usr/bin/python

import time
from pwm import PiPwm

PWM0 = 0    # logical handle for RPi3 PWM0
PWM1 = 1    # logical handle for RPi3 PWM1
# create an instance of my pi thing.
pi_pwm = PiPwm()

# Create two counter breathing PWM LEDs
print('Connect RED LED to GPIO18, GREEN LED to GPIO13, DIR SW to GPIO25')

time.sleep(1.0)
print('Starting PWM0 at 5Hz with 75% duty cycle')
ch0 = pi_pwm.start_pwm(0, 5, 75)
# time.sleep(0.01)
print('Starting PWM1 at 3Hz with 10% duty cycle')
ch1 = pi_pwm.start_pwm(1, 3, 50)

time.sleep(10.0)
print('Stopping PWM0')
pi_pwm.stop_pwm(ch0)
time.sleep(3.0)
print('Stopping PWM1')
pi_pwm.stop_pwm(ch1)
