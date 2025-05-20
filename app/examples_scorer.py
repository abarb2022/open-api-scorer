from app.scoring_strategy import ScoringStrategy
from typing import Dict, Any


class ExamplesScorer(ScoringStrategy):
    def __init__(self, spec: Dict[str, Any]):
        super().__init__(spec)
        self.max_score = 10

    def score(self) -> float:
        max_points = self.max_score
        score = 0
        points_per_example = 1

        for path, path_item in self.spec.get('paths', {}).items():
            for method, operation in path_item.items():
                if method.lower() not in ['get', 'post', 'put', 'patch', 'delete']:
                    continue

                # Check response examples
                responses = operation.get('responses', {})
                for code, response in responses.items():
                    for content_type, content in response.get('content', {}).items():
                        if 'example' in content or 'examples' in content:
                            score += points_per_example
                        else:
                            self.issues.append({
                                'location': f'paths.{path}.{method}.responses.{code}.content.{content_type}',
                                'message': 'Missing response example',
                                'severity': 'low'
                            })

                # Check request body examples
                if 'requestBody' in operation:
                    for content_type, content in operation['requestBody'].get('content', {}).items():
                        if 'example' in content or 'examples' in content:
                            score += points_per_example
                        else:
                            self.issues.append({
                                'location': f'paths.{path}.{method}.requestBody.content.{content_type}',
                                'message': 'Missing request example',
                                'severity': 'low'
                            })

        point_per_element = max_points / (score + len(self.issues)) if (score + len(self.issues)) > 0 else 0
        minus_points = point_per_element * len(self.issues)
        return max(0, max_points - minus_points)