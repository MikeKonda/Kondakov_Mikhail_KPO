from dataclasses import dataclass, field
from typing import Optional
from uuid import uuid4
from .exceptions import ValidationError


@dataclass(frozen=True)
class Score:
    value: float
    max_score: float

    def __post_init__(self):
        if self.value < 0:
            raise ValidationError(f"Оценка не может быть отрицательной: {self.value}")
        if self.value > self.max_score:
            raise ValidationError(f"Оценка {self.value} превышает максимум {self.max_score}")


@dataclass(frozen=True)
class Weight:
    value: float

    def __post_init__(self):
        if self.value < 0:
            raise ValidationError("Вес не может быть отрицательным")


@dataclass
class Student:
    name: str
    id: str = field(default_factory=lambda: str(uuid4()))

@dataclass
class Criterion:
    name: str
    max_score: float
    weight: Weight
    id: str = field(default_factory=lambda: str(uuid4()))

@dataclass
class Evaluation:
    student_id: str
    criterion_id: str
    score: Score
    comment: Optional[str] = None
    id: str = field(default_factory=lambda: str(uuid4()))