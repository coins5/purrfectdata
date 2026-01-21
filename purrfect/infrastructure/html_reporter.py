from pathlib import Path
from typing import List
import importlib.resources
from jinja2 import Template
from purrfect.domain.entities import Hairball, DatasetProfile

from purrfect.domain.scoring import QualityScore

class HTMLReporter:
    def generate_report(self, results: List[Hairball], profile: DatasetProfile, score: QualityScore, output_path: str) -> None:
        """
        Generates an HTML report from the validation results.
        
        Args:
            results: List of Hairball objects found during validation.
            profile: DatasetProfile object containing dataset statistics.
            score: QualityScore object containing the calculated score and grade.
            output_path: The file path where the HTML report should be saved.
        """
        template_content = importlib.resources.files('purrfect.templates').joinpath('report.html').read_text(encoding='utf-8')
        template = Template(template_content)
        html_output = template.render(hairballs=results, profile=profile, score=score)
        
        Path(output_path).write_text(html_output, encoding='utf-8')
