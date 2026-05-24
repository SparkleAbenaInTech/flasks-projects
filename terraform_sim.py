import json
from datetime import datetime

class TerraformSimulator:
    def __init__(self):
        self.state = {}
        self.plan = []
        self.resources = {}
    
    def define_resource(self, resource_type, name, config):
        resource_id = f"{resource_type}.{name}"
        self.resources[resource_id] = {
            'type': resource_type,
            'name': name,
            'config': config,
            'status': 'planned'
        }
        self.plan.append({
            'action': 'create',
            'resource': resource_id,
            'config': config
        })
        print(f"Planned: {resource_id}")
    
    def apply(self):
        print("\n--- Terraform Apply ---")
        applied = []
        for resource_id, resource in self.resources.items():
            resource['status'] = 'active'
            resource['created_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            resource['id'] = f"aws-{resource_id}-{len(applied)+1}"
            self.state[resource_id] = resource
            applied.append(resource_id)
            print(f"Created: {resource_id}")
        return applied
    
    def show_state(self):
        print("\n--- Current State ---")
        for resource_id, resource in self.state.items():
            print(f"\nResource: {resource_id}")
            print(f"  Status: {resource['status']}")
            print(f"  Created: {resource['created_at']}")
            print(f"  Config: {json.dumps(resource['config'], indent=4)}")
    
    def destroy(self, resource_id):
        if resource_id in self.state:
            del self.state[resource_id]
            print(f"Destroyed: {resource_id}")
        else:
            print(f"Resource not found: {resource_id}")

# Initialize Terraform
tf = TerraformSimulator()

print("=== Terraform Infrastructure as Code Simulation ===")
print("Built by Abena Apau - SparkleAbenaInTech\n")

print("--- Defining Resources ---")

# Define AWS resources
tf.define_resource("aws_vpc", "main", {
    "cidr_block": "10.0.0.0/16",
    "enable_dns": True,
    "tags": {"Name": "SparkleAbena-VPC", "Environment": "Production"}
})

tf.define_resource("aws_subnet", "public", {
    "vpc_id": "aws_vpc.main",
    "cidr_block": "10.0.1.0/24",
    "availability_zone": "us-east-1a",
    "tags": {"Name": "Public-Subnet"}
})

tf.define_resource("aws_security_group", "ai_app", {
    "name": "ai-application-sg",
    "description": "Security group for AI application",
    "ingress": [
        {"port": 443, "protocol": "tcp", "description": "HTTPS"},
        {"port": 80, "protocol": "tcp", "description": "HTTP"}
    ],
    "egress": [
        {"port": 0, "protocol": "-1", "description": "All outbound"}
    ]
})

tf.define_resource("aws_instance", "ai_server", {
    "ami": "ami-0c55b159cbfafe1f0",
    "instance_type": "t3.medium",
    "security_groups": ["aws_security_group.ai_app"],
    "tags": {"Name": "SparkleAbena-AI-Server", "Role": "AI-Engineering"}
})

tf.define_resource("aws_s3_bucket", "ai_data", {
    "bucket": "sparkleabena-ai-data",
    "versioning": True,
    "encryption": "AES-256",
    "tags": {"Name": "AI-Data-Bucket"}
})

# Apply the infrastructure
tf.apply()

# Show current state
tf.show_state()

print("\n--- Infrastructure Summary ---")
print(f"Total resources deployed: {len(tf.state)}")
print(f"Status: All systems operational")
print(f"\nThis is exactly what Terraform does in real AWS environments!")
print(f"Infrastructure as Code means your entire cloud setup is version controlled!")