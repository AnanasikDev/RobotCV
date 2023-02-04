# from gpiozero import TonalBuzzer
# from gpiozero.tones import Tone
# from time import sleep
# b = TonalBuzzer(17, initial_value=-1)
# print(b)
# b.play(Tone("A4"))
# b.play(Tone(220.0)) # Hz
# # b.play(Tone(60)) # middle C in MIDI notation
# b.play("A4")
# b.play(220.0)
# # b.play(60)
# sleep(1)

from gpiozero import OutputDevice
from time import sleep

buzzer = OutputDevice(18)

while True:
    buzzer.on()
    sleep(0.35)
    buzzer.off()
    sleep(0.2)
    print("A")
