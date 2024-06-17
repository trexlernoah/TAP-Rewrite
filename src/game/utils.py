import pandas as pd
import numpy as np
from enum import Enum

class game_state(Enum):
    START = 1
    READY = 2
    HOLD = 3
    SHOCK = 4

class Trial(object):
    def __init__(self, wl, shock, feedback):
        self.wl = wl
        self.shock = shock
        self.feedback = feedback

class DataRow(object):
    def __init__(self, trial):
        self.trial = trial
        self.wl = ''
        self.shock_intensity = '---'
        self.shock_duration = '-----'
        self.reaction_time = ''
    
    def get_row(self):
        return self.trial, self.wl, self.shock_intensity, self.shock_duration, self.reaction_time

class Data(object):
    ''' Main data object '''
    def __init__(self, subject_id: int, lower_shock_threshold: float, upper_shock_threshold: float):
        self.subject_id = subject_id
        self.data_headers = ['Trial', 'W/L', 'Shock Intensity', 'Shock Duration', 'Reaction Time']
        self.data_rows = []
        self.lower_shock_threshold = lower_shock_threshold
        self.upper_shock_threshold = upper_shock_threshold
        self.errors = []

    def append_data_row(self, dr: DataRow):
        for item in dr.get_row():
            self.data_rows.append(item)
        print(self.data_rows)

    def get_data_frame(self) -> pd.DataFrame:
        df = np.empty((0,5))
        for i in range(0, len(self.data_rows), 5):
            dr = []
            for j in range(i, i+5):
                dr.append(self.data_rows[j])
            df = np.append(df, np.array([dr]), axis=0)

        return pd.DataFrame(df)

    def save_data(self, filename: str):
        if not filename: return

        data = self.get_data_frame()
        data.to_csv(filename, sep='\t', encoding='utf-8', index=False)
