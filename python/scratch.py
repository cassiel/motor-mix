import mido
import time

def f(msg):
    print(msg)

with mido.open_input("Arturia KeyStep 32", callback=f) as p:
    while True:
        print("TICK")
        time.sleep(1)
