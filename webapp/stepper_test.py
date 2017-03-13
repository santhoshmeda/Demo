#!/usr/bin/python

import time
from stepper import PiStepper

CW = 1
CCW  = 0

# Create a stepper motor controller object
pi_smc = PiStepper()
print('Motor Controller Initialized')

# set the initial RPM speed

pi_smc.start()
pi_smc.setSpeed(100)
print 'Finding Home Position...'
pi_smc.setDirection(CCW)
pi_smc.step(1200)
pi_smc.setPosition(0)

# loop through several CW and CCW steps
for rpm in xrange(100,500):
    pi_smc.setSpeed(rpm)
    print '\n-------> Speed: %d rpm <-------' % (rpm)

    print('Stepping CW')
    pi_smc.setDirection(CW)
    pi_smc.step(600)
    time.sleep(0.2)
    pi_smc.step(600)
    print 'Position: %d (steps)' % (pi_smc.getPosition())

    print('Change Dir')
    pi_smc.nullCoils()
    time.sleep(0.1)


    print('Stepping CCW')
    pi_smc.setDirection(CCW)
    pi_smc.step(600)
    time.sleep(0.2)
    pi_smc.step(600)
    print 'Position: %d (steps)' % (pi_smc.getPosition())
    print('Change Dir')
    pi_smc.nullCoils()
    time.sleep(0.1)


print('Stopping Motor')
pi_smc.stop()
