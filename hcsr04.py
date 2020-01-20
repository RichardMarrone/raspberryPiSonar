import RPi.GPIO as GPIO
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from itertools import cycle
import time
import math

def init():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(18, GPIO.OUT)#Trigger Pin
    GPIO.setup(22,GPIO.IN)#Echo Pin
    GPIO.setup(11, GPIO.OUT)#PWM Pin for servo
    

def get_distance():
    time.sleep(0.2)#allow sensor to settle on repeat calls
    GPIO.output(18, True)
    time.sleep(0.00001)
    GPIO.output(18, False)
    start = time.time()

    while GPIO.input(22) == 0:
        start = time.time()
    

    while GPIO.input(22) == 1:
        end = time.time()
    

    duration = end - start

    d = (duration / 2) * 34300
    d = round(d, 2)
    time.sleep(0.05)
    return d

def plot_data_testing(i,pos,dist): 
    r = get_distance()
    #ignore objects beyond 50cm
    if r > 50:
        r = None
        
    theta = (next(x) * math.pi / 180) * 7.2
    pos.append(theta)
    dist.append(r)

    pos = pos[-25:]
    dist = dist[-25:]
    
    ax1.clear()
    plt.plot(pos,dist, 'o')
    
    move_servo()
    
        
def move_servo():
    #values of dc found to be
    #2.15= 0 deg
    #6.5 = 90 deg
    #12.45 = 180 deg

    #decremeneting by 0.412 gives 25 equal "steps"
    global dc
    if dc > 2.15:
        p.ChangeDutyCycle(dc)
        dc = dc - 0.412
    else:
        dc = 12.45
    

def cleanup():
    p.stop()
    GPIO.cleanup()
    print('cleaning up and quitting')
    quit()

init()
#setup figure to plot
fig = plt.figure()
ax1 = fig.add_subplot(1,1,1,projection='polar')

#lists to store data points
pos = []
dist = []

#position iterator for the animation func (25 increments)
x = cycle([x for x in range(25,0,-1)])

#setup PWM for servo. Pin 11, 50Hz
p = GPIO.PWM(11, 50)

#set inital duty cycle and start PWM
dc = 12.45
p.start(dc)


#figure animation loop to call plot_data every 0.10 second
ani = animation.FuncAnimation(fig, plot_data_testing,fargs=(pos,dist), interval=100)
plt.show()

cleanup()
