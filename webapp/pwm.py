import RPi.GPIO as GPIO

PWM0_PIN    = 18    # cobbler pin 12 (GPIO18)
PWM1_PIN    = 13    # cobbler pin 33 (GPIO13)
DIR_PIN     = 25    # cobbler pin 22 (GPIO25)

channel_map = {}    # keep track of channel handle to pin

# =============================================================================
# create a sensor object
# -----------------------------------------------------------------------------
class PiPwm(object):
    """Raspberry Pi Internet 'IoT GPIO PWM'."""

    def __init__(self):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)              # BMC Pin numbering convention
        GPIO.setup(PWM0_PIN, GPIO.OUT)      # PWM0 as output
        GPIO.setup(PWM1_PIN, GPIO.OUT)      # PWM1 as output
        GPIO.output(PWM0_PIN,0)             # initialize PWM0 state to off
        GPIO.output(PWM1_PIN,0)             # initialize PWM1 state to off
        GPIO.setup(DIR_PIN,  GPIO.IN)       # Direction Pin as input w/pu
        GPIO.setup(DIR_PIN,  GPIO.IN, pull_up_down=GPIO.PUD_UP)
        #  import pdb; pdb.set_trace()

    def read_direction(self):
        """Read the direction pin state."""
        return GPIO.input(DIR_PIN)

    # start a PWM running
    def start_pwm(self, pwm, freq, duty):
        """Setup and start a PWM to a particular frequency and duty cycle"""
        if(pwm == 0):
            pwm_ch = GPIO.PWM(PWM0_PIN, freq)
            channel_map[pwm_ch] = PWM0_PIN

        if(pwm == 1):
            pwm_ch = GPIO.PWM(PWM1_PIN, freq)
            channel_map[pwm_ch] = PWM1_PIN

        pwm_ch.start(duty)
        return pwm_ch

    # change a running PWM's duty cycle
    def change_duty_cycle(self, pwm_ch, duty):
        pwm_ch.ChangeDutyCycle(duty)


    # change a running PWM's duty cycle
    def change_frequency(self, pwm_ch, freq):
        pwm_ch.ChangeFrequency(freq)

    # stop a PWM running
    def stop_pwm(self, pwm_ch):
        """Stop a PWM on a particular channel"""
        pwm_ch.stop()
        # make sure output is off
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(channel_map[pwm_ch], GPIO.OUT)
        GPIO.output(channel_map[pwm_ch],0)
