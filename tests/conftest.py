import pytest

from domain.services import GradeCalculator, WeightedSumStrategy
from application.use_cases import AddStudentUseCase, AddCriterionUseCase, EvaluateStudentUseCase
from application.facade import POSFacade
from infrastructure.repositories import (
    InMemoryStudentRepository,
    InMemoryCriterionRepository,
    InMemoryEvaluationRepository,
)


@pytest.fixture
def student_repo():
    return InMemoryStudentRepository()


@pytest.fixture
def crit_repo():
    return InMemoryCriterionRepository()


@pytest.fixture
def eval_repo():
    return InMemoryEvaluationRepository()


@pytest.fixture
def grade_calculator():
    return GradeCalculator(WeightedSumStrategy())


@pytest.fixture
def facade(student_repo, crit_repo, eval_repo, grade_calculator):
    return POSFacade(
        AddStudentUseCase(student_repo),
        AddCriterionUseCase(crit_repo),
        EvaluateStudentUseCase(eval_repo, crit_repo, student_repo),
        student_repo,
        crit_repo,
        eval_repo,
        grade_calculator,
    )