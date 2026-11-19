import pytest
from domain.models import Score, Weight, Student, Criterion, Evaluation
from domain.services import GradeCalculator, WeightedSumStrategy


def make_criterion(name: str, max_score: float, weight: float) -> Criterion:
    return Criterion(name=name, max_score=max_score, weight=Weight(weight))


def make_evaluation(student_id, criterion, value, comment=""):
    return Evaluation(
        student_id=student_id,
        criterion_id=criterion.id,
        score=Score(value, criterion.max_score),
        comment=comment,
    )


class TestWeightedSumStrategy:
    def test_no_evaluations_returns_zero(self):
        calc = GradeCalculator(WeightedSumStrategy())
        assert calc.calculate_final_grade([], {}) == 0.0

    def test_single_full_score(self):
        c = make_criterion("Лаба", 10, 0.5)
        e = make_evaluation("s1", c, 10)
        calc = GradeCalculator(WeightedSumStrategy())
        assert calc.calculate_final_grade([e], {c.id: c}) == 0.5

    def test_single_half_score(self):
        c = make_criterion("Лаба", 10, 1.0)
        e = make_evaluation("s1", c, 5)
        calc = GradeCalculator(WeightedSumStrategy())
        assert calc.calculate_final_grade([e], {c.id: c}) == 0.5

    def test_zero_score(self):
        c = make_criterion("Лаба", 10, 1.0)
        e = make_evaluation("s1", c, 0)
        calc = GradeCalculator(WeightedSumStrategy())
        assert calc.calculate_final_grade([e], {c.id: c}) == 0.0

    def test_multiple_evaluations_sum(self):
        c1 = make_criterion("A", 10, 0.5)
        c2 = make_criterion("B", 10, 0.5)
        e1 = make_evaluation("s1", c1, 10)
        e2 = make_evaluation("s1", c2, 5)
        calc = GradeCalculator(WeightedSumStrategy())
        result = calc.calculate_final_grade([e1, e2], {c1.id: c1, c2.id: c2})
        assert result == 0.75

    def test_zero_weight_contributes_nothing(self):
        c = make_criterion("A", 10, 0.0)
        e = make_evaluation("s1", c, 10)
        calc = GradeCalculator(WeightedSumStrategy())
        assert calc.calculate_final_grade([e], {c.id: c}) == 0.0

    def test_rounding_two_decimals(self):
        c = make_criterion("A", 3, 1.0)
        e = make_evaluation("s1", c, 1)
        calc = GradeCalculator(WeightedSumStrategy())
        assert calc.calculate_final_grade([e], {c.id: c}) == 0.33

    def test_evaluation_for_unknown_criterion_is_ignored(self):
        c = make_criterion("A", 10, 1.0)
        e = make_evaluation("s1", c, 10)
        calc = GradeCalculator(WeightedSumStrategy())
        assert calc.calculate_final_grade([e], {}) == 0.0

    def test_strategy_is_swappable(self):
        class AlwaysOneStrategy:
            def calculate(self, evaluations, criteria):
                return 1.0

        calc = GradeCalculator(AlwaysOneStrategy())
        assert calc.calculate_final_grade([], {}) == 1.0