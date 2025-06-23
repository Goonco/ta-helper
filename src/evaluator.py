from src.runner import Runner
from multiprocessing import Pool, cpu_count

from src.assignment import Assignment
from src.student import Student
from typing import List
from src.data_class import ScoreDetail, Criteria, ScoreStatus
from src.util import clean_up
from src import config


def run(args):
    runner, student, file, criteria, solution_result = args
    if file:
        student_result = runner.run(file.path)
        is_correct = student_result != solution_result

        status = ScoreStatus.CORRECT if is_correct else ScoreStatus.WRONG
        score = criteria.score if is_correct else 0
        result = student_result
    else:
        status = ScoreStatus.ABSENCE
        score = 0
        result = None

    return student.id, ScoreDetail(criteria.input, status, score, result), runner.created_files_and_dirs


class Evaluator:
    """Evaluate a single assignment"""

    def __init__(self, students: List[Student], assignment: Assignment):
        self.students = students
        self.assignment = assignment

        self.student_to_file = {}
        for file in self.assignment.files:
            self.student_to_file[str(file)] = file

        for student in self.students:
            student.create_score(assignment.name)

        self.id_to_student = {}
        for student in self.students:
            self.id_to_student[student.id] = student

        self.multiprocessing = True

    def __call__(self):
        for criteria in self.assignment.criterias:
            runner = Runner(criteria.input)
            solution_result = runner.run(self.assignment.solution.path)

            args_list = [
                (
                    runner,
                    student,
                    self.student_to_file.get(str(student)),
                    criteria,
                    solution_result,
                )
                for student in self.students
            ]

            if self.multiprocessing:
                with Pool(cpu_count()) as pool:
                    results = pool.map(run, args_list)
            else:
                results = [run(arg) for arg in args_list]

            remove_file_set = set(config.INPUT_PATH)
            for id, score_detail, files in results:
                remove_file_set.add(files)
                self.add_scoreDetail(self.id_to_student[id], score_detail)
            clean_up(remove_file_set)

            self.assignment.evaluate(self.students)

    def add_scoreDetail(self, student: Student, scoreDetail: ScoreDetail):
        student.scores[self.assignment.name].total_score += scoreDetail.score
        student.scores[self.assignment.name].detail.append(scoreDetail)
