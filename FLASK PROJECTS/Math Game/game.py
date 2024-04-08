import random
import time

def generate_question(num_integers, round_number):
    """Generate a random arithmetic question."""
    min = 1
    max = 20
    numbers = [random.randint(min, max) for _ in range(num_integers)]
    if round_number <= 2:
        operators = [random.choice(['+', '-']) for _ in range(num_integers - 1)]
    elif round_number <= 4:
        operators = [random.choice(['+', '-', '*']) for _ in range(num_integers - 1)]
    else:
        operators = [random.choice(['+', '-', '*', '/']) for _ in range(num_integers - 1)]
    # Ensure division results in whole numbers
    for i, op in enumerate(operators):
        if op == '/':
            numbers[i] = numbers[i+1] * random.randint(1, 10)
    
    question = " ".join([f"{numbers[i]} {operators[i]}" for i in range(num_integers - 1)]) + f" {numbers[-1]} = ? "
    return question, eval("".join([str(numbers[i]) + operators[i] for i in range(num_integers - 1)]) + str(numbers[-1]))
    

def main():
    print("Welcome to the Math Game!")
    points = 0
    round_number = 1
    num_questions = 5
    num_integers = 2
    while round_number <= 5:
        print(f"Round {round_number}:")
        for _ in range(num_questions):
            question, answer = generate_question(num_integers, round_number)
            print(question)
            start_time = time.time()
            user_answer = input("Your answer: ")
            end_time = time.time()
            try:
                user_answer = float(user_answer)  # Convert user input to float for division
                if user_answer == answer:
                    points += 10
                    print("Correct!")
                else:
                    print("Incorrect!")
            except ValueError:
                print("Invalid input! Please enter a number.")
            # Add bonus points for answering quickly
            time_taken = end_time - start_time
            if user_answer == answer:
                points += max(0, 5 - int(time_taken))  # Maximum bonus: 5 points
        print(f"Round {round_number} over! Total points: {points}")
        print(f"Next round starts in 3 seconds...")
        time.sleep(3)
        round_number += 1
        num_integers += 1  # Increase number of questions for the next round
    
    print("Thanks for playing!")

if __name__ == "__main__":
    main()
