from app.scoring_strategy import ScoringStrategy
from typing import Dict, Any


class ResponseCodesScorer(ScoringStrategy):

    def __init__(self, spec: Dict[str, Any]):
        super().__init__(spec)
        self.max_score = 15

    def score(self) -> float:
        max_points = self.max_score
        required_codes = {
            'get': ['200'],
            'post': ['201'],
            'put': ['200'],
            'patch': ['200'],
            'delete': ['204']
        }
        num_methods = 0

        for path, path_item in self.spec.get('paths', {}).items():
            for method, operation in path_item.items():
                num_methods += 1
                method_lower = method.lower()
                if method_lower not in required_codes:
                    continue

                responses = operation.get('responses', {})
                for required_code in required_codes[method_lower]:

                    if required_code not in responses:
                        self.issues.append({
                            'location': f'paths.{path}.{method}.responses',
                            'message': f'Missing expected {required_code} response for {method.upper()}',
                            'severity': 'medium'
                        })

                if '500' not in responses:
                    self.issues.append({
                        'location': f'paths.{path}.{method}.responses',
                        'message': f'Missing 500 error response for {method.upper()}',
                        'severity': 'low'
                    })

        points_per_response = max_points / num_methods if num_methods > 0 else 0
        score = max_points - (len(self.issues) * points_per_response)
        return max(0, round(score, 1))
