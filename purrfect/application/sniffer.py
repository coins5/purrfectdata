from typing import List, Any
import polars as pl
from purrfect.domain.entities import Rule, RuleType, Hairball

class DataSniffer:
    """
    Application service that applies validation rules to a dataset.
    """

    def sniff(self, data: Any, rules: List[Rule]) -> List[Hairball]:
        """
        Validates the data against the provided rules.
        
        :param data: The dataset to validate (expected to be a Polars DataFrame).
        :param rules: A list of rules to apply.
        :return: A list of Hairballs (errors) found.
        """
        if not isinstance(data, pl.DataFrame):
            # In a real app we might try to convert or raise a specific error
            raise ValueError("DataSniffer currently only supports Polars DataFrames.")

        hairballs: List[Hairball] = []
        
        # Ensure we have a row index to report back
        # using 'row_nr' as a temporary column
        df_with_idx = data.with_row_index("row_nr")

        for rule in rules:
            if rule.rule_type == RuleType.NOT_NULL:
                self._check_not_null(df_with_idx, rule, hairballs)
            elif rule.rule_type == RuleType.POSITIVE:
                self._check_positive(df_with_idx, rule, hairballs)
        
        return hairballs

    def _check_not_null(self, df: pl.DataFrame, rule: Rule, hairballs: List[Hairball]):
        col = rule.column_name
        if col not in df.columns:
            return # Or raise error? For now, skip if column missing (or maybe it IS the error?)
                   # Let's assume we skip validation for missing columns or handle elsewhere if schema is strict.
                   # Ideally, missing column might be a schema error, but let's stick to row-level validation here.

        bad_rows = df.filter(pl.col(col).is_null()).select("row_nr")
        
        for row in bad_rows.iter_rows():
            idx = row[0]
            hairballs.append(Hairball(
                row_index=idx,
                column=col,
                message=f"Value in column '{col}' is null.",
                rule_type=rule.rule_type
            ))

    def _check_positive(self, df: pl.DataFrame, rule: Rule, hairballs: List[Hairball]):
        col = rule.column_name
        if col not in df.columns:
            return

        # Check for non-null values that are <= 0
        # We generally skip nulls in value checks unless specified otherwise, to avoid double reporting if NOT_NULL is also present.
        bad_rows = df.filter(
            (pl.col(col).is_not_null()) & (pl.col(col) <= 0)
        ).select("row_nr", col)

        for row in bad_rows.iter_rows():
            idx = row[0]
            val = row[1]
            hairballs.append(Hairball(
                row_index=idx,
                column=col,
                message=f"Value {val} in column '{col}' is not positive.",
                rule_type=rule.rule_type
            ))
