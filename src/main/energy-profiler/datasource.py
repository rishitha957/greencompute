import pandas as pd

class DataSource:
    def __init__(self):
        self.config = {
            "cpu_power_path": "data/hardware/cpu_power.csv",
        }
    def get_cpu_power_data(self) -> pd.DataFrame:
        """
        Returns CPU power Data
        """
        return pd.read_csv(self.cpu_power_path)