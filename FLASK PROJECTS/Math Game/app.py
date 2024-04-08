# Main entry point

from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def default():
    return open(index.html,'r')

@app.route('/send_question')
def send_question(question):
    return question


@app.route('/get_answer')
def get_answer():

    answer_int = request.form.get("answer")
    
    return answer_int
