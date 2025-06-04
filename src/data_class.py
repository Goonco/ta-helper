from dataclasses import dataclass
from typing import List

import re


@dataclass(frozen=True)
class File:
    NAME_ID_PATTERN = re.compile(r"([^-s]+-\d+)")
    
    name: str
    path: str

    def __str__(self) -> str:
        match = self.NAME_ID_PATTERN.match(self.name)
        if match:
            return match.group(1)
        return self.name

@dataclass(frozen=True)
class Result:
    type: str
    data: str

    def __str__(self) -> str:
        return f"{self.type}: {self.data}"