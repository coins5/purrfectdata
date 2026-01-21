from pathlib import Path
from typing import Any
import polars as pl
from purrfect.domain.ports import IDataLoader

class PolarsDataLoader(IDataLoader):
    """
    Concrete implementation of IDataLoader using the Polars library.
    """

    def load(self, path: str) -> pl.DataFrame:
        file_path = Path(path)

        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {path}")

        # Determine file type by extension
        suffix = file_path.suffix.lower()

        try:
            if suffix == ".csv":
                return pl.read_csv(file_path)
            elif suffix == ".json":
                return pl.read_json(file_path)
            else:
                raise ValueError(f"Unsupported file format: {suffix}")
        except Exception as e:
            raise e