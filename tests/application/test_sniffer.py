import pytest
import polars as pl
from purrfect.domain.entities import Rule, RuleType
from purrfect.application.sniffer import DataSniffer

@pytest.fixture
def sniffer():
    return DataSniffer()

def test_sniff_not_null(sniffer):
    data = pl.DataFrame({
        "id": [1, 2, 3],
        "name": ["Alice", None, "Charlie"],
        "age": [30, 25, None]
    })
    
    rules = [
        Rule(column_name="name", rule_type=RuleType.NOT_NULL),
        Rule(column_name="age", rule_type=RuleType.NOT_NULL)
    ]
    
    hairballs = sniffer.sniff(data, rules)
    
    assert len(hairballs) == 2
    
    # Check first hairball (Name null at index 1)
    # The order depends on how we iterate, usually by rule then by row.
    # Name rule is first.
    h1 = hairballs[0]
    assert h1.row_index == 1
    assert h1.column == "name"
    assert h1.rule_type == RuleType.NOT_NULL
    
    # Check second hairball (Age null at index 2)
    h2 = hairballs[1]
    assert h2.row_index == 2
    assert h2.column == "age"
    assert h2.rule_type == RuleType.NOT_NULL

def test_sniff_positive(sniffer):
    data = pl.DataFrame({
        "value": [10, -5, 0, 100],
        "other": [1, 1, 1, 1]
    })
    
    rules = [
        Rule(column_name="value", rule_type=RuleType.POSITIVE)
    ]
    
    hairballs = sniffer.sniff(data, rules)
    
    # -5 is <= 0 (fail)
    # 0 is <= 0 (fail)
    assert len(hairballs) == 2
    
    rows = sorted([h.row_index for h in hairballs])
    assert rows == [1, 2]
    
    for h in hairballs:
        assert h.column == "value"
        assert h.rule_type == RuleType.POSITIVE

def test_sniff_clean(sniffer):
    data = pl.DataFrame({
        "a": [1, 2, 3],
        "b": ["x", "y", "z"]
    })
    
    rules = [
        Rule(column_name="a", rule_type=RuleType.POSITIVE),
        Rule(column_name="b", rule_type=RuleType.NOT_NULL)
    ]
    
    hairballs = sniffer.sniff(data, rules)
    assert len(hairballs) == 0

def test_sniff_missing_column(sniffer):
    data = pl.DataFrame({"a": [1]})
    rules = [Rule(column_name="z", rule_type=RuleType.NOT_NULL)]
    
    # Should currently do nothing (skip missing cols)
    hairballs = sniffer.sniff(data, rules)
    assert len(hairballs) == 0
