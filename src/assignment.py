import os
from src import config

class Assignment:
    def __init__(self, name, files):
        self.name = name
        self.path = os.path.join(config.BASE_PATH, name)
        self.files = files
        
        self.solution = None
        for file in self.files:
            solution = file
        if solution is None:
            raise FileNotFoundError(f"solution.ipynb' not found in {self.path}")
        
        self.max_score = config.ASSIGNMENT_META[name]["max_score"]
    
        
    def evaluate(self) :
        # 평균, 표준편차, 중앙값, 각 학생의 점수, 
    
        

        
    