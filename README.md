# open-api-scorer

### A powerful tool that evaluates your OpenAPI specifications against industry best practices, providing a detailed quality assessment with actionable improvement suggestions.


#### Key Features
##### Comprehensive Scoring
Evaluates your API across 7 critical quality dimensions including schema completeness, documentation quality, and security practices.


##### Actionable Feedback
Provides specific, location-based improvement suggestions with severity indicators to help prioritize fixes.


##### Flexible Integration
Works seamlessly with both local specification files and remote URLs.


##### Validation Pipeline
Automatically verifies OpenAPI spec validity before scoring to ensure accurate results.


#### usage example:
  python -m app.main samples/sample1.json  
#### sample output:
<pre> ```json {
    "schema_types": {
      "score": 18.5,
      "max": 20,
      "issues": [
        {
          "location": "components.schemas.Address",
          "message": "Schema missing type definition",
          "severity": "high"
        }
      ]
    },
    "total": {
      "score": 86.5,
      "max": 100,
      "grade": "B"
    }
  } ``` </pre>
 
  
