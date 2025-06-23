import json
import os
from src import config


class FakeInput:
    def __init__(self):
        with open(config.INPUT_PATH, "r", encoding="utf-8") as f:
            self._inputs = json.load(f)
        self.input_iter = iter(self._inputs)

    def fake_input(self, prompt=""):
        try :
            cur_input = next(self.input_iter)
            print(f"{prompt} {cur_input}")
            return cur_input
        except StopIteration :
            print("Too much input calls!")
            return False


fakeInput = FakeInput()
