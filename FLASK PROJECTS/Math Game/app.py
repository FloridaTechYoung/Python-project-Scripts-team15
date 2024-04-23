# Main entry point

import json
from typing import Any
from flask import Flask, make_response, request
from game import Game

app = Flask(__name__)

class GameState():
    def __init__(self, questions_per_round=5):
        self.game = Game()
        self.questions_per_round = questions_per_round
        self.question_number = 0

    def get_question_resp(self):
        if self.game.question == None:
            self.game.generate_question()
            self.question_number += 1

        return {
            "question": self.game.question,
            "question_number": self.question_number,
            "questions_per_round": self.questions_per_round,
            "round": self.game.round_number,
            "points": self.game.points
        }
    
    def get_answer_resp(self, answer: float):
        if self.question_number == self.questions_per_round:
            self.game.next_round()
            self.question_number = 0

        return {"correct": self.game.submit_answer(answer)}



games: dict[str, GameState] = {}


@app.route("/")
def default():
    return open("./index.html", "r")


@app.route("/question")
def send_question():
    id = request.user_agent.string

    game_state = games.setdefault(id, GameState())

    return game_state.get_question_resp()

@app.route("/reset", methods=["POST"])
def reset():
    id = request.user_agent.string

    game_state = games.setdefault(id, GameState())
    game_state.game.restart()

    return game_state.get_question_resp()

@app.route("/answer", methods=["POST"])
def get_answer():
    id = request.user_agent.string
    try:
        body: dict[str, Any] = json.loads(request.data)
        answer = float(body.get("answer"))

        if id not in games:
            return {"error": 404, "message": "Game not started for " + id}, 404

        return games[id].get_answer_resp(answer)
    
    except TypeError:
        return {"error": 400, "message": "Answer should be a valid float"}, 400
