from RPi import GPIO

pinout = {'PWMA': 18,
          'AI1':  27,
          'AI2':  22,
          'STBY': 17}

class TB6612FNG(object):
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        for pinname in pinout:
            GPIO.setup(pinout[pinname], GPIO.OUT, initial=0)
        self.pwm = GPIO.PWM(pinout['PWMA'], 200)
        self.direction = 'CW'
        
    def power_on(self, dutycycle):
        # check that the output pins match the software direction
        self.set_direction(self.direction)
        GPIO.output(pinout['STBY'], GPIO.HIGH)
        self.pwm.start(dutycycle)

    def power_off(self):
        GPIO.output(pinout['AI1'], GPIO.LOW)
        GPIO.output(pinout['AI2'], GPIO.LOW)
        self.pwm.stop()
        
    def set_pwm(self, dutycycle):
        self.pwm.ChangeDutyCycle(dutycycle)

    def set_direction(self, direction):
        if direction is 'CW':
            GPIO.output(pinout['AI1'], GPIO.HIGH)
            GPIO.output(pinout['AI2'], GPIO.LOW)
        elif direction is 'CCW':
            GPIO.output(pinout['AI1'], GPIO.LOW)
            GPIO.output(pinout['AI2'], GPIO.HIGH)
        else:
            raise ValueError('Argument `direction` must be string "CW" or "CCW".')

        self.direction = direction
        
