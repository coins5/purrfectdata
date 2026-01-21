from typing import Protocol, Any, runtime_checkable

@runtime_checkable
class IDataLoader(Protocol):
    """
    Domain interface for loading data.
    Decouples the application layer from specific data engines (e.g., Polars, Pandas).
    """

    def load(self, path: str) -> Any:
        """
        Load data from a given file path.

        :param path: The absolute or relative path to the file.
        :return: The loaded data (typically a DataFrame, typed as Any to avoid leaking implementation details).
        """
        ...