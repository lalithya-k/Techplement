from flask import Flask, render_template, request, jsonify, url_for, redirect
from flask_pymongo import PyMongo, ObjectId
from datetime import datetime

app = Flask(__name__)

app.config['SECRET_KEY'] = 'Saibaba@321'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/calculator_db'
mongo = PyMongo(app)

class HistoryEntry:
    def __init__(self, expression, result):
        self.expression = expression
        self.result = result
        self.timestamp = datetime.now()

@app.route('/')
def home():
    return render_template("entryPage.html")

@app.route('/history', methods=['GET'])
def get_history():
    history_entries = list(mongo.db.history.find({}, {'_id': False}))
    return jsonify({'history': history_entries})


@app.route('/calculate', methods=['POST', 'GET'])
def calculate():
    if request.method == 'POST':
        expression = request.json.get('expression')

        try:
            result = evaluate_expression(expression)
            history_entry = HistoryEntry(expression=expression, result=result)
            mongo.db.history.insert_one(history_entry.__dict__)

            return jsonify({'result': result})
        except Exception as e:
            return jsonify({'error': str(e)}), 400
    else:
        return render_template("homePage.html")

def evaluate_expression(expression):
    safe_expr = sanitize_expression(expression)
    result = eval(safe_expr)
    return result

def sanitize_expression(expression):
    allowed_chars = set('0123456789+-*/() ')
    sanitized_expr = ''.join(c for c in expression if c in allowed_chars)
    return sanitized_expr

if __name__ == '__main__':
    app.run(debug=True)