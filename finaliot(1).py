import sys
from time import sleep
import signal
from gpiozero import LED, Button
from threading import Thread
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import datetime

LED = LED(17)
BUTTON = Button(27)
#state=0


PAHT_CRED = '/home/pi/Desktop/key.json'
URL_DB = 'https://pyrebasetest-92dd3.firebaseio.com/'

REF_HOME = 'home' #Coding after  it will be id.

REF_LED = 'led' #led
REF_DLED = 'd_led'
REF_LED_ON='led_on'
REF_LED_OFF='led_off'

REF_BUTTON = 'button'#led
REF_DBUTTON = 'd_button'

REF_TIME ='time'
REF_NTIME='n_time'


dt=datetime.datetime.now()

i_day=dt.day


REF_DEEP='deep'


class IOT():

    def __init__(self):
        cred = credentials.Certificate(PAHT_CRED)
        firebase_admin.initialize_app(cred, {
            'databaseURL': URL_DB
        })

        self.refHome = db.reference(REF_HOME) 

        self.refLed = self.refHome.child(REF_LED)
        self.refDled = self.refLed.child(REF_DLED)

        self.refLon=self.refLed.child(REF_LED_ON)
        self.refLoff=self.refLed.child(REF_LED_OFF)

        self.refButton = self.refHome.child(REF_BUTTON)
        self.refDbutton = self.refButton.child(REF_DBUTTON)

        self.refTime = self.refHome.child(REF_TIME)
        self.refNtime = self.refTime.child(REF_NTIME)
 
        self.refdeep=self.refHome.child(REF_DEEP)
        self.refdeep_s=self.refHome.child('deep_state')

        self.refHome.update({'deep':{'12':{'120249':{'day':i_day,'hour':02,'minute':49,'deep_num':0,'state':1}}}})
     

    def ledControlGPIO(self, getdb):

        dt1=datetime.datetime.now()

        if getdb:
            LED.on()
            self.refDbutton.set(True)
            self.refLon.push(dt1.strftime('%d day %H h %M m'))
            print('LED ON')

        else:
            LED.off()
            self.refDbutton.set(False)
            self.refLoff.push(dt1.strftime('%d day %H h %M m'))
            print('LED OFF')


    def ledStart(self):

        E, i = [], 0

        d_led_g = self.refDled.get()
        self.ledControlGPIO(d_led_g)
        E.append(d_led_g)

        while True:
          d_led_g = self.refDled.get()#led_db get
          E.append(d_led_g)
        
          if E[i] != E[-1]:
              self.ledControlGPIO(d_led_g)
          del E[0]
          i = i + i
          sleep(0.4)

    def deepStart(self):
        while True:
         dte=datetime.datetime.now()

         today=dte.strftime('%d')
         REF_TODAY=today
         self.reftoday=self.refdeep.child(REF_TODAY)

         t_total=dte.strftime('%d%H%M')
         REF_T_TOTAL=t_total
         self.refttotal=self.reftoday.child(REF_T_TOTAL)

         if(self.refttotal.get()!=None and self.refdeep_s.get()==True):
          deep_num=self.refttotal.child('deep_num').get()
          deep_day=self.refttotal.child('day').get()
          deep_hour=self.refttotal.child('hour').get()
          deep_minute=self.refttotal.child('minute').get()
          deepl_state=self.refttotal.child('state').get()
          today8am=dte.replace(day=deep_day,hour=deep_hour,minute=deep_minute)
          if(deep_num==0):
           self.refttotal.child('deep_num').set(1)
           if(deepl_state==1):
            self.refDled.set(True)
           else:
            self.refDled.set(False)
        sleep(1)

    def button_on(self):
        if self.refDled.get()==False:
         print('Button On')
         self.refDled.set(True)
         self.refDbutton.set(True)
        else:
         print('Button OFF')
         self.refDled.set(False)
         self.refDbutton.set(False)

    def buttonStart(self):
        print('Start btn !')
        BUTTON.when_pressed = self.button_on

print ('START !')
iot = IOT()

subproceso_led = Thread(target=iot.ledStart)
subproceso_led.daemon = True
subproceso_led.start()

subproceso_btn = Thread(target=iot.buttonStart)
subproceso_btn.daemon = True
subproceso_btn.start()


subproceso_deep = Thread(target=iot.deepStart)
subproceso_deep.daemon=True
subproceso_deep.start()

signal.pause()