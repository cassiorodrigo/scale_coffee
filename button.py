from machine import Pin
from utime import sleep_ms
from constants import POSSIBLE_STATES, BAR, WEIGHT, PERCENTAGE, HIGH, LOW


class Button:
    state = BAR
    def __init__(self, pin: Pin=2):
        self._pin = pin
        self.states = POSSIBLE_STATES
        self._pin.irq(
            trigger=Pin.IRQ_RISING,
            handler=self.cicler,
            )
        
    def cicler(self, *args):
        current_index = self.states.index(Button.state)
        print(current_index)
        new_index = self._calc_clicler(current_index)
        Button.state = self.states[new_index]
        print(Button.state)

    def _calc_clicler(self, cicler_index):
        return cicler_index+1 if cicler_index+1 <= len(self.states)-1 else 0
        
        
    def debugger(self):
        self._pin.irq(
            trigger=Pin.IRQ_RISING,
            handler=self.cicler,
            )


if __name__ == "__main__":
    button = Button(pin=Pin(2))
    while True:
        pass
#         sleep_ms(200)
#         button.debugger()
        
