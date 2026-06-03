print("Start the conversation Yes or No?")
start = input().lower()

if start == "no":
    print("Goodbye!")
else:
    print("You can end the conversation at any time by typing 'no'")

    print("Hi I am your AI chatbot! What's your name?")
    name = input()

    if name.lower() == "no":
        print("Goodbye!")
    else:
        print(f"Hi nice to see you {name}!")

        while True:

            print("What is your age?")
            age = input()
            if age.lower() == "no":
                break
            print(f"Nice to know you are {age} years old!")

            print("What are your hobbies?")
            hobbies = input()
            if hobbies.lower() == "no":
                break
            print(f"Interesting! {hobbies} sounds fun.")

            print("How is the weather today? Is it sunny, rainy or cloudy?")
            weather = input().lower()
            if weather == "no":
                break

            if weather == "sunny":
                print("Great! Enjoy the sunshine!")
            elif weather == "rainy":
                print("Don't forget to take an umbrella!")
            else:
                print("I hope you have a nice day regardless of the weather!")

            print("How are you feeling good or bad?")
            mood = input().lower()
            if mood == "no":
                break

            if mood == "good":
                print("That's nice")
            elif mood == "bad":
                print("Oh that's unfortunate!")
            else:
                print("I hope you have a good day regardless of how you are feeling!")
            
            break
        print(f"Nice talking to you {name}, have a good day!")