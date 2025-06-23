import os
import pandas as pd
import unicodedata

from src import config
from src.data_class import File
from src.assignment import Assignment
from src.student import Student
from src.util import check_time
from typing import List


class File_Reader:

    @staticmethod
    @check_time
    def read_assignments() -> List[Assignment]:
        assignments = []
        raw_candidates = [
            x for x in os.listdir(config.BASE_PATH)
            if os.path.isdir(os.path.join(config.BASE_PATH, x))
        ]
        candidates = [unicodedata.normalize("NFC", x) for x in raw_candidates]

        for name in config.ASSIGNMENT_META.keys():
            normalized_name = unicodedata.normalize("NFC", name)
            if normalized_name in candidates:
                assignments.append(
                    Assignment(
                        normalized_name,
                        File_Reader.read_files(os.path.join(config.BASE_PATH, normalized_name)),
                    )
                )
            else:
                raise FileNotFoundError(f"Assignment {name} not found")

        return assignments

    @staticmethod
    @check_time
    def read_files(dir_path):
        ipynb_files = []
        for file in os.listdir(dir_path):
            if file.endswith(".ipynb"):
                ipynb_files.append(File(file, os.path.join(dir_path, file)))
        return ipynb_files

    @staticmethod
    @check_time
    def read_students() -> List[Student]:
        students = []
        df = pd.read_csv(
            config.STUDENT_PATH,
            encoding="utf-8",
            header=None,
            names=["name", "student_id"],
        )
        for _, row in df.iterrows():
            students.append(Student(row["student_id"], row["name"]))
        return students
