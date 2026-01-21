from purrfect.domain.inference import RuleInferer
from purrfect.infrastructure.inspector import PolarsInspector
from purrfect.infrastructure.polars_loader import PolarsDataLoader
from purrfect.infrastructure.yaml_parser import YamlParser

class DiscoveryService:
    """
    Application service that coordinates the discovery of data quality rules.
    """
    def __init__(self):
        # In a real DI framework these would be injected.
        self.loader = PolarsDataLoader()
        self.inspector = PolarsInspector()
        self.inferer = RuleInferer()
        self.parser = YamlParser()

    def run(self, file_path: str, output_path: str):
        # 1. Load Data
        df = self.loader.load(file_path)

        # 2. Inspect Data
        stats = self.inspector.inspect(df)

        # 3. Infer Rules
        rules = self.inferer.infer(stats)

        # 4. Save Rules
        self.parser.dump(rules, output_path)

        return rules
