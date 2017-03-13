#!/usr/bin/python
import time
import pprint
import datetime
from GPIO import PiGpio
from stepper import PiStepper
from bmp280 import PiBMP280
from pwm import PiPwm
from flask import *
app = Flask(__name__)

PWM0 = 0
PWM1 = 1
led_green = 1

# Create a instance of GPIO
pi_gpio = PiGpio()

# Create a stepper motor controller object
pi_smc = PiStepper()

#Create a instance of PWM
pi_pwm = PiPwm()

# initializing pwm 0
pwm_red = pi_pwm.start_pwm(PWM0,100,50)
# pi_pwm.stop_pwm(pwm_red)
# initializing pwm 1
pwm_green = pi_pwm.start_pwm(PWM1,100,50)
# pi_pwm.stop_pwm(pwm_green)

# create a pi bmp280 sensor object and data structure
env_sensor = {'name' : 'bmp280', 'addr' : 0x76, 'chip' : PiBMP280(0x76) , 'data' : {}}
# import pdb; pdb.set_trace()

## function to read environmental parameters
def get_env_sensors():
    # Read the Sensor ID for 0x76 -> values into the ['data'] dictionary
    (chip_id, chip_version) = env_sensor['chip'].readBMP280ID()
    env_sensor['data']['chip_id'] = chip_id
    env_sensor['data']['chip_version'] = chip_version

    # Read the Sensor Temp/Pressure values into the ['data'] dictionary
    (temperature, pressure) = env_sensor['chip'].readBMP280All()
    env_sensor['data']['temperature'] = { 'reading': temperature, 'units' : 'C' }
    env_sensor['data']['pressure'] = { 'reading': pressure, 'units' : 'hPa' }
    return env_sensor['data']

@app.route("/")
def index():
    return render_template('index.html')
# ============================== API Routes ===================================
# ============================= POST: /motor/<state> ============================
# get sensor values methods from curl for example
# curl http://iot6041:5000/sensors
# -----------------------------------------------------------------------------
@app.route("/sensors", methods=['GET'])
def sensors():
    # return "Sensors" + str(get_env_sensors()) + "\n"
    # pprint.pprint(get_env_sensors())
    return "Sensors" + "\n"

# ============================ GET: /leds/<state> =============================
# read the LED status by GET method from curl for example
# curl http://iot8e3c:5000/leds/1
# curl http://iot8e3c:5000/leds/2
# curl http://iot8e3c:5000/leds/3
# -----------------------------------------------------------------------------
@app.route("/leds/<int:led_state>", methods=['GET'])
def leds(led_state):
  return "LED State:" + str(pi_gpio.get_led(led_state)) + "\n"

# ======================= POST: /ledcmd/<data> =========================
# set the LED state by POST method from curl. For example:
# curl --data 'led=1&state=ON' http://iot8e3c:5000/ledcmd
# -----------------------------------------------------------------------------
@app.route("/ledcmd", methods=['POST'])
def ledcommand():
    cmd_data = request.data
    print "LED Command:" + cmd_data
    led = int(str(request.form['led']))
    state = str(request.form['state'])
    if(state == 'OFF'):
        pi_gpio.set_led(led,False)
    elif (state == 'ON'):
        pi_gpio.set_led(led,True)
    else:
        return "Argument Error"

    return "Led State Command:" + state + " for LED number:"+ str(led) + "\n"
#===========GET: /pwm_green/<int:duty_cycle>====================================
# Set the led_green by GET method from curl
# curl http://iot6041:5000/led_green/50
#-------------------------------------------------------------------------------
@app.route("/led_green/<int:duty_cycle>", methods=['GET'])
def set_led_green(duty_cycle):
    pi_pwm.change_duty_cycle(pwm_green, duty_cycle)
    return "LED GREEN" + str(duty_cycle) + "\n"

#===========GET: /pwm_red<int:duty_cycle>====================================
# Set the pwm_green by GET method from curl
# curl http://iot6041:5000/pwm_green/50
#-------------------------------------------------------------------------------
@app.route("/led_red/<int:duty_cycle>", methods=['GET'])
def set_led_red(duty_cycle):
    pi_pwm.change_duty_cycle(pwm_red, duty_cycle)
    return "LED RED" + str(duty_cycle) + "\n"

# ============================= POST: /motor/<state> ============================
# control motor by POST methods from curl for example
# curl http://iot6041:5000/motor/0
# curl http://iot6041:5000/motor/1
# -----------------------------------------------------------------------------
@app.route("/motor/<int:motor_state>", methods=['GET'])
def motor(motor_state):
    if motor_state == 0:    # stop
        pi_smc.stop()
    elif motor_state == 1:      # start
        pi_smc.start()
    else:
        return ('Unknown Stepper Motor state!', 400)
    return ('', 204)


