from dataclasses import dataclass
from typing import List
from purrfect.domain.entities import DatasetProfile, Hairball

@dataclass
class QualityScore:
    value: float  # 0 to 100
    grade: str    # A, B, F

class ScoreCalculator:
    def calculate(self, profile: DatasetProfile, hairballs: List[Hairball]) -> QualityScore:
        if profile.row_count == 0:
            return QualityScore(value=0.0, grade="F")

        # Count unique rows with errors
        error_row_indices = {h.row_index for h in hairballs}
        unique_error_rows = len(error_row_indices)
        
        # Calculate raw score
        # If all rows have errors, score should be 0.
        # If no rows have errors, score should be 100.
        raw_score = (1 - (unique_error_rows / profile.row_count)) * 100
        
        # Ensure score is within 0-100 (though math should guarantee it if unique_error_rows <= row_count)
        final_score = max(0.0, min(100.0, raw_score))
        
        grade = self._assign_grade(final_score)
        
        return QualityScore(value=round(final_score, 1), grade=grade)

    def _assign_grade(self, score: float) -> str:
        if score >= 95:
            return "A"
        elif score >= 80:
            return "B"
        else:
            return "F"
