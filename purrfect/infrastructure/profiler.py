import polars as pl
from purrfect.domain.entities import DatasetProfile

class PolarsProfiler:
    def profile(self, df: pl.DataFrame) -> DatasetProfile:
        """
        Profiles the dataset to extract high-level statistics.
        """
        return DatasetProfile(
            row_count=df.height,
            column_count=df.width,
            columns=df.columns,
            missing_cells=df.null_count().sum_horizontal().item(),
            duplicate_rows=df.is_duplicated().sum(),
            memory_usage_mb=df.estimated_size("mb")
        )
