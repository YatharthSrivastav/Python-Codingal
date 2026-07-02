import requests
def random_joke():
    url = "https://official-joke-api.appspot.com/random_joke"
    response = requests.get(url)

    if response.status_code == 200:
        #
        # print(f"Full JSON Response {response.json()}")
        joke_data = response.json()
        return f"{joke_data['setup']} - {joke_data['punchline']}"
    else:
        return "Failed to retrieve a joke!"
    
def main():
    print("Hello! Welcome to Random Joke Generator")

    while True:
        ans = input("Press Enter to get a random joke. Type q/exit to quit: ")
        if ans in ("q", "exit"):
            print("Bye")
            break
        joke = random_joke()
        print(joke)

if __name__ == "__main__":
    main()
