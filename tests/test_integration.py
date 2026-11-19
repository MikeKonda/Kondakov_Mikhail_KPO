class TestIntegration:
    def test_two_students_are_independent(self, facade):
        s1 = facade.add_student("Студент 1")
        s2 = facade.add_student("Студент 2")
        c = facade.add_criterion("Лаба", 10, 1.0)

        facade.evaluate(s1.id, c.id, 10)
        facade.evaluate(s2.id, c.id, 2)

        assert facade.get_final_grade(s1.id) == 1.0
        assert facade.get_final_grade(s2.id) == 0.2

    def test_multiple_criteria_independent(self, facade):
        s = facade.add_student("Иван")
        c1 = facade.add_criterion("A", 10, 0.3)
        c2 = facade.add_criterion("B", 10, 0.7)

        facade.evaluate(s.id, c1.id, 10)
        facade.evaluate(s.id, c2.id, 5)

        assert facade.get_final_grade(s.id) == 0.65

    def test_broken_invariant_does_not_add_data(self, facade):
        s = facade.add_student("Иван")
        c = facade.add_criterion("Лаба", 10, 1.0)

        try:
            facade.evaluate(s.id, c.id, 100)
        except Exception:
            pass

        assert facade.get_final_grade(s.id) == 0.0