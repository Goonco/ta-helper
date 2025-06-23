import os
from src import config

from src.data_class import ScoreDetail, Score, Criteria
from src.student import Student
from typing import List

import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

import statistics
import csv


class Assignment:
    def __init__(self, name, files):
        self.name = name
        self.path = os.path.join(config.BASE_PATH, name)
        self.files = files

        self.solution = next(
            (file for file in self.files if file.name == "solution.ipynb"), None
        )
        if self.solution is None:
            raise FileNotFoundError(f"'solution.ipynb' not found in {self.path}")

        self.max_score = config.ASSIGNMENT_META[name]["max_score"]
        self.criterias: List[Criteria] = [
            Criteria(**item) for item in config.ASSIGNMENT_META[name]["criteria"]
        ]

        self.average = None
        self.median = None
        self.stdev = None

    def evaluate(self, students: List[Student]):
        scores = [student.scores[self.name].total_score for student in students]

        self.average = sum(scores) / len(students)
        self.median = statistics.median(scores)
        self.stdev = statistics.stdev(scores)

    def dump_csv(self):
        dir_name = os.path.join(config.EVAL_ASSIGNMENT_PATH, self.name)
        os.makedirs(dir_name, exist_ok=True)

        summary_path = os.path.join(dir_name, f"{self.name}_summary.csv")
        with open(summary_path, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Assignment", "Average", "Median", "StdDev"])
            writer.writerow([self.name, self.average, self.median, self.stdev])

    def dump_graph(self, students: List[Student]):
        dir_name = os.path.join(config.EVAL_ASSIGNMENT_PATH, self.name)
        student_names = [student.name for student in students]
        scores = [student.scores[self.name].total_score for student in students]

        plt.rcParams['font.family'] = 'AppleGothic'
        plt.figure(figsize=(15, 6))
        plt.xticks(rotation=45, fontsize=8)
        plt.bar(student_names, scores, color="skyblue")
        plt.title(f"Scores for {self.name}")
        plt.xlabel("Student Name")
        plt.ylabel("Total Score")
        plt.ylim(0, max(scores) + 10)

        plt.tight_layout()
        plt.savefig(os.path.join(dir_name, f"{self.name}_scores.png")) 
