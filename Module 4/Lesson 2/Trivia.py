import requests
import html
import random

GK_CATEGORY_ID = 9

URL = f"https://opentdb.com/api.php?amount=10&category={GK_CATEGORY_ID}&type=multiple"

def get_gk_questions():
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
    questions = get_gk_questions()
    if not questions:
        print("Error: Couldn't get the questions")
        return

    score = 0
    print("Welcome to a General Knowledge Trivia!")

    for i, q in enumerate(questions, 1):
        question = html.unescape(q["question"])
        correct = html.unescape(q["correct_answer"])
        incorrects = [html.unescape(a) for a in q["incorrect_answers"]]

        options = incorrects + [correct]
        random.shuffle(options)

        print(f"Question {i}: {question}")

        for j, option in enumerate(options, 1):
            print(f"Option {j}: {option}")

        while True:
            try:
                choice = int(input("\nPlease enter a number from 1 - 4: "))
                if 1 <= choice <= 4:
                    break
            except ValueError:
                pass
            print("Please type a number from 1 - 4")

        if options[choice - 1] == correct:
            print("Correct Answer!")
            score += 1
        else:
            print("Wrong Answer!", correct)

    print(f"Score: {score}/{len(questions)}")
    print(f"Percentage: {score / len(questions) * 100:.1f}%")

if __name__ == "__main__":
    quiz()