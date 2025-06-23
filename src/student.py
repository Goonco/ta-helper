from src.data_class import Score
from typing import Dict


class Student:
    def __init__(self, id, name):
        self.id = id
        self.name = name

        self.scores: Dict[str, Score] = {}

    def __str__(self):
        return f"{self.name}-{self.id}"

    def create_score(self, assignmentName: str):
        self.scores[assignmentName] = Score(0, [])
