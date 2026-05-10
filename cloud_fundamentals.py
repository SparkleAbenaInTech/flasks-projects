import json
import uuid
from datetime import datetime

# Simulating AWS IAM and Cloud Fundamentals
# This teaches you the concepts without needing an AWS account

class IAMSystem:
    """Identity and Access Management - controls WHO can do WHAT"""
    
    def __init__(self):
        self.users = {}
        self.roles = {}
        self.policies = {}
        self.audit_log = []
    
    def create_policy(self, policy_name, permissions):
        policy_id = str(uuid.uuid4())[:8]
        self.policies[policy_name] = {
            'id': policy_id,
            'name': policy_name,
            'permissions': permissions,
            'created': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        print(f"Policy created: {policy_name}")
        return policy_id
    
    def create_role(self, role_name, policies):
        role_id = str(uuid.uuid4())[:8]
        self.roles[role_name] = {
            'id': role_id,
            'name': role_name,
            'policies': policies,
            'created': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        print(f"Role created: {role_name}")
        return role_id
    
    def create_user(self, username, role):
        user_id = str(uuid.uuid4())[:8]
        self.users[username] = {
            'id': user_id,
            'username': username,
            'role': role,
            'created': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        print(f"User created: {username} with role {role}")
        return user_id
    
    def check_permission(self, username, action, resource):
        if username not in self.users:
            self._log(username, action, resource, 'DENIED', 'User not found')
            return False, "User not found"
        
        user = self.users[username]
        role_name = user['role']
        
        if role_name not in self.roles:
            self._log(username, action, resource, 'DENIED', 'Role not found')
            return False, "Role not found"
        
        role = self.roles[role_name]
        
        for policy_name in role['policies']:
            if policy_name in self.policies:
                policy = self.policies[policy_name]
                if action in policy['permissions']:
                    self._log(username, action, resource, 'ALLOWED', f"Via policy: {policy_name}")
                    return True, f"Access granted via {policy_name}"
        
        self._log(username, action, resource, 'DENIED', 'No matching policy')
        return False, "Access denied - no matching policy"
    
    def _log(self, username, action, resource, result, reason):
        self.audit_log.append({
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'username': username,
            'action': action,
            'resource': resource,
            'result': result,
            'reason': reason
        })
    
    def get_audit_report(self):
        return self.audit_log


class KMSSystem:
    """Key Management System - handles encryption keys"""
    
    def __init__(self):
        self.keys = {}
    
    def create_key(self, key_name, key_type='AES-256'):
        key_id = str(uuid.uuid4())
        self.keys[key_name] = {
            'id': key_id,
            'name': key_name,
            'type': key_type,
            'status': 'ACTIVE',
            'created': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        print(f"KMS Key created: {key_name} ({key_type})")
        return key_id
    
    def encrypt(self, key_name, data):
        if key_name not in self.keys:
            return None, "Key not found"
        if self.keys[key_name]['status'] != 'ACTIVE':
            return None, "Key is not active"
        encrypted = f"ENCRYPTED[{self.keys[key_name]['id'][:8]}]:{data[::-1]}"
        return encrypted, "Success"
    
    def decrypt(self, key_name, encrypted_data):
        if key_name not in self.keys:
            return None, "Key not found"
        data = encrypted_data.split(':', 1)[1][::-1]
        return data, "Success"


class LambdaSimulator:
    """Lambda Functions - serverless compute"""
    
    def __init__(self):
        self.functions = {}
        self.executions = []
    
    def register_function(self, function_name, handler):
        self.functions[function_name] = {
            'name': function_name,
            'handler': handler,
            'created': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        print(f"Lambda function registered: {function_name}")
    
    def invoke(self, function_name, event={}):
        if function_name not in self.functions:
            return {'error': 'Function not found'}
        
        start = datetime.now()
        result = self.functions[function_name]['handler'](event)
        end = datetime.now()
        duration = (end - start).microseconds / 1000
        
        execution = {
            'function': function_name,
            'timestamp': start.strftime('%Y-%m-%d %H:%M:%S'),
            'duration_ms': duration,
            'status': 'SUCCESS'
        }
        self.executions.append(execution)
        print(f"Lambda invoked: {function_name} ({duration}ms)")
        return result


# ============ DEMO ============
print("=" * 50)
print("AWS Cloud Fundamentals Simulation")
print("Built by Abena Apau - SparkleAbenaInTech")
print("=" * 50)

# Setup IAM
print("\n--- IAM Setup ---")
iam = IAMSystem()

iam.create_policy("AIReadPolicy", ["read:models", "read:data"])
iam.create_policy("AIWritePolicy", ["write:models", "write:data", "read:models", "read:data"])
iam.create_policy("AdminPolicy", ["read:models", "write:models", "read:data", "write:data", "delete:data", "manage:users"])

iam.create_role("AIEngineer", ["AIReadPolicy", "AIWritePolicy"])
iam.create_role("DataScientist", ["AIReadPolicy"])
iam.create_role("Admin", ["AdminPolicy"])

iam.create_user("abena", "AIEngineer")
iam.create_user("bob", "DataScientist")
iam.create_user("admin", "Admin")

print("\n--- Permission Checks ---")
checks = [
    ("abena", "write:models", "AI Model Repository"),
    ("bob", "write:models", "AI Model Repository"),
    ("abena", "delete:data", "Training Dataset"),
    ("admin", "delete:data", "Training Dataset"),
    ("unknown_user", "read:models", "AI Models"),
]

for username, action, resource in checks:
    allowed, message = iam.check_permission(username, action, resource)
    status = "✅ ALLOWED" if allowed else "❌ DENIED"
    print(f"{status} | {username} -> {action} on {resource}")
    print(f"         Reason: {message}")

# Setup KMS
print("\n--- KMS Encryption ---")
kms = KMSSystem()
kms.create_key("ai-model-key", "AES-256")
kms.create_key("user-data-key", "AES-256")

secret_data = "API_KEY=sk-abena-super-secret-12345"
encrypted, status = kms.encrypt("ai-model-key", secret_data)
print(f"Original: {secret_data}")
print(f"Encrypted: {encrypted}")

decrypted, status = kms.decrypt("ai-model-key", encrypted)
print(f"Decrypted: {decrypted}")

# Setup Lambda
print("\n--- Lambda Functions ---")
lambda_sim = LambdaSimulator()

def process_ai_request(event):
    return {
        'model': 'claude-sonnet',
        'response': f"Processed: {event.get('prompt', 'No prompt')}",
        'tokens': 150
    }

def resize_image(event):
    return {
        'original_size': event.get('size', '1080p'),
        'new_size': '720p',
        'status': 'resized'
    }

lambda_sim.register_function("processAIRequest", process_ai_request)
lambda_sim.register_function("resizeImage", resize_image)

result1 = lambda_sim.invoke("processAIRequest", {"prompt": "Explain vector databases"})
result2 = lambda_sim.invoke("resizeImage", {"size": "4K"})

print(f"AI Result: {json.dumps(result1, indent=2)}")

print("\n--- Audit Log ---")
for log in iam.get_audit_report()[:3]:
    print(f"{log['result']} | {log['username']} | {log['action']} | {log['reason']}")

print("\n✅ Cloud Fundamentals Complete!")
print("You now understand IAM, KMS, and Lambda!")