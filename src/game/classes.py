import typing
import pandas as pd
import numpy as np

import constants
from dataclasses import dataclass, astuple, field
from typing import List
from enum import Enum


class GameState(Enum):
    START = 1
    READY = 2
    HOLD = 3
    SHOCK = 4


class ErrorMessage(Enum):
    WAIT_TO_START = "Waited too long to press"
    WAIT_TOO_LONG = "Waited too long"
    RELEASE_TOO_SOON = "Released spacebar too soon"
    WAIT_TO_SHOCK = "Waited too long to shock"
    SHOCK_TOO_LONG = "Held shock button too long"


class Trial(typing.NamedTuple):
    wl: str
    shock: int
    feedback: int


@dataclass
class DataRow:
    trial: int
    wl: str = ""
    shock_intensity: str = "---"
    shock_duration: str = "-----"
    reaction_time: str = ""


class Data:
    def __init__(self):
        self.data_rows: List[DataRow] = []
        self.errors: List[ErrorMessage] = []
        self.current_data_row = DataRow(1)

    def finish_trial(self):
        self.data_rows.append(self.current_data_row)
        self.current_data_row = DataRow(self.current_data_row.trial + 1)

    def add_error(self, error: ErrorMessage):
        self.errors.append(error)

    def get_data_frame(self) -> pd.DataFrame:
        df = np.empty((0, 5))

        for data_row in self.data_rows:
            df = np.append(df, np.array([astuple(data_row)]), axis=0)

        df = pd.DataFrame(df)
        df.columns = constants.DATA_HEADERS

        return df

    def get_error_data(self):
        # Get dict of ErrorMessage enum keys with value set at 0
        error_data = {i.name: 0 for i in ErrorMessage}
        for error in self.errors:
            error_data[error.name] += 1
        return error_data

    def save_data(self, filename: str, subject_id: str):
        if not filename:
            return

        data = self.get_data_frame()
        data.to_csv(filename, sep="\t", encoding="utf-8", index=False)

        errors = self.get_error_data()

        with open(filename, "r") as file:
            save = file.read()
        with open(filename, "w") as file:
            file.write(f"Subject: {subject_id}\n\n")
            file.write(save)
            file.write("\n\n")
            for error, count in errors.items():
                file.write(f"{ErrorMessage[error].value}: {count} time(s)\n")


@dataclass(kw_only=True)
class Settings:
    filename: str = ""
    subject_id: str = "SUBJ"
    instruction: str = "Enter instructions here."
    trials: List[Trial] = field(default_factory=list)
