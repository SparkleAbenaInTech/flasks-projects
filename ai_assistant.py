from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)

class AIAssistant:
    def __init__(self):
        self.conversation_history = []
        self.knowledge = {
            'python': 'Python is a versatile programming language great for AI and backend development.',
            'flask': 'Flask is a lightweight Python web framework for building APIs.',
            'react': 'React is a JavaScript library for building interactive user interfaces.',
            'cybersecurity': 'Cybersecurity protects systems and networks from digital attacks.',
            'ai': 'Artificial Intelligence enables machines to learn and make decisions like humans.',
            'rag': 'RAG combines document retrieval with AI generation to answer specific questions.',
            'vector': 'Vector databases store data as mathematical embeddings for semantic search.',
        }

    def respond(self, message):
        message_lower = message.lower()
        self.conversation_history.append({'role': 'user', 'message': message, 'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')})
        response = None
        for keyword, answer in self.knowledge.items():
            if keyword in message_lower:
                response = answer
                break
        if not response:
            response = f"I received your message: '{message}'. I am SparkleAbenaInTech AI Assistant!"
        self.conversation_history.append({'role': 'assistant', 'message': response, 'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')})
        return response

    def get_history(self):
        return self.conversation_history

assistant = AIAssistant()

@app.route('/')
def home():
    return jsonify({'name': 'SparkleAbenaInTech AI Assistant', 'developer': 'Abena Apau', 'status': 'running'})

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    message = data.get('message', '')
    if not message:
        return jsonify({'error': 'No message provided'}), 400
    response = assistant.respond(message)
    return jsonify({'message': message, 'response': response, 'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')})

@app.route('/history', methods=['GET'])
def history():
    return jsonify({'conversation': assistant.get_history(), 'total_messages': len(assistant.get_history())})

if __name__ == '__main__':
    app.run(debug=True)
