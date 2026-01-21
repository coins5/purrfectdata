from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Dict, Any, Optional

class RuleType(Enum):
    NOT_NULL = auto()
    POSITIVE = auto()

@dataclass
class Rule:
    column_name: str
    rule_type: RuleType
    params: Dict[str, Any] = field(default_factory=dict)

@dataclass
class Hairball:
    row_index: int
    column: str
    message: str
    rule_type: Optional[RuleType] = None

@dataclass
class DatasetProfile:
    row_count: int
    column_count: int
    columns: list[str]
    missing_cells: int
    duplicate_rows: int
    memory_usage_mb: float
