from RPi import GPIO


class TB6612FNG(object):
    def __init__(self, pinout=None):
        '''
        Constructor

        Parameters
        ----------
        pinout : dict
            Dict containing RPi pin numbers (in BCM nomenclature) corresponding
            to each of the inputs on the TB6612FNG.

        Returns
        -------
        None
        '''
        if pinout is None:
            self.pinout = {'PWMA': 18,
                           'AI1':  27,
                           'AI2':  22,
                           'STBY': 17}
        else:
            if set(pinout.keys()) != {'STBY', 'AI2', 'PWMA', 'AI1'}:
                raise ValueError('Pinout does not contain correct pin names.')
            self.pinout = pinout
        
        GPIO.setmode(GPIO.BCM)
        for pinname in self.pinout:
            GPIO.setup(self.pinout[pinname], GPIO.OUT, initial=0)
        self.pwm = GPIO.PWM(self.pinout['PWMA'], 200)
        self.direction = 'CW'
        
    def power_on(self, dutycycle):
        '''
        Turn on the output voltage at a given PWM modulation. Note that the
        PWM is handled through the python RPi.GPIO module which only does PWM
        at the software level; thus, you should not expect excellent frequency
        stability. The PWM is operated at 200 Hz.

        Parameters
        ----------
        dutycycle : float
            Duty cycle % (0 to 100) of the pulse-width modulation.

        Returns
        -------
        None
        '''
        # check that the output pins match the software direction
        self.set_direction(self.direction)
        GPIO.output(self.pinout['STBY'], GPIO.HIGH)
        self.pwm.start(dutycycle)

    def power_off(self):
        '''
        Turn off the output voltage.

        Parameters
        ----------
        None

        Returns
        -------
        None
        '''
        GPIO.output(self.pinout['AI1'], GPIO.LOW)
        GPIO.output(self.pinout['AI2'], GPIO.LOW)
        self.pwm.stop()
        
    def set_pwm(self, dutycycle):
        '''
        Set the PWM duty cycle. Note that the PWM is handled through the python
        RPi.GPIO module which only does PWM at the software level; thus, you
        should not expect excellent frequency stability. The PWM is operated
        at 200 Hz.
        
        Parameters
        ----------
        dutycycle : float
            Duty cycle % (0 to 100) of the pulse-width modulation.

        Returns
        -------
        None
        '''
        self.pwm.ChangeDutyCycle(dutycycle)

    def set_direction(self, direction):
        '''
        Set the direction (polarity) of the output voltage.

        Parameters
        ----------
        direction : str
            Direction (polarity) of output voltage. Options are specified as
            as either of the strings "CW" or "CCW", according to the
            nomeclature of the IC datasheet.

        Returns
        -------
        None
        '''
        if direction is 'CW':
            GPIO.output(self.pinout['AI1'], GPIO.HIGH)
            GPIO.output(self.pinout['AI2'], GPIO.LOW)
        elif direction is 'CCW':
            GPIO.output(self.pinout['AI1'], GPIO.LOW)
            GPIO.output(self.pinout['AI2'], GPIO.HIGH)
        else:
            raise ValueError('Argument `direction` must be string "CW" or "CCW".')

        self.direction = direction
        
