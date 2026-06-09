from colorama import Fore, Style, init
import random
init(autoreset = True)

Moves = ['Rock', 'Paper', 'Scissors']

Beats = {
    'Rock': 'Paper',
    'Paper': 'Scissors',
    'Scissors': 'Rock'
}

def display_scores(player_name, player_score, ai_score, ties):
    print(Fore.CYAN + f"\n  {player_name}: {player_score}  |  AI: {ai_score}  |  Ties: {ties}\n")

def display_result(player_move, ai_move, result, player_name):
    print()
    print(Fore.YELLOW + f"  You chose:  " + Fore.RED + player_move)
    print(Fore.YELLOW + f"  AI chose:   " + Fore.BLUE + ai_move)
    print(Fore.GREEN + "=========================================")
    if result == 'win':
        print(Fore.GREEN + f"  You win this round, {player_name}!")
    elif result == 'lose':
        print(Fore.RED + "  AI wins this round!")
    else:
        print(Fore.YELLOW + "  It's a tie!")
    print(Fore.GREEN + "=========================================\n")

def get_player_move():
    print(Fore.CYAN + "  Choose your move:")
    for i, move in enumerate(Moves, 1):
        print(Fore.YELLOW + f"  {i}. {move}")
    
    choice = -1
    while choice not in range(1, 4):
        try:
            choice = int(input(Fore.WHITE + "\n  Enter 1, 2, or 3: "))
            if choice not in range(1, 4):
                print(Fore.RED + "  Invalid! Enter 1, 2, or 3.\n")
        except ValueError:
            print(Fore.RED + "  Enter a number!\n")
    
    return Moves[choice - 1]

def ai_move_basic():
    return random.choice(Moves)

def ai_move_smart(move_history):

    if not move_history:
        return random.choice(Moves)
    
    
    counts = {move: move_history.count(move) for move in Moves}
    
    
    predicted_player_move = max(counts, key=counts.get)
    
    
    counter = Beats[predicted_player_move]
    return counter

def check_winner(player_move, ai_move):
    if player_move == ai_move:
        return 'tie'
    elif Beats[player_move] == ai_move:
        return 'lose'
    else:
        return 'win'

def rock_paper_scissors():
    print(Fore.CYAN + "\n  Welcome to Rock Paper Scissors!")
    player_name = input(Fore.GREEN + "  Enter your name: ")
    
    print(Fore.CYAN + "\n  Choose AI difficulty:")
    print(Fore.YELLOW + "  1. Easy   (random AI)")
    print(Fore.YELLOW + "  2. Hard   (tracks your patterns)")
    
    difficulty = ''
    while difficulty not in ['1', '2', 'easy', 'hard']:
        difficulty = input(Fore.WHITE + "\n  Enter 1 or 2: ").strip().lower()

    use_smart_ai = (difficulty in ['2', 'hard'])

    while True:
        player_score = 0
        ai_score = 0
        ties = 0
        move_history = []
        rounds = 0

        while True:
            print(Fore.GREEN + "\n=========================================")
            display_scores(player_name, player_score, ai_score, ties)

            player_move = get_player_move()

            if use_smart_ai:
                ai = ai_move_smart(move_history)
            else:
                ai = ai_move_basic()

            move_history.append(player_move)

            result = check_winner(player_move, ai)
            display_result(player_move, ai, result, player_name)

            if result == 'win':
                player_score += 1
            elif result == 'lose':
                ai_score += 1
            else:
                ties += 1

            rounds += 1

            play_again = input(Fore.CYAN + "  Play another round? (yes/no): ").lower().strip()
            if play_again != 'yes':
                break

        print(Fore.GREEN + "\n=========================================")
        print(Fore.CYAN + f"  Final Score after {rounds} round(s):")
        display_scores(player_name, player_score, ai_score, ties)

        if player_score > ai_score:
            print(Fore.GREEN + f"  {player_name} wins the game! Well played!")
        elif ai_score > player_score:
            print(Fore.RED + "  AI wins the game! Better luck next time.")
        else:
            print(Fore.YELLOW + "  It's a draw! Evenly matched.")

        new_game = input(Fore.CYAN + "\n  Start a new game? (yes/no): ").lower().strip()
        if new_game != 'yes':
            print(Fore.GREEN + "\n  Thanks for playing, " + player_name + "!")
            break

if __name__ == "__main__":
    rock_paper_scissors()