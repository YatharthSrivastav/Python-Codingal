import requests
import html
import random
from inputimeout import inputimeout, TimeoutOccurred

def get_questions(category):
    URL = f"https://opentdb.com/api.php?amount=5&category={category}&type=multiple"
    try:
        response = requests.get(URL)
        if response.status_code == 200:
            data = response.json()
            if data["response_code"] == 0 and data["results"]:
                return data["results"]
    except requests.RequestException:
        pass
    return None

def quiz():

    print("Choose a category:")
    print("9 - General Knowledge")
    print("17 - Science & Nature")
    print("18 - Science: Computers")
    print("21 - Sports")

    while True:
        category = input("Enter category number: ").strip()
        if category in ["9", "17", "18", "21"]:
            break
        print("Please enter 9, 17, 18, or 21.")

    questions = get_questions(category)
    if not questions:
        print("Error: Couldn't get the questions")
        return

    score = 0
    print("Welcome to Trivia!\n")
    ans = input("Start the timed quiz? (yes/no)\n").strip().lower()
    if ans == "no":
        print("Bye!")
        return

    for i, q in enumerate(questions, 1):

        question = html.unescape(q["question"])
        correct = html.unescape(q["correct_answer"])
        incorrects = [html.unescape(a) for a in q["incorrect_answers"]]

        options = incorrects + [correct]
        random.shuffle(options)

        category = html.unescape(q["category"])
        print(f"\nCategory: {category}")
        print(f"Difficulty: {q['difficulty']}\n")
        print(f"Question {i}: {question}")

        for j, option in enumerate(options, 1):
            print(f"Option {j}: {option}")

        choice = None

        while True:
            try:
                choice = int(inputimeout(
                    prompt="\nPlease enter a number from 1 - 4 (10 seconds): ",
                    timeout=10
                ))
                if 1 <= choice <= 4:
                    break
                print("Please type a number from 1 - 4")

            except TimeoutOccurred:
                print("\nTime's up!")
                break

            except ValueError:
                print("Please type a number from 1 - 4")

        if choice is not None and options[choice - 1] == correct:
            print("Correct Answer!")
            score += 1
        else:
            print("Wrong Answer!", correct)

    print(f"\nScore: {score}/{len(questions)}")
    print(f"Percentage: {score / len(questions) * 100:.1f}%")

if __name__ == "__main__":
    quiz()