from machine import Pin, I2C
from ssd_1306 import SSD1306_I2C
from time import sleep
from hx711 import HX711
from utime import sleep_ms
from button import Button, BAR, WEIGHT, PERCENTAGE


class Scale:
    def __init__(self, datapin: int=16, clockpin: int=17, mug: bool=False):
        self._data_pin = datapin
        self._clock_pin = clockpin
        self.scale = HX711(self._data_pin, self._clock_pin)
        self.calibration = -19.81495
        self.zero = 22876
        self.mug = False

        if self.mug:
            self.max_weight = 0.610  # kg
            self.min_weight = 0.310  # kg
        else:
            self.max_weight = 1.16  # kg
            self.min_weight = 0.460  # kg
        
    def read(self):
        weight = ((self.scale.read() - self.zero)/self.calibration)/1000
        return weight


class Display(Button):
    def __init__(self, min_weight:float, max_weight:float, button_pin: Pin):
        self._WIDTH = 128
        self._HEIGHT = 32
        self.i2c = I2C(0, scl=Pin(22), sda=Pin(21))
        self.oled = SSD1306_I2C(self._WIDTH, self._HEIGHT, self.i2c)
        self.min_weight = min_weight
        self.max_weight = max_weight
        super().__init__(button_pin)
    
    def _show_percentage(self, weight):
        
        self.oled.fill(0)
        # Draw progress bar
        
        percentage_string = f"{self._calc_percentage(weight)*100:.1f}%"
        self.oled.text(percentage_string, 32, 16, col=2)
        
        # Update display
        self.oled.show()
        
    def _show_weight(self, weight):
        self.oled.fill(0)
        # Draw progress bar
        
        weight_string = f"{weight:.2f} kg"
        self.oled.text(weight_string, 32, 16, col=2)
        
        # Update display
        self.oled.show()

    def _show_bar(self, weight):
        # Calculate percentage filled
        percentage_to_fill = self._calc_percentage(weight)
        # Calculate pixels to fill
        pixels_to_fill = int(percentage_to_fill * self._WIDTH)

        # Clear display
        self.oled.fill(0)

        # Draw progress bar
        bar_width = pixels_to_fill
#         bar_x = self._WIDTH - bar_width  # Starting x-coordinate for the filled portion
        bar_x = 0
        self.oled.rect(0, 0, self._WIDTH, self._HEIGHT, 1)  # Outline
        self.oled.fill_rect(bar_x, 0, bar_width, self._HEIGHT, 1)  # Filled portion

        # Update display
        self.oled.show()
        
    def _calc_percentage(self, weight: int):
        percentage_filled = (weight - self.min_weight) / (self.max_weight - self.min_weight)
        if percentage_filled < 0:
            percentage_filled = 0
        elif percentage_filled > 1:
            percentage_filled = 1
        return percentage_filled
    
    def show(self, weight):
        if Button.state == BAR:
            self._show_bar(weight)
        elif Button.state == WEIGHT:
            self._show_weight(weight)
        else:
            self._show_percentage(weight)
    
    def poweroff(self):
        return self.oled.poweroff()
        

def run():
    try:
    
        b_pin = Pin(2)
        Button.state = WEIGHT
        scale = Scale()
        display = Display(min_weight=scale.min_weight, max_weight=scale.max_weight, button_pin=b_pin)
        while True:
            current_weight = scale.read()
            print(f"{current_weight=}")
            display.show(current_weight)
            sleep(0.5)
            
    except KeyboardInterrupt:
        display.poweroff()

run()
