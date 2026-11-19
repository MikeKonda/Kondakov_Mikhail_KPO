from application.facade import POSFacade
from domain.exceptions import ValidationError

class ConsoleUI:
    def __init__(self, facade: POSFacade):
        self.facade = facade

    def run(self):
        while True:
            print("\n=== МОДУЛЬ ПОС (Преподавательская Оценка Студентов) ===")
            print("1. Добавить студента")
            print("2. Добавить критерий")
            print("3. Выставить оценку")
            print("4. Показать всех студентов и критерии")
            print("5. Посчитать итоговый балл студента")
            print("0. Выход")
            
            choice = input("Выберите действие: ")

            try:
                if choice == "1":
                    self._add_student()
                elif choice == "2":
                    self._add_criterion()
                elif choice == "3":
                    self._evaluate_student()
                elif choice == "4":
                    self._show_all()
                elif choice == "5":
                    self._show_final_grade()
                elif choice == "0":
                    print("До свидания!")
                    break
                else:
                    print("Неверный ввод. Попробуйте снова.")
            except ValidationError as e:
                print(f"\n[ОШИБКА ДОМЕНА]: {e}")
            except Exception as e:
                print(f"\n[СИСТЕМНАЯ ОШИБКА]: {e}")

    def _add_student(self):
        name = input("Введите ФИО студента: ")
        student = self.facade.add_student(name)
        print(f"Студент добавлен! ID: {student.id}")

    def _add_criterion(self):
        name = input("Название критерия: ")
        max_score = float(input("Максимальный балл: "))
        weight = float(input("Вес критерия: "))
        criterion = self.facade.add_criterion(name, max_score, weight)
        print(f"Критерий добавлен! ID: {criterion.id}")

    def _evaluate_student(self):
        self._show_all()
        
        student_id = input("\nВведите ID студента: ")
        criterion_id = input("Введите ID критерия: ")
        score = float(input("Введите балл: "))
        comment = input("Комментарий (опционально, нажмите Enter чтобы пропустить): ")
        
        self.facade.evaluate(student_id, criterion_id, score, comment)
        print("Оценка успешно выставлена!")

    def _show_all(self):
        print("\n--- Студенты ---")
        students = self.facade.get_all_students()
        if not students:
            print("Студентов пока нет.")
        for s in students:
            print(f"ID: {s.id} | Имя: {s.name}")

        print("\n--- Критерии ---")
        criteria = self.facade.get_all_criteria()
        if not criteria:
            print("Критериев пока нет.")
        for c in criteria:
            print(f"ID: {c.id} | {c.name} | Макс: {c.max_score} | Вес: {c.weight.value}")

    def _show_final_grade(self):
        student_id = input("Введите ID студента для расчета итога: ")
        grade = self.facade.get_final_grade(student_id)
        print(f"\nИтоговый балл студента: {grade}")