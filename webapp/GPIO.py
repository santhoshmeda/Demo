import RPi.GPIO as GPIO

# GPIO_LIST(RED_LED)    = 18    # cobbler pin 12 (GPIO18)
# GRN_LED    = 13    # cobbler pin 33 (GPIO13)
# BLU_LED    = 23    # cobbler pin 16 (GPIO23)
# SWITCH_PIN  = 27    # cobbler pin 7  (GPIO27)
GPIO_LIST = {"RED_LED": 18, "GRN_LED": 13, "BLU_LED": 23,"SWITCH_PIN": 27}

class PiGpio(object):
    """Raspberry Pi Internet 'IoT GPIO'."""
    def __init__(self):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(GPIO_LIST["RED_LED"], GPIO.OUT)      # RED LED as output
        GPIO.setup(GPIO_LIST["GRN_LED"], GPIO.OUT)      # GRN LED as output
        GPIO.setup(GPIO_LIST["BLU_LED"], GPIO.OUT)      # BLU LED as output
        GPIO.setup(GPIO_LIST["SWITCH_PIN"], GPIO.IN)     # Switch as input w/pu
        GPIO.setup(GPIO_LIST["SWITCH_PIN"], GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def read_switch(self):
        """Read the switch state."""
        switch = GPIO.input(GPIO_LIST["SWITCH_PIN"])
        # invert because of active low momentary switch
        if (switch == 0):
            switch=1
        else:
            switch=0
        return switch

    # set the particular LED to ON or OFF
    def set_led(self, led, value):
        """Change the LED to the passed in value, '1 ON or '0' OFF."""
        if(led == 1):
            GPIO.output(GPIO_LIST["RED_LED"], value)
        if(led == 2):
            GPIO.output(GPIO_LIST["GRN_LED"], value)
        if(led == 3):
            GPIO.output(GPIO_LIST["BLU_LED"], value)

    # get the state of an LED
    def get_led(self, led):
        """Return the state value of the LED, '1' ON or '0' OFF."""
        if(led == 1):
            return GPIO.input(GPIO_LIST["RED_LED"])
        if(led == 2):
            return GPIO.input(GPIO_LIST["GRN_LED"])
        if(led == 3):
            return GPIO.input(GPIO_LIST["BLU_LED"])
