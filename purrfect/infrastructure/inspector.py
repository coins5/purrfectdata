import polars as pl
from typing import List
from purrfect.domain.entities import ColumnStats

class PolarsInspector:
    """
    Infrastructure service that collects statistics from a Polars DataFrame.
    """

    def inspect(self, df: pl.DataFrame) -> List[ColumnStats]:
        stats = []
        for col_name in df.columns:
            series = df[col_name]
            
            # Determine basic stats
            dtype = str(series.dtype)
            count = len(series)
            null_count = series.null_count()
            # n_unique is expensive on huge data, but for now we assume manageable size or it's fine.
            n_unique = series.n_unique()

            min_val = None
            max_val = None
            unique_vals = None

            # Type specific stats
            if series.dtype.is_numeric():
                min_val = series.min()
                max_val = series.max()
            
            if series.dtype == pl.String:
                # Capture unique values if cardinality is low enough to likely be an enum
                # Limit to e.g. 50 just to be safe so we don't blow up memory if logic changes
                if n_unique < 50:
                    unique_vals = series.unique().to_list()
            
            stats.append(ColumnStats(
                name=col_name,
                dtype=dtype,
                min_value=min_val,
                max_value=max_val,
                null_count=null_count,
                n_unique=n_unique,
                count=count,
                unique_values=unique_vals
            ))
            
        return stats
