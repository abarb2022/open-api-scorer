
from typing import Dict, Any
from app.scoring_strategy import ScoringStrategy


class BestPracticesScorer(ScoringStrategy):
    """Score miscellaneous best practices."""

    def __init__(self, spec: Dict[str, Any]):
        super().__init__(spec)
        self.max_score = 10

    def score(self) -> float:
        max_points = self.max_score
        score = 0

        if 'servers' in self.spec and len(self.spec['servers']) > 0:
            score += 2
            for i, server in enumerate(self.spec['servers']):
                if not server.get('description'):
                    self.issues.append({
                        'location': f'servers[{i}]',
                        'message': 'Server entry missing description',
                        'severity': 'low'
                    })
        else:
            self.issues.append({
                'location': 'servers',
                'message': 'No servers defined',
                'severity': 'medium'
            })

        if self.spec.get('info', {}).get('version'):
            score += 2
        else:
            self.issues.append({
                'location': 'info',
                'message': 'No API version specified',
                'severity': 'medium'
            })

        if 'tags' in self.spec and len(self.spec['tags']) > 0:
            score += 2
            for i, tag in enumerate(self.spec['tags']):
                if not tag.get('description'):
                    self.issues.append({
                        'location': f'tags[{i}]',
                        'message': 'Tag missing description',
                        'severity': 'low'
                    })
        else:
            self.issues.append({
                'location': 'tags',
                'message': 'No tags defined',
                'severity': 'low'
            })

        components = self.spec.get('components', {})
        if any(components.values()):
            score += 2
            schemas_used = False
            for path, path_item in self.spec.get('paths', {}).items():
                for method, operation in path_item.items():
                    if method.lower() not in ['get', 'post', 'put', 'patch', 'delete']:
                        continue

                    for param in operation.get('parameters', []):
                        if '$ref' in param.get('schema', {}):
                            schemas_used = True

                    if 'requestBody' in operation:
                        for content in operation['requestBody'].get('content', {}).values():
                            if '$ref' in content.get('schema', {}):
                                schemas_used = True

                    for response in operation.get('responses', {}).values():
                        for content in response.get('content', {}).values():
                            if '$ref' in content.get('schema', {}):
                                schemas_used = True

            if not schemas_used and 'schemas' in components:
                self.issues.append({
                    'location': 'components.schemas',
                    'message': 'Schemas defined but not referenced',
                    'severity': 'medium'
                })
                score -= 1
        else:
            self.issues.append({
                'location': 'components',
                'message': 'No components defined',
                'severity': 'low'
            })

        if self.spec.get('info', {}).get('contact'):
            score += 2
        else:
            self.issues.append({
                'location': 'info.contact',
                'message': 'No contact information provided',
                'severity': 'low'
            })

        return min(score, max_points)