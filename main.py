from src.runner import Runner
from src.evaluator import Evaluator
from src.file_reader import File_Reader
from src.util import check_time

import matplotlib.pyplot as plt

@check_time
def main():
    students = File_Reader.read_students()
    assignments = File_Reader.read_assignments()

    for assignment in assignments:
        Evaluator(students, assignment)()

    for assignment in assignments:

        assignment.dump_csv()
        assignment.dump_graph(students)


if __name__ == "__main__":
    main()
