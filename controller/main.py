import time

import ssd1306

from machine import Pin, I2C
from rotary_irq import RotaryIRQ

i2c = I2C(1, scl=Pin(27), sda=Pin(26))

display = ssd1306.SSD1306_I2C(128, 32, i2c)

sw = Pin(12, Pin.IN, Pin.PULL_UP) # the switch on the rotary encoder

r = RotaryIRQ(
    pin_num_clk=10, 
    pin_num_dt=11, 
    min_val=0, 
    max_val=10, 
    reverse=True, 
    range_mode=RotaryIRQ.RANGE_BOUNDED,
)

def update_display():
    display.fill(0) # clear the screen
    display.text(f"Enabled: {sw.value()}", 0, 0)
    display.text(f"Power: {r.value()}", 0, 8)
    display.show()

def main():
    display.text("Hello, Wokwi!", 0, 16)
    display.show()

    prev = r.value()
    while True:
        curr = r.value()
        
        if prev != curr:
            prev = curr
            update_display()

        time.sleep(50)

main()