from typing import List, Optional
from domain.models import Student, Criterion, Evaluation
from domain.repositories import IStudentRepository, ICriterionRepository, IEvaluationRepository

class InMemoryStudentRepository(IStudentRepository):
    def __init__(self):
        self._storage = {}

    def save(self, student: Student) -> None:
        self._storage[student.id] = student

    def get_by_id(self, student_id: str) -> Optional[Student]:
        return self._storage.get(student_id)

    def get_all(self) -> List[Student]:
        return list(self._storage.values())

class InMemoryCriterionRepository(ICriterionRepository):
    def __init__(self):
        self._storage = {}

    def save(self, criterion: Criterion) -> None:
        self._storage[criterion.id] = criterion

    def get_by_id(self, criterion_id: str) -> Optional[Criterion]:
        return self._storage.get(criterion_id)
    
    def get_all(self) -> List[Criterion]:
        return list(self._storage.values())

class InMemoryEvaluationRepository(IEvaluationRepository):
    def __init__(self):
        self._storage = {}

    def save(self, evaluation: Evaluation) -> None:
        self._storage[evaluation.id] = evaluation

    def get_by_student(self, student_id: str) -> List[Evaluation]:
        return [e for e in self._storage.values() if e.student_id == student_id]

    def delete(self, evaluation_id: str) -> None:
        if evaluation_id in self._storage:
            del self._storage[evaluation_id]