from hx711 import HX711
from utime import sleep_us


class Balanca:
        def __init__(self):
                    self.DOUT_PIN = 4  # Example pin numbers, please adjust based on your actual connections
                            self.PD_SCK_PIN = 5  # Example pin numbers, please adjust based on your actual connections
                                    self.TARE_VALUE = 22876
                                            # CALIBRATION_VALUE = -20.47
                                                    self.CALIBRATION_VALUE = -19.81495
                                                            # Initialize the HX711 module
                                                                    self.hx711 = HX711(d_out=self.DOUT_PIN, pd_sck=self.PD_SCK_PIN)


                                                                        def read_weight(self):
                                                                                    """
                                                                                            Function to read the weight from the HX711 module.
                                                                                                    """
                                                                                                            # Read the weight and print it
                                                                                                                    res = ((self.hx711.read(raw=True) - self.TARE_VALUE)/self.CALIBRATION_VALUE)/1000  # turn grams to kg.
                                                                                                                            return res

                                                                                                                            def tare(self):
                                                                                                                                        """
                                                                                                                                                Function to calibrate the scale and find the offset.
                                                                                                                                                        """
                                                                                                                                                                # Perform tare to find the offset
                                                                                                                                                                        
                                                                                                                                                                                self.TARE_VALUE = self.hx711.read(raw=True)
                                                                                                                                                                                        print("Offset:", self.TARE_VALUE)

                                                                                                                                                                                            def calibrate_scale(self):
                                                                                                                                                                                                        """
                                                                                                                                                                                                                Function to calibrate the scale and offset.
                                                                                                                                                                                                                        """
                                                                                                                                                                                                                                # Perform tare to find the offset
                                                                                                                                                                                                                                        self.tare()
                                                                                                                                                                                                                                                print("Put the weight in the scale")
                                                                                                                                                                                                                                                        sleep_us(5000000)
                                                                                                                                                                                                                                                                print("reading the weight")
                                                                                                                                                                                                                                                                        
                                                                                                                                                                                                                                                                                self.CALIBRATION_VALUE = (self.hx711.read(raw=True)-self.TARE_VALUE)/535.0
                                                                                                                                                                                                                                                                                        
                                                                                                                                                                                                                                                                                                print('the calibration value should be: ', self.CALIBRATION_VALUE)

                                                                                                                                                                                                                                                                                                    def get_offset(self):
                                                                                                                                                                                                                                                                                                                return self.TARE_VALUE

                                                                                                                                                                                                                                                                                                            if __name__ == "__main__":
                                                                                                                                                                                                                                                                                                                    bal = Balanca()
                                                                                                                                                                                                                                                                                                                        w = bal.read_weight()
                                                                                                                                                                                                                                                                                                                            print(w)


