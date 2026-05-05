from flask import Flask, jsonify, request
from datetime import datetime

app = Flask(__name__)

# Home route
@app.route('/')
def home():
    return jsonify({
        'message': 'Welcome to SparkleAbenaInTech API!',
        'status': 'running',
        'developer': 'Abena Apau'
    })

# Get current time
@app.route('/time')
def get_time():
    return jsonify({
        'current_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'message': 'Time from your Flask server!'
    })

# Calculator route
@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.get_json()
    num1 = data.get('num1', 0)
    num2 = data.get('num2', 0)
    operation = data.get('operation', 'add')

    if operation == 'add':
        result = num1 + num2
    elif operation == 'subtract':
        result = num1 - num2
    elif operation == 'multiply':
        result = num1 * num2
    elif operation == 'divide':
        result = num1 / num2 if num2 != 0 else 'Cannot divide by zero'

    return jsonify({
        'num1': num1,
        'num2': num2,
        'operation': operation,
        'result': result
    })

# About route
@app.route('/about')
def about():
    return jsonify({
        'name': 'Abena Apau',
        'title': 'Full Stack AI Engineer',
        'skills': ['Python', 'Flask', 'React', 'JavaScript', 'AI Engineering'],
        'github': 'github.com/SparkleAbenaInTech'
    })

if __name__ == '__main__':
    app.run(debug=True)
    