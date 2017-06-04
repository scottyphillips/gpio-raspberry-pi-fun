#!/usr/bin/python
import RPi.GPIO as GPIO
import time, sys, os
import RPIO
from RPIO import PWM

def redirect_stdout():
    sys.stdout.flush() # <--- important when redirecting to files
    newstdout = os.dup(1)
    devnull = os.open(os.devnull, os.O_WRONLY)
    os.dup2(devnull, 1)
    os.close(devnull)
    sys.stdout = os.fdopen(newstdout, 'w')

GPIO.setmode(GPIO.BCM)
RPIO.setwarnings(False)
PWM.set_loglevel(PWM.LOG_LEVEL_ERRORS)
PWM.setup()
p0 = 17
p1 = 18
p2 = 27
p3 = 22
p4 = 23
p5 = 24
timer = 0.5
servo_position = 1500
exitProgram = 0
redirect_stdout()
print("Setting up Servo..")
servo = PWM.Servo()
GPIO.setup(p0, GPIO.OUT)
#GPIO.setup(p1, GPIO.OUT)
GPIO.setup(p4, GPIO.OUT)
GPIO.setup(p2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(p3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(p5, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
#pwm=GPIO.PWM(p1,50)
#pwm.start(7.5)

servo.set_servo(p1, servo_position)
def light(value1, value2 ):
  GPIO.output(value1, GPIO.LOW)
  GPIO.output(value2, GPIO.HIGH)



def button1(channel):
   print ("Button 1 Pressed!")
   global timer
   global servo
   global servo_position
   if (timer == 0.12):
      timer = 0.5
   else:
      timer = 0.12
   if(servo_position >= 1000):
      servo_position -= 100
      servo.set_servo(p1, servo_position) 

def button2(channel):
   global exitProgram
   exitProgram = 1

def button3(channel):
   global servo_position
   print("Button 3 Pressed!")
   if(servo_position <= 2000):
      while (GPIO.input(p5) == True and servo_position < 2000):
        time.sleep(0.05)
        servo_position += 10
        servo.set_servo(p1, servo_position)

GPIO.add_event_detect(p2, 
 GPIO.RISING, callback=button1, bouncetime=300)
GPIO.add_event_detect(p3,
 GPIO.RISING, callback=button2, bouncetime=300)
GPIO.add_event_detect(p5,
 GPIO.RISING, callback=button3, bouncetime=300)


while(exitProgram == 0):
   light(p0, p4)
   time.sleep(timer)  
   light(p4, p0)
   time.sleep(timer)
GPIO.cleanup()
sys.exit("Button 2 Pressed. Exiting Program")


