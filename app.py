from flask import Flask, jsonify, request
from datetime import datetime
import os

app = Flask(__name__)

# Home route
@app.route('/')
def home():
    return jsonify({
        'message': 'Welcome to SparkleAbenaInTech AI API!',
        'status': 'running',
        'developer': 'Abena Apau',
        'version': '2.0 - Now with AI!'
    })

# AI Chat route
@app.route('/ai/chat', methods=['POST'])
def ai_chat():
    try:
        from openai import OpenAI
        client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))
        
        data = request.get_json()
        user_message = data.get('message', '')
        
        if not user_message:
            return jsonify({'error': 'No message provided'}), 400
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant for SparkleAbenaInTech. You are knowledgeable about AI, cybersecurity, and software development."},
                {"role": "user", "content": user_message}
            ]
        )
        
        return jsonify({
            'response': response.choices[0].message.content,
            'status': 'success'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# AI Motivator route
@app.route('/ai/motivate', methods=['GET'])
def motivate():
    try:
        from openai import OpenAI
        client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an encouraging coach for someone learning to code and build AI apps. Keep responses under 3 sentences."},
                {"role": "user", "content": "Give me a short motivational message for someone learning to become a Full Stack AI Engineer"}
            ]
        )
        
        return jsonify({
            'motivation': response.choices[0].message.content,
            'from': 'Your AI Coach'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# About route
@app.route('/about')
def about():
    return jsonify({
        'name': 'Abena Apau',
        'title': 'Full Stack AI Engineer',
        'skills': ['Python', 'Flask', 'React', 'JavaScript', 'AI Engineering', 'Cybersecurity'],
        'github': 'github.com/SparkleAbenaInTech'
    })

if __name__ == '__main__':
    app.run(debug=True)
    