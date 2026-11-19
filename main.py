from infrastructure.di_container import DIContainer
from infrastructure.repositories import InMemoryStudentRepository, InMemoryCriterionRepository, InMemoryEvaluationRepository
from domain.services import GradeCalculator, WeightedSumStrategy
from application.use_cases import AddStudentUseCase, AddCriterionUseCase, EvaluateStudentUseCase
from application.facade import POSFacade
from infrastructure.console_ui import ConsoleUI

def main():
    print("Инициализация приложения...")
    
    container = DIContainer()

    student_repo = InMemoryStudentRepository()
    crit_repo = InMemoryCriterionRepository()
    eval_repo = InMemoryEvaluationRepository()

    strategy = WeightedSumStrategy()
    grade_calculator = GradeCalculator(strategy)

    add_student_uc = AddStudentUseCase(student_repo)
    add_criterion_uc = AddCriterionUseCase(crit_repo)
    evaluate_uc = EvaluateStudentUseCase(eval_repo, crit_repo, student_repo)

    facade = POSFacade(
        add_student_uc, 
        add_criterion_uc, 
        evaluate_uc,
        student_repo,
        crit_repo,
        eval_repo,
        grade_calculator
    )

    container.register("facade", facade)

    ui = ConsoleUI(container.resolve("facade"))
    ui.run()

if __name__ == "__main__":
    main()