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
                
                # Collect valid params (anything except column and type)
                params = {k: v for k, v in r.items() if k not in ["column", "type"]}
                
                rules.append(Rule(column_name=col, rule_type=rule_type, params=params))
            except KeyError:
                # Unknown rule type, skip or log?
                # For now, skip to keep simple.
                continue
        
        return rules

    def dump(self, rules: List[Rule], file_path: str) -> None:
        """
        Serializes a list of Rule entities to a YAML file.
        """
        data = {"rules": []}
        for rule in rules:
            rule_dict = {
                "column": rule.column_name,
                "type": rule.rule_type.name.upper() # Ensure UPPERCASE for consistency
            }
            # Add params if any exists
            if rule.params:
                # accepted_values specific handling? or just dump all params?
                # The entities.py shows Rule has params: Dict[str, Any]
                # For ACCEPTED_VALUES, we want "values" key in the yaml rule object, 
                # but currently Rule puts them in 'params'. 
                # We should flatten params into the rule_dict for the YAML format to be clean.
                # Example YAML: 
                #   - column: "status"
                #     type: "ACCEPTED_VALUES"
                #     values: ["active", "inactive"]
                for k, v in rule.params.items():
                    rule_dict[k] = v
            
            data["rules"].append(rule_dict)

        with open(file_path, 'w') as f:
            yaml.dump(data, f, sort_keys=False)
