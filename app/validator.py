import json
import yaml
import urllib.request
from pathlib import Path
from typing import Union



class OpenAPIValidator:
    @staticmethod
    def validate_spec_dict(spec: dict) -> list[str]:
        """
        Validate a parsed OpenAPI spec dictionary (JSON or YAML).
        Returns: list of error messages
        """
        errors = []

        if not isinstance(spec, dict):
            return ["Spec must be a dictionary"]

        if 'openapi' not in spec:
            errors.append("Missing 'openapi' field")
        elif not spec['openapi'].startswith('3.'):
            errors.append("Only OpenAPI 3.x is supported")

        if 'info' not in spec:
            errors.append("Missing 'info' section")
        else:
            if 'title' not in spec['info']:
                errors.append("Missing 'info.title'")
            if 'version' not in spec['info']:
                errors.append("Missing 'info.version'")

        if 'paths' not in spec:
            errors.append("Missing 'paths' section")

        return errors

    def load_openapi_spec(source: Union[str, Path]) -> tuple[dict | None, str | None]:
        """
        Load an OpenAPI 3.x spec (YAML or JSON) from local file or URL.
        Returns: (parsed_spec_dict, error) — error is None if successful
        """
        try:
            if str(source).startswith(('http://', 'https://')):
                with urllib.request.urlopen(source) as response:
                    content = response.read().decode('utf-8')
                    content_type = response.headers.get('Content-Type', '')
            else:
                path = Path(source)
                if not path.exists():
                    return None, f"File not found: {path}"
                content = path.read_text()
                content_type = path.suffix

            if 'json' in content_type or str(source).endswith('.json'):
                spec = json.loads(content)
            else:
                spec = yaml.safe_load(content)

            return spec, None

        except Exception as e:
            return None, f"Failed to load : {e}"

