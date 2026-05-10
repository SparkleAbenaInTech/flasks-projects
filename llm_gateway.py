import time
import json
from datetime import datetime
from collections import defaultdict

class LLMGateway:
    def __init__(self):
        self.request_counts = defaultdict(list)
        self.rate_limit = 10  # max requests per minute
        self.request_log = []
        self.models = {
            'fast': 'claude-haiku',
            'balanced': 'claude-sonnet', 
            'powerful': 'claude-opus'
        }
    
    def check_rate_limit(self, user_id):
        now = time.time()
        minute_ago = now - 60
        
        # Remove requests older than 1 minute
        self.request_counts[user_id] = [
            t for t in self.request_counts[user_id] 
            if t > minute_ago
        ]
        
        # Check if over limit
        if len(self.request_counts[user_id]) >= self.rate_limit:
            return False, f"Rate limit exceeded. Max {self.rate_limit} requests per minute."
        
        self.request_counts[user_id].append(now)
        return True, "OK"
    
    def route_request(self, prompt, priority='balanced'):
        # Route to different models based on priority
        if len(prompt) < 100:
            model = self.models['fast']
            reason = "Short prompt - routing to fast model"
        elif priority == 'powerful' or '?' in prompt:
            model = self.models['powerful']
            reason = "Complex query - routing to powerful model"
        else:
            model = self.models['balanced']
            reason = "Standard query - routing to balanced model"
        
        return model, reason
    
    def process_request(self, user_id, prompt, priority='balanced'):
        # Check rate limit
        allowed, message = self.check_rate_limit(user_id)
        if not allowed:
            return {
                'status': 'error',
                'message': message,
                'user_id': user_id
            }
        
        # Route to appropriate model
        model, routing_reason = self.route_request(prompt, priority)
        
        # Log the request
        log_entry = {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'user_id': user_id,
            'model': model,
            'routing_reason': routing_reason,
            'prompt_length': len(prompt),
            'priority': priority
        }
        self.request_log.append(log_entry)
        
        return {
            'status': 'success',
            'user_id': user_id,
            'model_selected': model,
            'routing_reason': routing_reason,
            'requests_this_minute': len(self.request_counts[user_id]),
            'rate_limit': self.rate_limit
        }
    
    def get_observability_report(self):
        # This is the observability concept from the job posting!
        total_requests = len(self.request_log)
        model_usage = defaultdict(int)
        
        for log in self.request_log:
            model_usage[log['model']] += 1
        
        return {
            'total_requests': total_requests,
            'model_usage': dict(model_usage),
            'active_users': len(self.request_counts),
            'recent_requests': self.request_log[-3:] if self.request_log else []
        }

# Test our LLM Gateway
gateway = LLMGateway()

print("=== LLM Gateway Simulation ===\n")

# Simulate different users making requests
test_requests = [
    ("user_abena", "Hi!", "balanced"),
    ("user_abena", "What is machine learning and how does it work in enterprise AI systems?", "powerful"),
    ("user_abena", "Tell me about Python", "balanced"),
    ("user_bob", "How do vector databases work?", "balanced"),
    ("user_bob", "Explain RAG", "fast"),
    ("user_abena", "What is cybersecurity?", "balanced"),
]

for user_id, prompt, priority in test_requests:
    result = gateway.process_request(user_id, prompt, priority)
    print(f"User: {user_id}")
    print(f"Prompt: {prompt[:50]}...")
    print(f"Status: {result['status']}")
    if result['status'] == 'success':
        print(f"Model: {result['model_selected']}")
        print(f"Reason: {result['routing_reason']}")
        print(f"Requests this minute: {result['requests_this_minute']}/{result['rate_limit']}")
    else:
        print(f"Error: {result['message']}")
    print("---")

print("\n=== Observability Report ===")
report = gateway.get_observability_report()
print(json.dumps(report, indent=2))