# ====================== GET: /motor_speed/<speed_rpm> ========================
# set the motor speed in RPM by GET method from curl. For example:
# curl http://iot6041:5000/motor_speed/60
# -----------------------------------------------------------------------------
@app.route("/motor_speed/<int:motor_speed>", methods=['GET'])
def set_motor_speed(motor_speed):
    pi_smc.setSpeed(motor_speed)
    return "Set Motor Speed : " + str(pi_smc.getSpeed()) + "\n"

# ===================== GET: /motor_direction/<direction> =====================
# set the motor direction (CW/CCW) by GET method from curl. For example:
# curl http://iot6041:5000/motor_direction/1
# -----------------------------------------------------------------------------
@app.route("/motor_zero", methods=['GET'])
def set_motor_zero():
    pi_smc.setPosition(0)
    return "Set Motor Position : " + str(pi_smc.getPosition()) + "\n"

# ===================== GET: /motor_direction/<direction> =====================
# set the motor direction (CW/CCW) by GET method from curl. For example:
# curl http://iot6041:5000/motor_direction/1
# -----------------------------------------------------------------------------
@app.route("/motor_direction/<string:direction>", methods=['GET'])
def set_motor_dir(direction):
    pi_smc.setDirection(direction)
    return "Set Motor Direction : " + str(pi_smc.getDirection()) + "\n"

# ===================== GET: /motor_steps/<steps> =====================
# set the motor steps (int) by HTTP GET method  CURL example:
# curl http://iot6041:5000/motor_steps/100
# -----------------------------------------------------------------------------
@app.route("/motor_steps/<int:steps>", methods=['GET'])
def set_motor_steps(steps):
    pi_smc.setSteps(steps)
    return "Set Motor Steps : " + str(pi_smc.getSteps()) + "\n"

# ====================== GET: /motor_position/<position> ======================
# set the motor position by HTTP GET method. CURL example:
# curl http://iot6041:5000/motor_position/1
# -----------------------------------------------------------------------------
@app.route("/motor_position/<int:position>", methods=['GET'])
def set_motor_pos(position):
    pi_smc.setDirection(direction)
    return "Set Motor Direction : " + str(pi_smc.getDirection()) + "\n"


# ======================= POST: /motor_multistep/<dir> =========================
# set the motor multistep by POST method from curl. For example:
# curl --data 'steps=10&direction=CW' http://iot6041:5000/motor_multistep
# -----------------------------------------------------------------------------
@app.route("/motor_multistep", methods=['POST'])
def postMotorMultistep():
    ctrl_data = request.data
    print "Motor Control Data:" + ctrl_data
    direction = str(request.form['direction'])
    if (direction == 'CW'):
        pi_smc.setDirection(1)
    elif (direction == 'CCW'):      # start
        pi_smc.setDirection(0)
    else:
        return ('Unknown Stepper Motor Direction!', 400)

    steps = str(request.form['steps'])
    pi_smc.step(int(steps))
    return "Motor Multisteps Steps:" + steps + " Direction:"+ direction + "\n"

# curl --data 'mykey=FOOBAR' http://0.0.0.0:5000/createHello
# echo 'mykey={"name":"Carrie Fisher","age":"60"}' | curl -d @- http://0.0.0.0:5000/createHello
@app.route('/test', methods = ['POST'])
def postRequestTest():
    mydata = request.data

    # import pdb; pdb.set_trace()
    return "Hello API Server : You sent a "+ request.method + \
            " message on route path " + request.path + \
            " \n\tData:" +  data + "\n"


# ============================ END API Routes =================================

# ============================= Run App Server ================================
# =========================== Endpoint: /myData ===============================
# read the sensor values by GET method from curl for example
# curl http://iot6041:5000/myData
# -----------------------------------------------------------------------------
@app.route('/myData')
def myData():
    def get_values():
        while True:
            # return the yield results on each loop, but never exits while loop
            data_obj = {'environmental' : get_env_sensors(),
                        'motor' : { 'position':str(pi_smc.getPosition()),
                                    'state':str(pi_smc.getState()) },
                        'timestamp' : datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        'led_states' : {'led_red' : pi_gpio.get_led(1),
                                        'led_grn' : pi_gpio.get_led(2),
                                        'led_blu' : pi_gpio.get_led(3)}
            }

            yield('data: {0}\n\n'.format(data_obj))
            time.sleep(2.0)
    return Response(get_values(), mimetype='text/event-stream')
# ============================== API Routes ===================================

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, threaded=True)
# =============================================================================
