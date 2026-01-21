import pytest
from purrfect.domain.scoring import ScoreCalculator, QualityScore
from purrfect.domain.entities import DatasetProfile, Hairball, RuleType

@pytest.fixture
def calculator():
    return ScoreCalculator()

@pytest.fixture
def mock_profile():
    return DatasetProfile(
        row_count=100,
        column_count=5,
        columns=["col1", "col2", "col3", "col4", "col5"],
        missing_cells=0,
        duplicate_rows=0,
        memory_usage_mb=1.0
    )

def test_score_perfect(calculator, mock_profile):
    hairballs = []
    score = calculator.calculate(mock_profile, hairballs)
    assert score.value == 100.0
    assert score.grade == "A"

def test_score_bad(calculator, mock_profile):
    # Create hairballs for every row
    hairballs = [
        Hairball(row_index=i, column="col1", message="Error", rule_type=RuleType.NOT_NULL)
        for i in range(100)
    ]
    score = calculator.calculate(mock_profile, hairballs)
    assert score.value == 0.0
    assert score.grade == "F"

def test_score_partial_b(calculator, mock_profile):
    # 10 errors (10% bad) -> 90% score -> Grade B
    hairballs = [
        Hairball(row_index=i, column="col1", message="Error", rule_type=RuleType.NOT_NULL)
        for i in range(10)
    ]
    score = calculator.calculate(mock_profile, hairballs)
    assert score.value == 90.0
    assert score.grade == "B"

def test_score_partial_a(calculator, mock_profile):
    # 2 errors (2% bad) -> 98% score -> Grade A
    hairballs = [
        Hairball(row_index=i, column="col1", message="Error", rule_type=RuleType.NOT_NULL)
        for i in range(2)
    ]
    score = calculator.calculate(mock_profile, hairballs)
    assert score.value == 98.0
    assert score.grade == "A"
    
def test_score_partial_f(calculator, mock_profile):
    # 25 errors (25% bad) -> 75% score -> Grade F
    hairballs = [
        Hairball(row_index=i, column="col1", message="Error", rule_type=RuleType.NOT_NULL)
        for i in range(25)
    ]
    score = calculator.calculate(mock_profile, hairballs)
    assert score.value == 75.0
    assert score.grade == "F"

def test_multiple_errors_same_row(calculator, mock_profile):
    # 1 row with multiple errors should count as 1 bad row.
    # 1 bad row out of 100 -> 99% score.
    hairballs = [
        Hairball(row_index=0, column="col1", message="Error 1", rule_type=RuleType.NOT_NULL),
        Hairball(row_index=0, column="col2", message="Error 2", rule_type=RuleType.POSITIVE)
    ]
    score = calculator.calculate(mock_profile, hairballs)
    assert score.value == 99.0
    assert score.grade == "A"

def test_zero_rows_handling(calculator):
    profile = DatasetProfile(
        row_count=0,
        column_count=5,
        columns=[],
        missing_cells=0,
        duplicate_rows=0,
        memory_usage_mb=0.0
    )
    score = calculator.calculate(profile, [])
    assert score.value == 0.0
    assert score.grade == "F"
