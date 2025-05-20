from app.scoring_strategy import ScoringStrategy
from typing import Dict, Any


class SecurityScorer(ScoringStrategy):

    def __init__(self, spec: Dict[str, Any]):
        super().__init__(spec)
        self.max_score = 10

    def score(self) -> float:
        max_points = self.max_score
        score = 0

        security_schemes = self.spec.get('components', {}).get('securitySchemes', {})
        if security_schemes:
            score += 3

            global_security = self.spec.get('security', [])
            security_used = bool(global_security)

            for path, path_item in self.spec.get('paths', {}).items():
                for method, operation in path_item.items():
                    if method.lower() not in ['get', 'post', 'put', 'patch', 'delete']:
                        continue
                    if operation.get('security') is not None:
                        security_used = True

            if security_used:
                score += 7
            else:
                self.issues.append({
                    'location': 'security',
                    'message': 'Security schemes defined but not used',
                    'severity': 'high'
                })
        else:
            self.issues.append({
                'location': 'components.securitySchemes',
                'message': 'No security schemes defined',
                'severity': 'high'
            })

        return score