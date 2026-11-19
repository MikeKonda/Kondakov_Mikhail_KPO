from domain.models import Student, Criterion, Weight
from domain.repositories import IStudentRepository, ICriterionRepository, IEvaluationRepository
from infrastructure.patterns.evaluation_factory import EvaluationFactory
from domain.exceptions import ValidationError

class AddStudentUseCase:
    def __init__(self, repo: IStudentRepository):
        self.repo = repo

    def execute(self, name: str) -> Student:
        if not name.strip():
            raise ValidationError("Имя студента не может быть пустым")
        student = Student(name=name)
        self.repo.save(student)
        return student

class AddCriterionUseCase:
    def __init__(self, repo: ICriterionRepository):
        self.repo = repo

    def execute(self, name: str, max_score: float, weight_value: float) -> Criterion:
        if max_score <= 0:
            raise ValidationError("Максимальный балл должен быть больше нуля")
        
        weight = Weight(weight_value)
        criterion = Criterion(name=name, max_score=max_score, weight=weight)
        self.repo.save(criterion)
        return criterion

class EvaluateStudentUseCase:
    def __init__(self, eval_repo: IEvaluationRepository, crit_repo: ICriterionRepository, student_repo: IStudentRepository):
        self.eval_repo = eval_repo
        self.crit_repo = crit_repo
        self.student_repo = student_repo

    def execute(self, student_id: str, criterion_id: str, score_value: float, comment: str = "") -> None:
        student = self.student_repo.get_by_id(student_id)
        if not student:
            raise ValidationError("Студент не найден!")

        criterion = self.crit_repo.get_by_id(criterion_id)
        if not criterion:
            raise ValidationError("Критерий не найден в рубрикаторе!")
        
        evaluation = EvaluationFactory.create(student_id, criterion, score_value, comment)
        
        self.eval_repo.save(evaluation)