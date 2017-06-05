#!/usr/bin/python

# This is just a stupid little python script to exercise the Raspberry Pi
# This program is designed specifically to run on RPi series 1 model B since
# thats what I own. Schematic for the useless thingy i built might come later.
import RPi.GPIO as GPIO
import time, sys, os
import RPIO
from RPIO import PWM

# Global variables
# P0 to P5 corresponds to the labelling on my RPi cobbler.
p0 = 17 # GPIO 17
p1 = 18
p2 = 27
p3 = 22
p4 = 23
p5 = 24
timer_slow = 0.5
timer_fast = 0.12
timer = timer_slow
init_servo_pos = 1500
max_servo_pos = 2000
min_servo_pos = 1000
servo_pos = init_servo_pos
exitProgram = 0

# functions
# redirtect_stdout is mainly used to hide some output from RPIO.
def redirect_stdout():
    sys.stdout.flush() # <--- important when redirecting to files
    newstdout = os.dup(1)
    devnull = os.open(os.devnull, os.O_WRONLY)
    os.dup2(devnull, 1)
    os.close(devnull)
    sys.stdout = os.fdopen(newstdout, 'w')

# light is simply used to flash two lights onn and off.
def light(value1, value2 ):
  GPIO.output(value1, GPIO.LOW)
  GPIO.output(value2, GPIO.HIGH)

# switchTimer is used to change the flashing of the lights.
def switchTimer(value):
  if (value == timer_fast):
     value = timer_slow
  else:
     value = timer_fast
  return value

# servoClockwise is used to allow a fixed adjustment of the servo.
def servoClockwise(inc):
  global servo_pos
  global servo
  if(servo_pos >= min_servo_pos ):
    servo_pos -= inc
    servo.set_servo(p1, servo_pos)

# servoAntiClocwise allows a user to hold down the button to rotate
def serverAntiClockwise(inc):
  global servo_pos
  global servo
  # allow user to hold down button to rotate servo.
  if(servo_pos <= max_servo_pos ):
     while (GPIO.input(p5) == True and servo_pos < max_servo_pos ):
       time.sleep(0.05)
       servo_pos+= inc
       servo.set_servo(p1, servo_pos)

# Used in conjunction with the listeners
def button1(channel):
   global timer
   print ("Button 1 Pressed!")
   timer = switchTimer(timer)
   servoClockwise(100)

def button2(channel):
   global exitProgram
   print ("Button 2 Pressed!")
   exitProgram = 1

def button3(channel):
   print("Button 3 Pressed!")
   serverAntiClockwise(10)

def myExit():
   RPIO.cleanup()
   GPIO.cleanup()
   sys.exit("Exiting Program")

# initialisation
try:
    GPIO.setmode(GPIO.BCM)
    RPIO.setwarnings(False)
    PWM.set_loglevel(PWM.LOG_LEVEL_ERRORS)
    PWM.setup()
    redirect_stdout()
    print("Setting up Servo..")
    servo = PWM.Servo()

    # P0 and P4 are for the LEDs.
    GPIO.setup(p0, GPIO.OUT)
    GPIO.setup(p4, GPIO.OUT)

    # P2, P3 and P5 are for the buttons
    GPIO.setup(p2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(p3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(p5, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    # P1 is the PWM signal for the servo.
    servo.set_servo(p1, servo_position)

    # add listeners.
    GPIO.add_event_detect(p2,
     GPIO.RISING, callback=button1, bouncetime=300)
    GPIO.add_event_detect(p3,
     GPIO.RISING, callback=button2, bouncetime=300)
    GPIO.add_event_detect(p5,
     GPIO.RISING, callback=button3, bouncetime=300)

    # main program loop
    while(exitProgram == 0):
       light(p0, p4)
       time.sleep(timer)
       light(p4, p0)
       time.sleep(timer)

# Catch lazy people who press control C like me.
except KeyboardInterrupt:
   myExit()
myExit()
