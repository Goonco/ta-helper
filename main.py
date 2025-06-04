from src.read_file import read_assignments, read_students
from src.runner import Runner
from src.evaluator import Evaluator

if __name__ == "__main__":
    students = read_students()
    assignment = read_assignments()

    evaluator = Evaluator(students, assignment[0], ["Sogang University"])
    evaluator.run()

    # for assignment in read_assignments(config.BASE_PATH) :
    # for file in assignment.files :
    #     runner = Runner(file.path, ["Sogang University"])

    # inputs = User_Input()
    # file_organizer = File_Organizer(inputs.delete_file_flag, inputs.total_problem, inputs.target_problem)
    # ids = file_organizer.run()

    # eval_result = Evaluator(ids, inputs.ignore_space_flag, inputs.essentials, inputs.forbiddens, inputs.inputs).run();
    # Result_Printer.run(eval_result);

    # inputs.check_feedback_id()
    # if inputs.feedback_id_flag : file_organizer.feedback_ids(ids)
