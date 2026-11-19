class TestPOSFacade:
    def test_add_student_through_facade(self, facade):
        s = facade.add_student("Алексей")
        assert facade.get_all_students()[0].id == s.id

    def test_add_criterion_through_facade(self, facade):
        c = facade.add_criterion("Лаба", 10, 0.5)
        assert facade.get_all_criteria()[0].id == c.id

    def test_final_grade_no_evaluations_returns_zero(self, facade):
        s = facade.add_student("Алексей")
        assert facade.get_final_grade(s.id) == 0.0

    def test_final_grade_for_nonexistent_student_returns_zero(self, facade):
        assert facade.get_final_grade("no-such-id") == 0.0

    def test_full_flow_through_facade(self, facade):
        s = facade.add_student("Иван")
        c1 = facade.add_criterion("Лаба 1", 10, 0.5)
        c2 = facade.add_criterion("Лаба 2", 20, 0.5)

        facade.evaluate(s.id, c1.id, 10)
        facade.evaluate(s.id, c2.id, 10)

        grade = facade.get_final_grade(s.id)
        assert grade == 0.75