import json
from app.open_api_scorer import OpenAPIScorer
from app.validator import OpenAPIValidator

def main():
    # if len(sys.argv) != 2:
    #     print("Usage: python -m app.main <path_to_json_file>")
    #     sys.exit(1)
    #
    # source = Path(sys.argv[1])
    source = 'https://petstore3.swagger.io/api/v3/openapi.json'

    spec, load_error = OpenAPIValidator.load_openapi_spec(source)

    if load_error:
        print(f"Load error: {load_error}")
    else:
        errors = OpenAPIValidator.validate_spec_dict(spec)
        if errors:
            print("Validation errors:")
            for e in errors:
                print(f" - {e}")
        else:
            print("OpenAPI spec loaded and validated successfully!")

    scorer = OpenAPIScorer(spec)
    results = scorer.score_all()
    print(json.dumps(results, indent=2))


if __name__ == '__main__':
    main()