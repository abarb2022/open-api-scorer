from typing import Dict, Any

from app.scoring_strategy import ScoringStrategy


class PathsOperationsScorer(ScoringStrategy):
    def __init__(self, spec: Dict[str, Any]):
        super().__init__(spec)
        self.max_score = 15

    def score(self) -> float:
        max_points = self.max_score
        score = max_points
        paths = self.spec.get('paths', {})
        path_names = list(paths.keys())

        # Check for consistent naming
        inconsistent_names = any('_' in path for path in path_names) or any(' ' in path for path in path_names)
        if inconsistent_names:
            self.issues.append({
                'location': 'paths',
                'message': 'Inconsistent path naming',
                'severity': 'low'
            })
            score -= 1

        crud_methods = {'get', 'post', 'put', 'patch', 'delete'}
        for path, path_item in paths.items():
            methods = set(m.lower() for m in path_item.keys() if m.lower() in crud_methods)

            if not path.endswith('}') and not methods.issuperset({'get', 'post'}):
                self.issues.append({
                    'location': f'paths.{path}',
                    'message': 'would be better if it had both get,post methods',
                    'severity': 'medium'
                })

            if path.endswith('}') and not methods.issuperset({'get', 'put', 'delete'}):
                self.issues.append({
                    'location': f'paths.{path}',
                    'message': 'would be better if it had get,post,delete methods',
                    'severity': 'medium'
                })

        score -= len(self.issues) * (max_points / len(path_names)) if path_names else 0
        return max(0, score)