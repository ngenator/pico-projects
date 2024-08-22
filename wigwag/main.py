import asyncio

from asyncio import Event, Task
from machine import Pin, ADC


class Slider:
    minimum: int
    maximum: int

    pin: ADC

    def __init__(self, pin: int, minimum: int = 1000, maximum: int = 5000):
        self.minimum = minimum
        self.maximum = maximum
        self.pin = ADC(Pin(pin))

    def value(self) -> int:
        return int(self.pin.read_u16() / 65535 * (self.maximum - self.minimum) + self.minimum)

    
class WigWag:
    enable: Event

    relay: Pin
    switch: Pin

    on_slider: Slider
    off_slider: Slider

    watch_task: Task
    run_task: Task

    def __init__(self, relay_pin: int, switch_pin: int, on_slider: Slider, off_slider: Slider):
        self.enable = Event()

        self.relay = Pin(relay_pin, Pin.OUT)
        self.switch = Pin(switch_pin, Pin.IN, Pin.PULL_UP)

        self.on_slider = on_slider
        self.off_slider = off_slider

    def start(self):
        self.watch_task = asyncio.create_task(self._watch())
        self.run_task = asyncio.create_task(self._run())

    def stop(self):
        self.watch_task.cancel()
        self.run_task.cancel()
        self.enable.clear()

    async def _watch(self):
        while True:
            if self.switch.value():
                self.enable.set()
            else:
                self.enable.clear()
            await asyncio.sleep_ms(100)

    async def _run(self):
        while True:
            await self.enable.wait()
            self.relay.on()
            await asyncio.sleep_ms(self.on_slider.value())
            self.relay.off()
            await asyncio.sleep(0)
            if self.enable.is_set():
                await asyncio.sleep_ms(self.off_slider.value())

async def main():
    on_slider = Slider(28)
    off_slider = Slider(27)

    w = WigWag(15, 14, on_slider, off_slider)

    w.start()

    while True:
        await asyncio.sleep_ms(100)

asyncio.run(main())