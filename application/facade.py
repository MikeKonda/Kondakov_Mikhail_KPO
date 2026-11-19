from typing import List, Optional
from domain.models import Student, Criterion
from domain.repositories import IStudentRepository, ICriterionRepository, IEvaluationRepository
from domain.services import GradeCalculator
from application.use_cases import AddStudentUseCase, AddCriterionUseCase, EvaluateStudentUseCase
from domain.exceptions import ValidationError

class POSFacade:
    def __init__(
        self,
        add_student_uc: AddStudentUseCase,
        add_criterion_uc: AddCriterionUseCase,
        evaluate_uc: EvaluateStudentUseCase,
        student_repo: IStudentRepository,
        crit_repo: ICriterionRepository,
        eval_repo: IEvaluationRepository,
        grade_calculator: GradeCalculator
    ):
        self.add_student_uc = add_student_uc
        self.add_criterion_uc = add_criterion_uc
        self.evaluate_uc = evaluate_uc
        self.student_repo = student_repo
        self.crit_repo = crit_repo
        self.eval_repo = eval_repo
        self.grade_calculator = grade_calculator

    def add_student(self, name: str) -> Student:
        return self.add_student_uc.execute(name)

    def add_criterion(self, name: str, max_score: float, weight: float) -> Criterion:
        return self.add_criterion_uc.execute(name, max_score, weight)

    def evaluate(self, student_id: str, criterion_id: str, score: float, comment: str = "") -> None:
        self.evaluate_uc.execute(student_id, criterion_id, score, comment)

    def get_all_students(self) -> List[Student]:
        return self.student_repo.get_all()

    def get_all_criteria(self) -> List[Criterion]:
        return self.crit_repo.get_all()

    def get_final_grade(self, student_id: str) -> float:
        evaluations = self.eval_repo.get_by_student(student_id)
        
        all_criteria = {c.id: c for c in self.crit_repo.get_all()}
        
        if not evaluations:
            return 0.0
            
        return self.grade_calculator.calculate_final_grade(evaluations, all_criteria)