import json
import os
from BaseClasses import ItemClassification
from ..config import make_config
from . import MetroidPrimeTestBase


def dict_diff(d1, d2, path=""):
    """Prints out the differences between two dictionaries recursively, will show up if the test fails"""
    for k in d1:
        if k not in d2:
            print(f"{path}: Key {k} not found in second dict")
        elif isinstance(d1[k], dict) and isinstance(d2[k], dict):
            dict_diff(d1[k], d2[k], path=f"{path}.{k}")
        elif d1[k] != d2[k]:
            print(f"Difference at {path}.{k}: {d1[k]} != {d2[k]}")

    for k in d2:
        if k not in d1:
            print(f"{path}: Key {k} not found in first dict")

class TestOutputGeneration(MetroidPrimeTestBase):
    options = {
    }

    def test_output_generates_correctly(self) -> None:
        self.test_fill()
        output = make_config(self.world)
        expected_output = {}
        path = os.path.join(os.path.dirname(__file__), "data", "vanilla_config.json")
        with open(path, "r") as f:
            expected_output = json.load(f)

        dict_diff(expected_output, output)
        self.assertDictEqual(output, expected_output)
