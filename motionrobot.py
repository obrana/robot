import RPi.GPIO as GPIO
import time


GPIO.setmode(GPIO.BCM)
TRIG = 23
ECHO = 24
cPins = [4,14,15,18]
cPin2 = [4,16,20,21]

print "Distance Measurement In Progress"

GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)
GPIO.output(TRIG, False)
for pin in cPins:
        GPIO.setup(pin,GPIO.OUT)
        GPIO.output(pin,0)

for pin in cPin2:
        GPIO.setup(pin,GPIO.OUT)
        GPIO.output(pin,0)

seq =   [ [1,0,0,0],
          [1,1,0,0],
          [0,1,0,0],
          [0,1,1,0],
          [0,0,1,0],
          [0,0,1,1],
          [0,0,0,1],
          [1,0,0,1]  ]

seq2=   [ [1,0,0,1],
          [0,0,0,1],
          [0,0,1,1],
          [0,0,1,0],
          [0,1,1,0],
          [0,1,0,0],
          [1,1,0,0],
          [1,0,0,0] ]

print "Waiting For Sensor To Settle"

time.sleep(2)
i = 0
avgDistance=0


while(True):
    GPIO.output(TRIG, True)
    time.sleep(0.001)

    GPIO.output(TRIG, False)
    while GPIO.input(ECHO)==0:
      pulse_start = time.time()

    while GPIO.input(ECHO)==1:
      pulse_end = time.time()    

    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150
    distance = round(distance, 2)
    avgDistance = avgDistance+distance
   
    if distance >=10:
           print "distance:", distance,"cm"
  	   for i in range (512):
                for hstep in range (8):
                        for pin in range(4):
                                GPIO.output(cPins[pin], seq[hstep][pin])
                                GPIO.output(cPin2[pin], seq2[hstep][pin])
                        time.sleep(0.001)  
 
    elif 5 < distance < 10 :
     print "Distance:",distance,"cm"
     time.sleep(1)
     for i in range (512):
	for hstep in range(8):
		for pin in range(4):
			GPIO.output(cPins[pin], seq[hstep][pin])
			time.sleep(0.001)
    else:
     print "Distance is to near:", distance,"cm"
     time.sleep(1)

GPIO.cleanup()
