from src.runner import Runner

from src.assignment import Assignment
from src.student import Student
from typing import List


class Evaluator:
    """Evaluate a single assignment."""

    def __init__(self, students : List[Student], assignment : Assignment, inputs):
        self.students = students
        self.assignment = assignment
        self.runner = Runner(inputs)

    def run(self):
        solution_result = self.runner.run(self.assignment.solution.path)

        student_to_file = {}
        for file in self.assignment.files:
            student_to_file[str(file)] = file

        for student in self.students:
            if str(student) in student_to_file:
                file = student_to_file[str(student)]

                print(f"-- Evalauting : {student.name} --")
                student_result = self.runner.run(file.path)

                if student_result != solution_result:
                    print("Wrong : ", student)
                    print(student_result)
                    print(solution_result)
                    print()
                else:
                    print("Correct : ", student)
                    print()
            else:
                print("Not found : ", student)
