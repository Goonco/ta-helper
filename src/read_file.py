import os
import pandas as pd
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
        candidates = filter(
            lambda x: os.path.isdir(os.path.join(config.BASE_PATH, x)),
            os.listdir(config.BASE_PATH),
        )

        for name in config.ASSIGNMENT_META.keys():
            if name in candidates:
                assignments.append(
                    Assignment(
                        name,
                        File_Reader.read_files(os.path.join(config.BASE_PATH, name)),
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
