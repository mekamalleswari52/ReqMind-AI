from typing import List, Dict


class AIService:
    """A provider-independent AI service. This is a development/mock implementation.
    Configure a real provider by implementing the same interface and wiring via env vars.
    """

    def analyze_requirement(self, requirement_text: str) -> Dict:
        cleaned = requirement_text.strip()
        lower = cleaned.lower()
        vague_words = [
            word for word in ["fast", "easy", "quick", "user-friendly", "efficient", "appropriate"]
            if word in lower
        ]
        quality_score = 85
        issues = []
        if not cleaned:
            return {
                "requirement_id": None,
                "type": "unknown",
                "quality_score": 0,
                "issues": [{"type": "empty", "message": "Requirement text is empty."}],
                "explanation": "The requirement is empty and needs to be rewritten.",
                "improved_requirement": "The system shall provide a clear, testable requirement statement.",
                "acceptance_criteria": [],
                "test_cases": [],
            }
        if vague_words:
            quality_score -= 20
            issues.append({"type": "vague", "words": vague_words})
        if "shall" not in lower:
            quality_score -= 10
            issues.append({"type": "style", "message": "Requirement should use clear imperative language such as 'shall'."})

        improved_requirement = cleaned
        if not improved_requirement.endswith("."):
            improved_requirement += "."

        acceptance_criteria = [
            "The requirement is testable and observable.",
            "The behavior is specific enough to validate automatically or manually.",
        ]
        test_cases = [
            {
                "title": "Verify requirement behavior",
                "steps": ["Set up the target scenario.", "Execute the requested action.", "Check the expected result."],
                "expected_result": "The system behaves as specified in the requirement.",
            }
        ]

        return {
            "requirement_id": None,
            "type": "functional" if "system" in lower or "shall" in lower else "non-functional",
            "quality_score": max(0, quality_score),
            "issues": issues,
            "explanation": "The requirement is understandable and mostly testable.",
            "improved_requirement": improved_requirement,
            "acceptance_criteria": acceptance_criteria,
            "test_cases": test_cases,
        }

    def analyze_requirements(self, requirements: List[str]) -> List[Dict]:
        results = []
        for i, requirement in enumerate(requirements, start=1):
            result = self.analyze_requirement(requirement)
            result["requirement_id"] = f"R-{i}"
            results.append(result)
        return results

    def improve_requirement(self, requirement_text: str) -> Dict:
        cleaned = requirement_text.strip()
        improved = cleaned if cleaned.endswith(".") else cleaned + "."
        return {
            "improved_requirement": improved,
            "reason": "The statement is clarified to be more testable and measurable.",
        }
