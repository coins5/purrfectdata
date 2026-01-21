import pytest
from pathlib import Path
from purrfect.infrastructure.yaml_parser import YamlParser
from purrfect.domain.entities import RuleType

@pytest.fixture
def parser():
    return YamlParser()

def test_parse_valid_rules(parser, tmp_path):
    # Create a temporary YAML file
    rules_file = tmp_path / "rules.yaml"
    rules_file.write_text("""
rules:
  - column: "price"
    type: "POSITIVE"
  - column: "name"
    type: "NOT_NULL"
""")
    
    rules = parser.parse(str(rules_file))
    
    assert len(rules) == 2
    assert rules[0].column_name == "price"
    assert rules[0].rule_type == RuleType.POSITIVE
    assert rules[1].column_name == "name"
    assert rules[1].rule_type == RuleType.NOT_NULL

def test_parse_file_not_found(parser):
    with pytest.raises(FileNotFoundError):
        parser.parse("non_existent_file.yaml")

def test_parse_invalid_yaml(parser, tmp_path):
    bad_file = tmp_path / "bad.yaml"
    bad_file.write_text("rules: [ unclosed list")
    
    with pytest.raises(ValueError, match="Error parsing YAML"):
        parser.parse(str(bad_file))

def test_parse_malformed_rules(parser, tmp_path):
    # Missing type or column should be skipped based on implementation
    rules_file = tmp_path / "partial.yaml"
    rules_file.write_text("""
rules:
  - column: "only_column"
  - type: "POSITIVE"
  - column: "valid"
    type: "POSITIVE"
""")
    rules = parser.parse(str(rules_file))
    assert len(rules) == 1
    assert rules[0].column_name == "valid"
