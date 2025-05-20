import unittest
from app.open_api_scorer import OpenAPIScorer


class TestIntegrationWithDeficientSpec(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.deficient_spec = {
            "openapi": "3.0.0",
            "info": {
                "title": "Deficient API",
                "version": "1.0"
            },
            "paths": {
                "/users": {
                    "get": {
                        "responses": {
                            "200": {
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "type": "object",
                                            "properties": {
                                                "id": {"type": "string"}
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    },
                    "post": {
                        "responses": {
                            "200": {}
                        }
                    }
                },
                "/users/{id}": {
                    "get": {},
                }
            },
        }

    def test_scorer_detects_all_known_deficiencies(self):
        scorer = OpenAPIScorer(self.deficient_spec)
        results = scorer.score_all()

        # Verify total score is low
        self.assertLess(results['total']['score'], 50)

        # Descriptions checks
        desc_issues = results['descriptions']['issues']
        self.assertTrue(any("missing description" in issue['message']
                            for issue in desc_issues))
        self.assertGreater(len(desc_issues), 3)

        # Paths Operations checks
        paths_issues = results['paths_operations']['issues']
        self.assertTrue(any("would be better if it had" in issue['message']
                            for issue in paths_issues))

        # Response Codes checks
        resp_issues = results['response_codes']['issues']
        self.assertTrue(any("Missing expected 201 response" in issue['message']
                            for issue in resp_issues))

        # Examples checks
        examples_issues = results['examples']['issues']
        self.assertTrue(any("Missing response example" in issue['message']
                            for issue in examples_issues))

        # Security checks
        security_issues = results['security']['issues']
        self.assertTrue(any("No security schemes defined" in issue['message']
                            for issue in security_issues))

        # Best Practices checks
        bp_issues = results['best_practices']['issues']
        self.assertTrue(any("No servers defined" in issue['message']
                            for issue in bp_issues))
        self.assertTrue(any("No tags defined" in issue['message']
                            for issue in bp_issues))

