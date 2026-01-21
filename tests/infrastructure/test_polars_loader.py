import pytest
import polars as pl
from purrfect.domain.ports import IDataLoader
from purrfect.infrastructure.polars_loader import PolarsDataLoader

def test_loader_interface_compliance():
    """Ensure PolarsDataLoader implements the IDataLoader protocol."""
    assert issubclass(PolarsDataLoader, IDataLoader)
    loader = PolarsDataLoader()
    assert isinstance(loader, IDataLoader)

def test_polars_csv_loading(tmp_path):
    """Verify that a CSV file is correctly loaded into a Polars DataFrame."""
    csv_file = tmp_path / "test_data.csv"
    csv_content = "id,name\n1,Alice\n2,Bob"
    csv_file.write_text(csv_content, encoding="utf-8")

    loader = PolarsDataLoader()
    df = loader.load(str(csv_file))

    assert isinstance(df, pl.DataFrame)
    assert df.shape == (2, 2)
    assert df["name"][0] == "Alice"
    assert df["id"][1] == 2

def test_polars_json_loading(tmp_path):
    """Verify that a JSON file is correctly loaded into a Polars DataFrame."""
    json_file = tmp_path / "test_data.json"
    json_content = '[{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]'
    json_file.write_text(json_content, encoding="utf-8")

    loader = PolarsDataLoader()
    df = loader.load(str(json_file))

    assert isinstance(df, pl.DataFrame)
    assert df.shape == (2, 2)
    assert df["name"][0] == "Alice"

def test_missing_file():
    """Ensure FileNotFoundError is raised when the file does not exist."""
    loader = PolarsDataLoader()
    
    with pytest.raises(FileNotFoundError) as excinfo:
        loader.load("non_existent_ghost_file.csv")
    assert "File not found" in str(excinfo.value)