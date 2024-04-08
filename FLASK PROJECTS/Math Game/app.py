# Main entry point

from flask import Flask, request

app = Flask(__name__)

@app.route('/send_question')
def send_question(question):
    return question
@app.route('/print')
def print_anything(statement):
    return statement

@app.route('/get_answer')
def get_answer():

    answer_int = request.form.get("answer")
    
    return answer_int
