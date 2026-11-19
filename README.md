Модуль «ПОС» (Преподавательская Оценка Студентов)
ДЗ2 по КПО

Кондаков Михаил Андреевич БПИ257


ЗАПУСК ПРОЕКТА

Установка зависимостей:
pip install -r requirements.txt

Запуск приложения:
python main.py

Запуск тестов:
python -m pytest -v

АРХИТЕКТУРА

Проект реализован по паттерну Clean Architecture. Зависимости направлены внутрь, к центру - домену.
Infrastructure -> Application -> Domain.

- Domain: Содержит сущности (models.py), доменные сервисы (services.py) и интерфейсы репозиториев (repositories.py). Домен не зависит от консоли или баз данных.
- Application: Слой Use Cases (use_cases.py). Оркестрирует работу домена. Здесь же находится Фасад (facade.py) для UI.
- Infrastructure: Реализация портов (In-Memory репозитории), консольный интерфейс (console_ui.py), DI-контейнер (di_container.py) и реализации паттернов (evaluation_factory.py).
- main.py: Composition Root, где собирается граф зависимостей.

DDD (DOMAIN-DRIVEN DESIGN)

Ubiquitous Language:
Термины: Student (студент), Criterion (критерий), Evaluation (оценка), Score (балл).

Entity и Value Object:
- Value Object (VO): Score и Weight. Они неизменяемы, сравниваются по значению и содержат инварианты. Например, Score проверяет, что балл не меньше 0 и не больше максимума.
- Entity: Student, Criterion, Evaluation. Имеют уникальный идентификатор (UUID) и жизненный цикл.

Инварианты:
- Балл не выходит за пределы критерия (защищено в VO Score).
- Оценка ставится только по существующему критерию (проверяется в EvaluateStudentUseCase).
- Вес критерия не может быть отрицательным (защищено в VO Weight).

Repository:
В домене определены интерфейсы IStudentRepository, ICriterionRepository, IEvaluationRepository. В инфраструктуре они реализованы через InMemory-репозитории.

Domain Service:
GradeCalculator — расчет итогового балла зависит от набора оценок студента и всего рубрикатора.

ПАТТЕРНЫ GOF

1. Порождающий: Фабрика
Где: infrastructure/patterns/evaluation_factory.py (класс EvaluationFactory).
Боль: Централизует создание объекта Evaluation. Фабрика гарантирует, что оценка создается только с валидным Score, защищая инвариант от случайного нарушения.

2. Структурный: Facade
Где: application/facade.py (класс POSFacade).
Боль: Скрывает сложность работы с Use Cases и репозиториями от консольного интерфейса. Предоставляет единый простой API (add_student, evaluate, get_final_grade).

3. Поведенческий: Strategy
Где: domain/services.py (класс GradeCalculator и интерфейс GradeCalculationStrategy).
Боль: Позволяет менять алгоритм подсчета итогового балла (например, WeightedSumStrategy) без изменения кода самого калькулятора.

РОЛЬ ИИ В РЕШЕНИИ

ИИ-помощник использовался как инструмент для генерации базового каркаса проекта, написания тестов и составления README.