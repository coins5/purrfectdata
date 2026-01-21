from typing import List, Optional
from purrfect.domain.entities import Rule, RuleType, ColumnStats

class RuleInferer:
    """
    Domain service that infers rules based on column statistics.
    """

    def infer(self, column_stats: List[ColumnStats]) -> List[Rule]:
        rules = []
        for stat in column_stats:
            # 1. NOT_NULL
            # If we see no nulls in the sample, we assume it *should* be not null.
            if stat.null_count == 0:
                rules.append(Rule(column_name=stat.name, rule_type=RuleType.NOT_NULL))

            # 2. POSITIVE
            # If numeric and min >= 0, suggest POSITIVE (unless it's all zeros? maybe just POSITIVE for now)
            # We blindly assume if min >= 0 it might be a positive constraint. 
            # This is a heuristic, so false positives are expected.
            if stat.dtype in ('Int64', 'Float64') and stat.min_value is not None:
                if stat.min_value >= 0:
                    rules.append(Rule(column_name=stat.name, rule_type=RuleType.POSITIVE))

            # 3. ACCEPTED_VALUES (Categorical detection)
            # If string type, and n_unique is small relative to total count, or absolute small number?
            # Let's say if unique ratio < 10% AND n_unique < 20 (to avoid huge enums)
            if stat.dtype == 'String' and stat.count > 0:
                unique_ratio = stat.n_unique / stat.count
                if (unique_ratio < 0.1 or stat.n_unique < 20) and stat.unique_values:
                    # Clean up unique values (remove None if present, though null_count check might handle it)
                    clean_values = [v for v in stat.unique_values if v is not None]
                    if clean_values:
                        rules.append(Rule(
                            column_name=stat.name, 
                            rule_type=RuleType.ACCEPTED_VALUES,
                            params={'values': clean_values}
                        ))
        
        return rules
