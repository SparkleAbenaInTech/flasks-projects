import json
import numpy as np
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

class RAGSystem:
    def __init__(self):
        self.documents = []
        self.index = []
    
    def add_document(self, title, content, category):
        doc = {'id': len(self.documents), 'title': title, 'content': content, 'category': category}
        self.documents.append(doc)
        self.index.append(self.text_to_vector(content))
    
    def text_to_vector(self, text):
        vector = np.zeros(100)
        for i, char in enumerate(text.lower()):
            vector[i % 100] += ord(char)
        norm = np.linalg.norm(vector)
        return vector / (norm + 1e-9)
    
    def search(self, query, top_k=3):
        if not self.documents:
            return []
        query_vector = self.text_to_vector(query)
        scores = [(np.dot(query_vector, doc_vector), i) for i, doc_vector in enumerate(self.index)]
        scores.sort(reverse=True)
        return [{'title': self.documents[idx]['title'], 'content': self.documents[idx]['content'], 'category': self.documents[idx]['category'], 'relevance_score': round(float(score), 4)} for score, idx in scores[:top_k]]
    
    def answer(self, query):
        results = self.search(query)
        if not results:
            return "No relevant documents found."
        answer = "Based on my knowledge base, here is what I found:\n\n"
        for i, r in enumerate(results, 1):
            answer += f"{i}. [{r['title']}]\n{r['content']}\n\n"
        return answer

rag = RAGSystem()
rag.add_document("Firewall Basics", "A firewall monitors and controls network traffic based on security rules.", "cybersecurity")
rag.add_document("Encryption", "Encryption converts data into a coded format. AES-256 is the gold standard used by banks and governments.", "cybersecurity")
rag.add_document("Zero Trust Security", "Zero Trust means never trust always verify. Every user must be authenticated regardless of location.", "cybersecurity")
rag.add_document("AI Safety", "AI Safety research focuses on ensuring AI systems behave as intended and do not cause unintended harm.", "AI")
rag.add_document("Vector Databases", "Vector databases store data as mathematical embeddings enabling semantic search based on meaning.", "AI")
rag.add_document("RAG Systems", "Retrieval Augmented Generation combines search with language models to answer questions using specific documents.", "AI")

@app.route('/')
def home():
    return jsonify({'message': 'RAG System API by SparkleAbenaInTech', 'documents': len(rag.documents), 'status': 'ready'})

@app.route('/search', methods=['POST'])
def search():
    data = request.get_json()
    query = data.get('query', '')
    if not query:
        return jsonify({'error': 'No query provided'}), 400
    return jsonify({'query': query, 'results': rag.search(query)})

@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    query = data.get('question', '')
    if not query:
        return jsonify({'error': 'No question provided'}), 400
    return jsonify({'question': query, 'answer': rag.answer(query)})

if __name__ == '__main__':
    app.run(debug=True)
