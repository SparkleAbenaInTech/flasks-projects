import json
from datetime import datetime

class AIEvaluator:
    def __init__(self):
        self.test_results = []
    
    def create_test_case(self, test_id, input_text, expected_keywords, category):
        return {'test_id': test_id, 'input': input_text, 'expected_keywords': expected_keywords, 'category': category}
    
    def simulate_ai_response(self, input_text):
        responses = {
            'firewall': 'A firewall monitors network traffic and blocks unauthorized access using security rules.',
            'encryption': 'Encryption uses AES-256 to convert data into secure coded format.',
            'ai safety': 'AI Safety ensures systems behave as intended without causing unintended harm.',
            'rag': 'RAG combines retrieval with generation to answer questions using specific documents.',
        }
        for key in responses:
            if key in input_text.lower():
                return responses[key]
        return 'This is a simulated AI response for evaluation purposes.'
    
    def evaluate_response(self, test_case, actual_response):
        expected = test_case['expected_keywords']
        found = [kw for kw in expected if kw.lower() in actual_response.lower()]
        score = len(found) / len(expected) if expected else 0
        result = {'test_id': test_case['test_id'], 'category': test_case['category'], 'score': round(score, 2), 'passed': score >= 0.7, 'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        self.test_results.append(result)
        return result
    
    def run_regression_test(self, test_suite):
        print("Running regression tests...")
        passed = 0
        for test in test_suite:
            response = self.simulate_ai_response(test['input'])
            result = self.evaluate_response(test, response)
            status = "PASS" if result['passed'] else "FAIL"
            if result['passed']:
                passed += 1
            print(f"  [{status}] {test['test_id']} - Score: {result['score']}")
        return {'passed': passed, 'failed': len(test_suite)-passed, 'total': len(test_suite)}
    
    def generate_report(self):
        total = len(self.test_results)
        passed = sum(1 for r in self.test_results if r['passed'])
        avg_score = sum(r['score'] for r in self.test_results) / total if total > 0 else 0
        return {'total_tests': total, 'passed': passed, 'failed': total-passed, 'pass_rate': f"{round((passed/total)*100, 1)}%", 'average_score': round(avg_score, 2), 'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

evaluator = AIEvaluator()
print("=== AI Evaluation & Regression Testing System ===")
print("Built by Abena Apau - SparkleAbenaInTech\n")

test_suite = [
    evaluator.create_test_case("TC001", "What is a firewall?", ["firewall", "network", "security"], "cybersecurity"),
    evaluator.create_test_case("TC002", "Explain encryption", ["encryption", "AES", "secure"], "cybersecurity"),
    evaluator.create_test_case("TC003", "What is AI safety?", ["AI", "safety", "harm"], "AI"),
    evaluator.create_test_case("TC004", "How does RAG work?", ["RAG", "retrieval", "documents"], "AI"),
    evaluator.create_test_case("TC005", "What is blockchain?", ["blockchain", "distributed", "ledger"], "general"),
]

results = evaluator.run_regression_test(test_suite)
print(f"\nPassed: {results['passed']}/{results['total']}")
report = evaluator.generate_report()
print(f"\n--- Report ---")
print(json.dumps(report, indent=2))
