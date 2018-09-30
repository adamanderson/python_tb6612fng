# python_tb6612fng
Python driver for the TB6612FNG on Raspberry Pi. Currently requires python3 and tested on Raspberry Pi 3.

# Setup Notes
Use should be self-explanatory from docstrings. Note that the driver is currently only configured to use one of the two outputs of the TB6612FNG. In addition, the driver uses the software PWM of the `RPi.GPIO` module, which obviously does not provide very good frequency stability. As far as I am aware, there is no native way to use the hardware PWM functionality of the Broadcom SOC. The software PWM seems to provide acceptable performance for the control of most motors, which have enough inertia that frequency stability of the PWM is not crucial for many applications.
