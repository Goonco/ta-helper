import os
import pandas as pd
from src import config
from src.data_class import File, Student
from src.assignment import Assignment
from src.student import Student


def read_assignments():
    assignments = []
    candidates = filter(lambda x : os.path.isdiros.path.join(config.BASE_PATH, x), os.listdir(config.BASE_PATH))
    
    for name in config.ASSIGNMENT_META.keys:
        if name in candidates:
            assignments.append(Assignment(name, read_files(os.path.join(config.BASE_PATH, name))))
        else:
            raise FileNotFoundError(f"Assignment {name} not found")

    return assignments


def read_files(dir_path):
    ipynb_files = []
    for file in os.listdir(dir_path):
        if file.endswith(".ipynb"):
            ipynb_files.append(File(file, os.path.join(dir_path, file)))
    return ipynb_files


def read_students():
    students = []
    df = pd.read_csv(
        config.STUDENT_PATH, encoding="utf-8", header=None, names=["name", "student_id"]
    )
    for _, row in df.iterrows():
        students.append(Student(row["student_id"], row["name"]))
    return students
