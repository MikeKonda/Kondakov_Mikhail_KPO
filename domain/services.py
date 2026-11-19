from abc import ABC, abstractmethod
from typing import List, Dict
from .models import Evaluation, Criterion

class GradeCalculationStrategy(ABC):
    @abstractmethod
    def calculate(self, evaluations: List[Evaluation], criteria: Dict[str, Criterion]) -> float:
        pass

class WeightedSumStrategy(GradeCalculationStrategy):
    def calculate(self, evaluations: List[Evaluation], criteria: Dict[str, Criterion]) -> float:
        total = 0.0
        for ev in evaluations:
            criterion = criteria.get(ev.criterion_id)
            if criterion:
                ratio = ev.score.value / criterion.max_score
                total += ratio * criterion.weight.value
        return round(total, 2)

class GradeCalculator:
    def __init__(self, strategy: GradeCalculationStrategy):
        self._strategy = strategy

    def calculate_final_grade(self, evaluations: List[Evaluation], criteria: Dict[str, Criterion]) -> float:
        return self._strategy.calculate(evaluations, criteria)