from typing import Dict, Any, List
from abc import ABC, abstractmethod


class ScoringStrategy(ABC):
    def __init__(self, spec: Dict[str, Any]):
        self.spec = spec
        self.max_score = 0
        self.issues = []

    @abstractmethod
    def score(self) -> float:
        pass

    def get_result(self) -> Dict[str, Any]:
        return {
            'score': self.score(),
            'max': self.max_score,
            'issues': self.issues
        }