from typing import Dict, Any

from app.scoring_strategy import ScoringStrategy


class SchemaTypesScorer(ScoringStrategy):
    """Score the schema and types quality."""

    def __init__(self, spec: Dict[str, Any]):
        super().__init__(spec)
        self.max_score = 20

    def score(self) -> float:
        max_points = self.max_score
        score_one = max_points
        score_two = max_points
        score_three = max_points
        num_schemas = len(self.spec.get('components', {}).get('schemas', {}))
        minus_points_per_bad_schema = max_points / num_schemas if num_schemas > 0 else 0

        # Check schemas in components
        for schema_name, schema in self.spec.get('components', {}).get('schemas', {}).items():
            if not schema.get('type'):
                self.issues.append({
                    'location': f'components.schemas.{schema_name}',
                    'message': 'Schema missing type definition',
                    'severity': 'high'
                })
                score_one -= minus_points_per_bad_schema

        # Check parameters and request bodies
        num_params = 0
        num_bad_params = 0
        num_contents = 0
        num_bad_contents = 0

        for path, path_item in self.spec.get('paths', {}).items():
            for method, operation in path_item.items():
                if method.lower() not in ['get', 'post', 'put', 'patch', 'delete', 'head', 'options', 'trace']:
                    continue

                for param in operation.get('parameters', []):
                    num_params += 1
                    if 'schema' not in param:
                        self.issues.append({
                            'location': f'paths.{path}.{method}.parameters.{param['name']}',
                            'message': 'Parameter missing schema definition',
                            'severity': 'medium'
                        })
                        num_bad_params += 1

                if 'requestBody' in operation:
                    for content_type, content in operation['requestBody'].get('content', {}).items():
                        num_contents += 1
                        if 'schema' not in content:
                            num_bad_contents += 1
                            self.issues.append({
                                'location': f'paths.{path}.{method}.requestBody.content.{content_type}',
                                'message': 'Request body missing schema definition',
                                'severity': 'medium'
                            })

        if num_params != 0:
            minus_points_per_bad_parameter = max_points / num_params
            score_two -= minus_points_per_bad_parameter * num_bad_params

        if num_contents != 0:
            minus_point_per_bad_content = max_points / num_contents
            score_three -= minus_point_per_bad_content * num_bad_contents

        return (score_one + score_two + score_three) / 3