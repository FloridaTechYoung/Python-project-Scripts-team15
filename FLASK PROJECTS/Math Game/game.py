import random
import time

import pytest


class Game():
    start_num_integers = 0
    def restart(self):
        self.num_integers = self.start_num_integers
        self.round_number = 1
        self.question = None
        self.question_number = 0
        self.generated_time = 0
        self.answer = 0
        self.points = 0

    def __init__(self, num_integers = 2) -> None:
        self.start_num_integers = num_integers
        self.restart()

    def get_operators(self):
        if self.round_number <= 2:
            return [random.choice(['+', '-']) for _ in range(self.num_integers - 1)]
        elif self.round_number <= 4:
            return [random.choice(['+', '-', '*']) for _ in range(self.num_integers - 1)]
        else:
            return [random.choice(['+', '-', '*', '/']) for _ in range(self.num_integers - 1)]

    def generate_question(self):
        """Generate a random arithmetic question."""
        min = 1
        max = 10
        numbers = [random.randint(min, max) for _ in range(self.num_integers)]

        operators = self.get_operators()

        # Ensure division results in whole numbers
        for i, op in enumerate(operators):
            if op == '/':
                numbers[i] = numbers[i+1] * random.randint(1, 10)
        
        self.generated_time = time.time()
        self.question = " ".join([f"{numbers[i]} {operators[i]}" for i in range(self.num_integers - 1)]) + f" {numbers[-1]} = ? "
        self.answer = eval("".join([str(numbers[i]) + operators[i] for i in range(self.num_integers - 1)]) + str(numbers[-1]))
        return self.question
    
    def submit_answer(self, answer: float) -> bool:
        if self.question == None:
            raise Exception("No question generated")

        self.question = None
        if self.answer == answer:
            self.points += 100

            time_taken = time.time() - self.generated_time
            self.points += max(0, int(100 - (time_taken * 5)))

            return True
        return False
    
    def next_round(self):
        self.round_number += 1
        self.num_integers += 1

def main():
    print("Welcome to the Math Game!")
    game = Game()

    num_questions = 5

    while game.round_number <= 5:
        print(f"Round {game.round_number}:")
        for _ in range(num_questions):
            question = game.generate_question()
            print(question)
            user_answer = input("Your answer: ")
            try:
                user_answer = float(user_answer)  # Convert user input to float for division
                if game.submit_answer(user_answer):
                    print("Correct!")
                else:
                    print("Incorrect!")
            except ValueError:
                print("Invalid input! Please enter a number.")

        print(f"Round {game.round_number} over! Total points: {game.points}")
        if game.round_number < 5:
            time.sleep(3)

        game.next_round()

    print("Thanks for playing!")

def test_generate_equation():
    random.seed(123)
    game = Game()
    assert "2 + 9 = ? " == game.generate_question()

def test_answer_correct():
    random.seed(123)
    game = Game()
    game.generate_question()
    assert game.submit_answer(11) == True

def test_answer_incorrect():
    random.seed(123)
    game = Game()
    game.generate_question()
    assert game.submit_answer(1) == False

def test_answer_no_question():
    game = Game()
    
    with pytest.raises(Exception):
        game.submit_answer(10)

if __name__ == "__main__":
    main()
