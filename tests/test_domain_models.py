import pytest
from domain.models import Score, Weight, Student, Criterion, Evaluation
from domain.exceptions import ValidationError


class TestScore:
    def test_score_zero_is_valid(self):
        s = Score(value=0, max_score=10)
        assert s.value == 0

    def test_score_equal_to_max_is_valid(self):
        s = Score(value=10, max_score=10)
        assert s.value == 10

    def test_score_between_is_valid(self):
        s = Score(value=5.5, max_score=10)
        assert s.value == 5.5

    def test_score_negative_raises(self):
        with pytest.raises(ValidationError, match="не может быть отрицательной"):
            Score(value=-0.01, max_score=10)

    def test_score_above_max_raises(self):
        with pytest.raises(ValidationError, match="превышает максимум"):
            Score(value=10.01, max_score=10)

    def test_score_is_frozen(self):
        s = Score(value=5, max_score=10)
        with pytest.raises(Exception):
            s.value = 7

    def test_score_equality_by_value(self):
        assert Score(5, 10) == Score(5, 10)
        assert Score(5, 10) != Score(5, 20)


class TestWeight:
    def test_weight_zero_is_valid(self):
        w = Weight(0)
        assert w.value == 0

    def test_weight_positive_is_valid(self):
        assert Weight(0.5).value == 0.5

    def test_weight_negative_raises(self):
        with pytest.raises(ValidationError, match="Вес не может быть отрицательным"):
            Weight(-1)


class TestEntities:
    def test_student_gets_uuid(self):
        s = Student(name="Иван")
        assert s.id is not None
        assert len(s.id) == 36

    def test_students_have_unique_ids(self):
        s1, s2 = Student("A"), Student("B")
        assert s1.id != s2.id

    def test_criterion_contains_weight_vo(self):
        c = Criterion(name="Лаба", max_score=10, weight=Weight(0.5))
        assert c.weight.value == 0.5
        assert c.max_score == 10

    def test_evaluation_stores_score_vo(self):
        e = Evaluation(
            student_id="s1",
            criterion_id="c1",
            score=Score(8, 10),
            comment="Ок",
        )
        assert e.score.value == 8
        assert e.comment == "Ок"