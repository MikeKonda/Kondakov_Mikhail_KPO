import pytest
from application.use_cases import AddStudentUseCase, AddCriterionUseCase, EvaluateStudentUseCase
from domain.exceptions import ValidationError


class TestAddStudentUseCase:
    def test_valid_name(self, student_repo):
        uc = AddStudentUseCase(student_repo)
        student = uc.execute("Иван Иванов")
        assert student.name == "Иван Иванов"
        assert student_repo.get_by_id(student.id) is not None

    def test_empty_name_raises(self, student_repo):
        uc = AddStudentUseCase(student_repo)
        with pytest.raises(ValidationError, match="Имя студента"):
            uc.execute("")

    def test_whitespace_name_raises(self, student_repo):
        uc = AddStudentUseCase(student_repo)
        with pytest.raises(ValidationError, match="Имя студента"):
            uc.execute("   ")


class TestAddCriterionUseCase:
    def test_valid_criterion(self, crit_repo):
        uc = AddCriterionUseCase(crit_repo)
        c = uc.execute("Лаба", 10, 0.5)
        assert c.name == "Лаба"
        assert crit_repo.get_by_id(c.id) is not None

    def test_zero_max_score_raises(self, crit_repo):
        uc = AddCriterionUseCase(crit_repo)
        with pytest.raises(ValidationError, match="Максимальный балл"):
            uc.execute("Лаба", 0, 1.0)

    def test_negative_max_score_raises(self, crit_repo):
        uc = AddCriterionUseCase(crit_repo)
        with pytest.raises(ValidationError, match="Максимальный балл"):
            uc.execute("Лаба", -5, 1.0)

    def test_negative_weight_raises(self, crit_repo):
        uc = AddCriterionUseCase(crit_repo)
        with pytest.raises(ValidationError, match="Вес не может быть отрицательным"):
            uc.execute("Лаба", 10, -0.1)


class TestEvaluateStudentUseCase:
    def _prepare(self, student_repo, crit_repo):
        student = AddStudentUseCase(student_repo).execute("Петр")
        criterion = AddCriterionUseCase(crit_repo).execute("Лаба", 10, 1.0)
        return student, criterion

    def test_valid_evaluation(self, student_repo, crit_repo, eval_repo):
        student, criterion = self._prepare(student_repo, crit_repo)
        uc = EvaluateStudentUseCase(eval_repo, crit_repo, student_repo)
        uc.execute(student.id, criterion.id, 7.5)
        evals = eval_repo.get_by_student(student.id)
        assert len(evals) == 1
        assert evals[0].score.value == 7.5

    def test_nonexistent_student_raises(self, student_repo, crit_repo, eval_repo):
        _, criterion = self._prepare(student_repo, crit_repo)
        uc = EvaluateStudentUseCase(eval_repo, crit_repo, student_repo)
        with pytest.raises(ValidationError, match="Студент не найден"):
            uc.execute("fake-id", criterion.id, 5)

    def test_nonexistent_criterion_raises(self, student_repo, crit_repo, eval_repo):
        student, _ = self._prepare(student_repo, crit_repo)
        uc = EvaluateStudentUseCase(eval_repo, crit_repo, student_repo)
        with pytest.raises(ValidationError, match="Критерий не найден"):
            uc.execute(student.id, "fake-id", 5)

    def test_score_above_max_raises(self, student_repo, crit_repo, eval_repo):
        student, criterion = self._prepare(student_repo, crit_repo)
        uc = EvaluateStudentUseCase(eval_repo, crit_repo, student_repo)
        with pytest.raises(ValidationError, match="превышает максимум"):
            uc.execute(student.id, criterion.id, 15)

    def test_negative_score_raises(self, student_repo, crit_repo, eval_repo):
        student, criterion = self._prepare(student_repo, crit_repo)
        uc = EvaluateStudentUseCase(eval_repo, crit_repo, student_repo)
        with pytest.raises(ValidationError, match="не может быть отрицательной"):
            uc.execute(student.id, criterion.id, -1)

    def test_boundary_score_zero(self, student_repo, crit_repo, eval_repo):
        student, criterion = self._prepare(student_repo, crit_repo)
        uc = EvaluateStudentUseCase(eval_repo, crit_repo, student_repo)
        uc.execute(student.id, criterion.id, 0)
        assert eval_repo.get_by_student(student.id)[0].score.value == 0

    def test_boundary_score_max(self, student_repo, crit_repo, eval_repo):
        student, criterion = self._prepare(student_repo, crit_repo)
        uc = EvaluateStudentUseCase(eval_repo, crit_repo, student_repo)
        uc.execute(student.id, criterion.id, 10)
        assert eval_repo.get_by_student(student.id)[0].score.value == 10