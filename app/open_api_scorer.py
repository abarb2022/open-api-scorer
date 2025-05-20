from typing import Dict, Any

from app.best_practices_scorer import BestPracticesScorer
from app.descriptions_scorer import DescriptionsScorer
from app.examples_scorer import ExamplesScorer
from app.paths_operations_scorer import PathsOperationsScorer
from app.response_codes_scorer import ResponseCodesScorer
from app.schema_types_scorer import SchemaTypesScorer
from app.security_scorer import SecurityScorer


class OpenAPIScorer:
    def __init__(self, spec: Dict[str, Any]):
        if not isinstance(spec, dict):
            raise ValueError("Spec must be a dictionary")

        self.spec = spec
        self.scorers = {
            'schema_types': SchemaTypesScorer(spec),
            'descriptions': DescriptionsScorer(spec),
            'paths_operations': PathsOperationsScorer(spec),
            'response_codes': ResponseCodesScorer(spec),
            'examples': ExamplesScorer(spec),
            'security': SecurityScorer(spec),
            'best_practices': BestPracticesScorer(spec)
        }

    def score_all(self) -> Dict[str, Any]:
        results = {}

        for name, scorer in self.scorers.items():
            results[name] = scorer.get_result()

        total = sum(category['score'] for category in results.values())
        percentage = round((total / 100) * 100, 1)

        results['total'] = {
            'score': round(total, 1),
            'max': 100,
            'grade': self._calculate_grade(percentage)
        }

        return results

    def _calculate_grade(self, percentage: float) -> str:
        if percentage >= 91:
            return 'A'
        elif percentage >= 81:
            return 'B'
        elif percentage >= 71:
            return 'C'
        elif percentage >= 61:
            return 'D'
        elif percentage >= 51:
            return 'D'
        else:
            return 'F'