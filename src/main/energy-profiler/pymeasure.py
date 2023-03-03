from cpu import *

class EnergyProfiler:
    def __init__(self) -> None:
        print("Intel Power Gadget Available? - ",is_powergadget_available())
        self.pg = IntelPowerGadget()

    def measure_energy_consumption(self,snippet):
        if is_powergadget_available():            
            print(self.pg.get_cpu_details())
            os.system(snippet)
            print(self.pg.get_cpu_details())