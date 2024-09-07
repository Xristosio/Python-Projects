import RPi.GPIO as GPIO                                         #Βιβλιοθήκες
from evdev import InputDevice                                   #RPi.GPIO, evdev

Aristera_mprosta = 17 
Deksia_pisw = 18                                                #Ορισμός Pin
Deksia_mprosta = 22
Aristera_pisw = 23

GPIO.setmode(GPIO.BCM)                                          #Ορισμός αρίθμισης των pin
GPIO.setwarnings(False)

GPIO.setup(Deksia_mprosta, GPIO.OUT)
GPIO.setup(Aristera_pisw, GPIO.OUT)                             #Δήλωση της συμπεριφοράς των Pin
GPIO.setup(Aristera_mprosta, GPIO.OUT)
GPIO.setup(Deksia_pisw, GPIO.OUT)

GPIO.output(Deksia_mprosta, GPIO.LOW)
GPIO.output(Aristera_pisw, GPIO.LOW)                            #Αρχικοποίηση ώστε τα pins να μην έχουν ρεύμα
GPIO.output(Aristera_mprosta, GPIO.LOW)
GPIO.output(Deksia_pisw, GPIO.LOW)

def control_motors(kinisi,timi):
    if kinisi == 304 and timi == 1:
        GPIO.output(Deksia_mprosta, GPIO.HIGH)
        GPIO.output(Aristera_pisw, GPIO.LOW)
        GPIO.output(Aristera_mprosta, GPIO.HIGH)
        GPIO.output(Deksia_pisw, GPIO.LOW)
    elif kinisi == 307 and timi == 1:
        GPIO.output(Deksia_mprosta, GPIO.LOW)
        GPIO.output(Aristera_pisw, GPIO.HIGH)
        GPIO.output(Aristera_mprosta, GPIO.LOW)
        GPIO.output(Deksia_pisw, GPIO.HIGH)
    elif kinisi == 16 and timi==-1:
        GPIO.output(Deksia_mprosta, GPIO.HIGH)
        GPIO.output(Aristera_pisw, GPIO.HIGH)
        GPIO.output(Aristera_mprosta, GPIO.LOW)
        GPIO.output(Deksia_pisw, GPIO.LOW)
    elif kinisi == 16 and timi== 1:
        GPIO.output(Deksia_mprosta, GPIO.LOW)
        GPIO.output(Aristera_pisw, GPIO.LOW)
        GPIO.output(Aristera_mprosta, GPIO.HIGH)
        GPIO.output(Deksia_pisw, GPIO.HIGH)
    elif kinisi == 305:
        GPIO.output(Deksia_mprosta, GPIO.LOW)
        GPIO.output(Aristera_pisw, GPIO.LOW)
        GPIO.output(Aristera_mprosta, GPIO.LOW)
        GPIO.output(Deksia_pisw, GPIO.LOW)

def main():
    while True:     # Επανάληψη ώστε να δουλεύει μόνιμα
        try:
            dev = InputDevice('/dev/input/event1') # Σύνδεση συσκευής
            print("Περιμένω εισόδους από το χειριστήριο...")
            for event in dev.read_loop():           # Λήψη του κάθε event
                print(event)
                kinisi=event.code
                timi=event.value
                control_motors(kinisi,timi)         # Εκτέλεση συνάρτησης
        except Error:
            # Εάν ο μοχλός αποσυνδεθεί, περιμένουμε ξανά την επανασύνδεση
            GPIO.output(Deksia_mprosta, GPIO.LOW)
            GPIO.output(Aristera_pisw, GPIO.LOW)
            GPIO.output(Aristera_mprosta, GPIO.LOW)
            GPIO.output(Deksia_pisw, GPIO.LOW)
            print("Περιμένω επανασύνδεση του μοχλού...")
            while True:
                try:
                    dev = InputDevice('/dev/input/event1')
                    print("Ο μοχλός συνδέθηκε ξανά")
                    break
                except Error:
                    pass

if __name__ == "__main__":
    main()