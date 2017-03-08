import RPi.GPIO as GPIO
import time

LED     = 23    # GPIO23 RUNNING STATUS LED
SW      = 25    # cobbler pin 22 (GPIO25)

AIN1    = 19    # GPIO19 TB6612 AIN1 Logic Input
AIN2    = 26    # GPIO26 TB6612 AIN2 Logic Input
BIN1    = 20    # GPIO20 TB6612 BIN1 Logic Input
BIN2    = 21    # GPIO21 TB6612 BIN2 Logic Input
STBY    = 16    # GPIO16 TB6612 Standby Input

# =============================================================================
# create a Stepper Motor Object
# -----------------------------------------------------------------------------
class PiStepper(object):
    """Raspberry Pi 'IoT GPIO Stepper Motor'."""

    def __init__(self, freq=10, steps=600):
        self.steps_per_rev = steps
        self.sec_per_step = 0.1
        self.steppingcounter = 0
        self.currentstep = 0
        self.speed = 0
        self.state = 0
        self.steps = 0
        self.direction = 0
        self.position = 0

        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)          # BMC Pin numbering convention
        GPIO.setup(LED, GPIO.OUT)       # LED as output
        GPIO.setup(AIN1, GPIO.OUT)      # AIN1 as output
        GPIO.setup(AIN2, GPIO.OUT)      # AIN2 as output
        GPIO.setup(BIN1, GPIO.OUT)      # BIN1 as output
        GPIO.setup(BIN2, GPIO.OUT)      # BIN2 as output
        GPIO.setup(STBY, GPIO.OUT)      # Standby as output
        GPIO.output(AIN1,0)             # initialize AIN1 state to off
        GPIO.output(AIN2,0)             # initialize AIN2 state to off
        GPIO.output(BIN1,0)             # initialize BIN1 state to off
        GPIO.output(BIN2,0)             # initialize BIN2 state to off
        GPIO.output(STBY,0)             # initialize Standby state to off
        GPIO.setup(SW,  GPIO.IN, pull_up_down=GPIO.PUD_UP)
        #  import pdb; pdb.set_trace()

# -----------------------------------------------------------------------------
    def hello(self):
        print "Hello Stepper"

    def start(self):
        print "Starting Stepper Motor"
        GPIO.output(LED,1)      # turn on LED status
        GPIO.output(STBY,1)     # TB6612 Standby State TRUE
        self.state = 1

    def stop(self):
        print "Stopping Stepper Motor"
        GPIO.output(LED,0)      # turn off LED status
        GPIO.output(STBY,0)     # TB6612 Standby State FALSE
        self.state = 0

    def getState(self):
        return self.state

    # get motor position
    def getPosition(self):
        return self.position

    # set motor position
    def setPosition(self,position):
        self.position = position

    # set the speed parameters for stepper motor based on RPM
    def setSpeed(self, rpm):
        self.sec_per_step = 60.0 / (self.steps_per_rev * rpm)
        self.steppingcounter = 0
        self.speed = rpm

    def getSpeed(self):
        return self.speed
# -----------------------------------------------------------------------------
    # perform one step in sequence at a direction CW or CCW
    def oneStep(self, direction):
        # go to next 'step' and wrap around
        self.direction = direction
        coils = [0, 0, 0, 0]
        step2coils = [
        #    A2 B1 A1 B2
            [1, 0, 0, 0],
            [1, 1, 0, 0],
            [0, 1, 0, 0],
            [0, 1, 1, 0],
            [0, 0, 1, 0],
            [0, 0, 1, 1],
            [0, 0, 0, 1],
            [1, 0, 0, 1] ]
        coils = step2coils[self.currentstep]
        # print '%d', self.currentstep, " : coils = AIN1:%d AIN2:%d BIN1:%d BIN2:%d" % (coils[2],coils[0],coils[1],coils[3])

        # post increment/decrement the modulo step counter depeneding on direction
        #   also update the stepper position (one tic per step)
        if(direction == 1):
            self.currentstep += 1
            self.position += 1
        else:
            self.currentstep -= 1
            self.position -= 1
        self.currentstep %= 8

        #print "coils state = " + str(coils)
        self.setPin(AIN2, coils[0])
        self.setPin(BIN1, coils[1])
        self.setPin(AIN1, coils[2])
        self.setPin(BIN2, coils[3])

    # set current pin in sequence
    def setPin(self, pin, value):
        GPIO.output(pin,value)

    # set motor direction
    def setDirection(self,direction):
        self.direction = direction

    # get motor direction
    def getDirection(self):
        return self.direction

    # set motor steps
    def setSteps(self,steps):
        self.steps = steps

    # get motor direction
    def getSteps(self):
        return self.steps

    # execute all steps
    def step(self, steps):
        s_per_s = self.sec_per_step

        for s in range(steps):
            self.oneStep(self.direction)
            time.sleep(s_per_s)

    # de-energize all coils
    def nullCoils(self):
        coils = [0, 0, 0, 0]
        self.setPin(AIN2, coils[0])
        self.setPin(BIN1, coils[1])
        self.setPin(AIN1, coils[2])
        self.setPin(BIN2, coils[3])
