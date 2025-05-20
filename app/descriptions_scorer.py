from app.scoring_strategy import ScoringStrategy
from typing import Dict, Any


class DescriptionsScorer(ScoringStrategy):
    """Check that all elements have descriptions."""

    def __init__(self, spec: Dict[str, Any]):
        super().__init__(spec)
        self.max_score = 20

    def score(self) -> float:
        max_points = self.max_score
        total_elements = 0

        # Check info description
        if not self.spec.get('info', {}).get('description'):
            self.issues.append({
                'location': 'info',
                'message': 'API missing general description',
                'severity': 'medium'
            })

        # Check paths and operations
        for path, path_item in self.spec.get('paths', {}).items():
            for method, operation in path_item.items():
                total_elements += 1
                if method.lower() not in ['get', 'post', 'put', 'patch', 'delete', 'head', 'options', 'trace']:
                    continue

                if not operation.get('description'):
                    self.issues.append({
                        'location': f'paths.{path}',
                        'message': 'Path missing description',
                        'severity': 'medium'
                    })

                # Check parameters
                for param in operation.get('parameters', []):
                    total_elements += 1
                    if not param.get('description'):
                        self.issues.append({
                            'location': f'paths.{path}.{method}.parameters.{param['name']}',
                            'message': 'Parameter missing description',
                            'severity': 'low'
                        })

                # Check request body
                if 'requestBody' in operation and not operation['requestBody'].get('description'):
                    self.issues.append({
                        'location': f'paths.{path}.{method}.requestBody',
                        'message': 'Request body missing description',
                        'severity': 'medium'
                    })

                # Check responses
                for resp_code, response in operation.get('responses', {}).items():
                    total_elements += 1
                    if not response.get('description'):
                        self.issues.append({
                            'location': f'paths.{path}.{method}.responses.{resp_code}',
                            'message': 'Response missing description',
                            'severity': 'medium'
                        })

        points_per_element = max_points / total_elements if total_elements > 0 else 0
        score = max_points - (len(self.issues) * points_per_element)
        return max(0, score)