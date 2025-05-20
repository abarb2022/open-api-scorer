import unittest
from app.open_api_scorer import (
    OpenAPIScorer,
    SchemaTypesScorer,
    DescriptionsScorer,
    PathsOperationsScorer,
    ResponseCodesScorer,
    ExamplesScorer,
    SecurityScorer,
    BestPracticesScorer
)


class TestSchemaTypesScorer(unittest.TestCase):
    def setUp(self):
        self.spec = {
            'components': {
                'schemas': {
                    'Pet': {'type': 'object'},
                    'User': {}
                }
            },
            'paths': {
                '/pets': {
                    'get': {
                        'parameters': [
                            {'name': 'limit', 'schema': {'type': 'integer'}},
                            {'name': 'offset'}
                        ],
                        'requestBody': {
                            'content': {
                                'application/json': {
                                    'schema': {'type': 'object'}
                                },
                                'application/xml': {}
                            }
                        }
                    }
                }
            }
        }

    def test_score_with_missing_types(self):
        scorer = SchemaTypesScorer(self.spec)
        result = scorer.score()

        self.assertLess(result, scorer.max_score)
        self.assertEqual(len(scorer.issues), 3)

    def test_score_with_all_types_present(self):
        self.spec['components']['schemas']['User']['type'] = 'object'
        self.spec['paths']['/pets']['get']['parameters'][1]['schema'] = {'type': 'integer'}
        self.spec['paths']['/pets']['get']['requestBody']['content']['application/xml']['schema'] = {'type': 'object'}

        scorer = SchemaTypesScorer(self.spec)
        result = scorer.score()

        self.assertEqual(result, scorer.max_score)
        self.assertEqual(len(scorer.issues), 0)


class TestDescriptionsScorer(unittest.TestCase):
    def setUp(self):
        self.spec = {
            'info': {'description': 'API description'},
            'paths': {
                '/pets': {
                    'get': {
                        'description': 'Get pets',
                        'parameters': [
                            {'name': 'limit', 'description': 'Max items'},
                            {'name': 'offset'}
                        ],
                        'responses': {
                            '200': {'description': 'Success'},
                            '400': {}
                        }
                    }
                }
            }
        }

    def test_score_with_missing_descriptions(self):
        scorer = DescriptionsScorer(self.spec)
        result = scorer.score()

        self.assertLess(result, scorer.max_score)
        self.assertEqual(len(scorer.issues), 2)


class TestPathsOperationsScorer(unittest.TestCase):
    def setUp(self):
        self.spec = {
            'paths': {
                '/pets': {
                    'get': {},
                    'post': {}
                },
                '/pets/{id}': {
                    'get': {}

                }
            }
        }

    def test_score_with_missing_operations(self):
        scorer = PathsOperationsScorer(self.spec)
        result = scorer.score()

        self.assertLess(result, scorer.max_score)
        self.assertEqual(len(scorer.issues), 1)


class TestResponseCodesScorer(unittest.TestCase):
    def setUp(self):
        self.spec = {
            'paths': {
                '/pets': {
                    'get': {
                        'responses': {
                            '200': {},
                            '500': {}
                        }
                    },
                    'post': {
                        'responses': {
                            '200': {}
                        }
                    }
                }
            }
        }

    def test_score_with_incorrect_codes(self):
        scorer = ResponseCodesScorer(self.spec)
        result = scorer.score()

        self.assertLess(result, scorer.max_score)
        self.assertEqual(len(scorer.issues), 2)


class TestExamplesScorer(unittest.TestCase):
    def setUp(self):
        self.spec = {
            'paths': {
                '/pets': {
                    'get': {
                        'responses': {
                            '200': {
                                'content': {
                                    'application/json': {
                                        'example': {'id': 1}
                                    },
                                    'application/xml': {}
                                }
                            }
                        }
                    }
                }
            }
        }

    def test_score_with_missing_examples(self):
        scorer = ExamplesScorer(self.spec)
        result = scorer.score()

        self.assertLess(result, scorer.max_score)
        self.assertEqual(len(scorer.issues), 1)


class TestSecurityScorer(unittest.TestCase):
    def test_score_with_no_security(self):
        spec = {}
        scorer = SecurityScorer(spec)
        result = scorer.score()

        self.assertEqual(result, 0)
        self.assertEqual(len(scorer.issues), 1)

    def test_score_with_unused_security(self):
        spec = {
            'components': {
                'securitySchemes': {
                    'apiKey': {'type': 'apiKey'}
                }
            }
        }
        scorer = SecurityScorer(spec)
        result = scorer.score()

        self.assertEqual(result, 3)
        self.assertEqual(len(scorer.issues), 1)


class TestBestPracticesScorer(unittest.TestCase):
    def setUp(self):
        self.spec = {
            'info': {
                'version': '1.0.0'
            },
            'servers': [
                {'url': 'http://api.example.com'}
            ],
            'tags': [
                {'name': 'pets'}
            ]
        }

    def test_score_with_missing_best_practices(self):
        scorer = BestPracticesScorer(self.spec)
        result = scorer.score()

        self.assertLess(result, scorer.max_score)
        self.assertGreater(len(scorer.issues), 0)


class TestOpenAPIScorer(unittest.TestCase):
    def setUp(self):
        self.spec = {
            'openapi': '3.0.0',
            'info': {
                'title': 'Test API',
                'version': '1.0.0',
                'description': 'Test description'
            },
            'paths': {
                '/test': {
                    'get': {
                        'description': 'Test endpoint',
                        'responses': {
                            '200': {
                                'description': 'OK'
                            }
                        }
                    }
                }
            }
        }

    def test_score_all(self):
        scorer = OpenAPIScorer(self.spec)
        results = scorer.score_all()

        self.assertIn('total', results)
        self.assertIn('schema_types', results)
        self.assertIn('descriptions', results)

    def test_calculate_grade(self):
        scorer = OpenAPIScorer({})

        self.assertEqual(scorer._calculate_grade(95), 'A')
        self.assertEqual(scorer._calculate_grade(85), 'B')
        self.assertEqual(scorer._calculate_grade(75), 'C')
        self.assertEqual(scorer._calculate_grade(65), 'D')
        self.assertEqual(scorer._calculate_grade(30), 'F')