from pathlib import Path
from typing import List
import yaml
from purrfect.domain.entities import Rule, RuleType

class YamlParser:
    """
    Infrastructure service to parse YAML files into domain Entities.
    """

    def parse(self, file_path: str) -> List[Rule]:
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"Rules file not found: {file_path}")

        with open(path, 'r') as f:
            try:
                data = yaml.safe_load(f)
            except yaml.YAMLError as e:
                raise ValueError(f"Error parsing YAML file: {e}")

        if not data or "rules" not in data:
             # If empty or structure is wrong, return empty or raise. 
             # Let's return empty list but user should probably know.
             # Actually, let's look for 'rules' key.
             return []

        rules_data = data["rules"]
        rules: List[Rule] = []

        for r in rules_data:
            col = r.get("column")
            r_type_str = r.get("type")

            if not col or not r_type_str:
                continue # Skip malformed rules

            try:
                rule_type = RuleType[r_type_str.upper()]
                rules.append(Rule(column_name=col, rule_type=rule_type))
            except KeyError:
                # Unknown rule type, skip or log?
                # For now, skip to keep simple.
                continue
        
        return rules
