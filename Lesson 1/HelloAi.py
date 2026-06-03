print("Hi I am your AI chatbot ")
name = input()
print(f"Hi nice to see you {name}")

print("How are you feeling good or bad?")
mood = input().lower()

if mood == "good":
    print("Thats nice")
elif mood == "bad":
    print("How can i help")
else:
    print("Im not sure how i can help")

print(f"Nice talking {name} have a good day")
