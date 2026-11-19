from abc import ABC, abstractmethod
from typing import List, Optional
from .models import Student, Criterion, Evaluation

class IStudentRepository(ABC):
    @abstractmethod
    def save(self, student: Student) -> None: pass
    
    @abstractmethod
    def get_by_id(self, student_id: str) -> Optional[Student]: pass

    @abstractmethod
    def get_all(self) -> List[Student]: pass

class ICriterionRepository(ABC):
    @abstractmethod
    def save(self, criterion: Criterion) -> None: pass

    @abstractmethod
    def get_by_id(self, criterion_id: str) -> Optional[Criterion]: pass
    
    @abstractmethod
    def get_all(self) -> List[Criterion]: pass

class IEvaluationRepository(ABC):
    @abstractmethod
    def save(self, evaluation: Evaluation) -> None: pass
    
    @abstractmethod
    def get_by_student(self, student_id: str) -> List[Evaluation]: pass
    
    @abstractmethod
    def delete(self, evaluation_id: str) -> None: pass