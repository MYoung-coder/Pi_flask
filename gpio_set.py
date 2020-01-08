import RPi.GPIO  as GPIO
import time

gpio_tuple = (38, 29, 31, 32, 33, 35, 36, 40)


def gpio_model():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)
    GPIO.setup(gpio_tuple, GPIO.OUT)
    GPIO.output(gpio_tuple, GPIO.HIGH)
    # GPIO.setup(gpio_tuple, GPIO.IN)


def liushuideng():
    gpio_model()
    GPIO.output(gpio_tuple[0], GPIO.LOW)  # ON 3s
    time.sleep(3)
    GPIO.output(gpio_tuple[1], GPIO.LOW)  # ON 3s
    time.sleep(3)
    GPIO.output(gpio_tuple[2], GPIO.LOW)  # ON 3s
    time.sleep(3)
    GPIO.output(gpio_tuple[3], GPIO.LOW)  # ON 3s
    time.sleep(3)
    GPIO.output(gpio_tuple[4], GPIO.LOW)  # ON 3s
    time.sleep(3)
    GPIO.output(gpio_tuple[5], GPIO.LOW)  # ON 3s
    time.sleep(3)
    GPIO.output(gpio_tuple[6], GPIO.LOW)  # ON 3s
    time.sleep(3)
    GPIO.output(gpio_tuple[7], GPIO.LOW)  # ON 3s
    time.sleep(3)
    GPIO.output(gpio_tuple, GPIO.HIGH)  # OFF
    time.sleep(3)
#
# if __name__ == '__main__':
#     while True:
#         liushuideng()

