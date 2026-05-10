import numpy as np
import json

# This simulates how vector databases work
# In real apps you'd use Pinecone or similar

class SimpleVectorDB:
    def __init__(self):
        self.documents = []
        self.metadata = []
    
    def add_document(self, text, metadata={}):
        # Simulate embedding by converting text to numbers
        vector = self.text_to_vector(text)
        self.documents.append(vector)
        self.metadata.append({
            'text': text,
            'metadata': metadata
        })
        print(f"Added document: {text[:50]}...")
    
    def text_to_vector(self, text):
        # Simple simulation of text embeddings
        vector = np.zeros(100)
        for i, char in enumerate(text.lower()):
            vector[i % 100] += ord(char)
        return vector / (np.linalg.norm(vector) + 1e-9)
    
    def search(self, query, top_k=3):
        if not self.documents:
            return []
        
        query_vector = self.text_to_vector(query)
        
        # Calculate similarity scores
        scores = []
        for i, doc_vector in enumerate(self.documents):
            similarity = np.dot(query_vector, doc_vector)
            scores.append((similarity, i))
        
        # Sort by similarity
        scores.sort(reverse=True)
        
        # Return top results
        results = []
        for score, idx in scores[:top_k]:
            results.append({
                'text': self.metadata[idx]['text'],
                'metadata': self.metadata[idx]['metadata'],
                'similarity_score': round(float(score), 4)
            })
        return results

# Create our knowledge base
db = SimpleVectorDB()

# Add cybersecurity knowledge
db.add_document(
    "A firewall is a network security system that monitors and controls incoming and outgoing network traffic based on predetermined security rules.",
    {"category": "cybersecurity", "topic": "firewall"}
)

db.add_document(
    "Phishing is a type of social engineering attack where attackers disguise themselves as trustworthy entities to steal sensitive information.",
    {"category": "cybersecurity", "topic": "phishing"}
)

db.add_document(
    "Encryption is the process of converting data into a coded format that can only be read by someone with the correct decryption key.",
    {"category": "cybersecurity", "topic": "encryption"}
)

db.add_document(
    "A VPN or Virtual Private Network creates a secure encrypted connection over a less secure network such as the internet.",
    {"category": "cybersecurity", "topic": "VPN"}
)

db.add_document(
    "Multi-factor authentication adds an extra layer of security by requiring users to provide two or more verification factors to gain access.",
    {"category": "cybersecurity", "topic": "MFA"}
)

# Add AI knowledge
db.add_document(
    "Large Language Models or LLMs are AI systems trained on massive amounts of text data that can generate human-like text responses.",
    {"category": "AI", "topic": "LLMs"}
)

db.add_document(
    "Vector databases store data as mathematical vectors enabling fast similarity search which is essential for AI applications.",
    {"category": "AI", "topic": "vector databases"}
)

db.add_document(
    "RAG or Retrieval Augmented Generation combines vector search with LLMs to answer questions using your own documents.",
    {"category": "AI", "topic": "RAG"}
)

print("\n--- Knowledge Base Ready ---")
print(f"Total documents: {len(db.documents)}")

# Test searches
print("\n--- Search Results ---")

queries = [
    "How do I protect my network?",
    "What is artificial intelligence?",
    "How does encryption work?"
]

for query in queries:
    print(f"\nQuery: {query}")
    results = db.search(query, top_k=2)
    for r in results:
        print(f"  Score: {r['similarity_score']} | {r['text'][:80]}...")