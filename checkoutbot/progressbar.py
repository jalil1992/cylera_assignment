from datetime import datetime, timedelta
import math


class ProgressBar:
    def __init__(self, n: int, cols: int = 40):
        self.n = n
        self.cols = cols
        self.started = datetime.now()

    @staticmethod
    def _trunc_ms(td: timedelta):
        return timedelta(seconds=math.ceil(td.total_seconds()))

    def display(self, i: int):
        progress = i / self.n
        filled_cols = math.ceil(progress * self.cols)
        empty_cols = math.floor(self.cols - filled_cols)
        percent = math.ceil(progress * 100)

        elapsed = datetime.now() - self.started
        seconds = elapsed.total_seconds()
        rate = seconds / (i + 1)
        remaining = self.n - i
        eta = timedelta(seconds=remaining * rate)

        out = f"Progress: |{'█' * filled_cols}{'-' * (empty_cols)}| {percent}% (elapsed {self._trunc_ms(elapsed)}, eta {self._trunc_ms(eta)}, current {i + 1}/{self.n})"
        if i == 0:
            print()
        print(f"{out}", end="\r")
        if i + 1 == self.n:
            print("\n")
