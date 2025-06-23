from dataclasses import dataclass
from typing import List
from enum import Enum

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


class ScoreStatus(Enum):
    CORRECT = 1
    WRONG = 2
    ABSENCE = 3


@dataclass(frozen=True)
class ScoreDetail:
    input: str
    status: ScoreStatus
    score: int
    result: Result | None


@dataclass
class Score:
    """Score for a single assignment"""

    total_score: int
    detail: List[ScoreDetail]


@dataclass(frozen=True)
class Criteria:
    input: List[str]
    score: int
