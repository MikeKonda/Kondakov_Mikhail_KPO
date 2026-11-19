from domain.models import Evaluation, Criterion, Score
from domain.exceptions import ValidationError

class EvaluationFactory:
    
    @staticmethod
    def create(student_id: str, criterion: Criterion, score_value: float, comment: str = "") -> Evaluation:
        try:
            score_vo = Score(value=score_value, max_score=criterion.max_score)
        except ValidationError as e:
            raise ValidationError(f"Ошибка при создании оценки: {e}")

        return Evaluation(
            student_id=student_id,
            criterion_id=criterion.id,
            score=score_vo,
            comment=comment
        )