from colorama import Fore, Style, init
import random
init(autoreset=True)

def display_board(board):
    print()
    def colored(cell):
        if cell == "X":
            return Fore.RED + cell + Style.RESET_ALL
        elif cell == "O":
            return Fore.BLUE + cell + Style.RESET_ALL
        
        else:
            return Fore.YELLOW + cell + Style.RESET_ALL
        
    print(' ' + colored(board[0]) + '|' + colored(board[1]) + '|' + colored(board[2]))
    print(Fore.GREEN + '==========')
    print(' ' + colored(board[3]) + '|' + colored(board[4]) + '|' + colored(board[5]))
    print(Fore.GREEN + '==========')
    print(' ' + colored(board[6]) + '|' + colored(board[7]) + '|' + colored(board[8]))
    print()

def player_move(board, symbol):
    move = -1
    while move not in range(1, 10) or not board[move -1].isdigit():
        try:
            move = int(input("Enter a number between 1 to 9\n"))
            if move not in range (1, 10) or not board[move -1].isdigit():
                print("Invalid move. Please try again\n")
        except ValueError:
            print("Enter a number between 1 and 9!\n")
    board[move -1] = symbol

def player_choice():
    symbol = ''
    while symbol not in ['X', 'O']:
        symbol = input(Fore.BLUE + "Do you want to be X or O\n").upper()
    if symbol == 'X':
        return('X', 'O')
    else:
        return('O', 'X')
    
def ai_move(board, ai_symbol, player_symbol):
    for i in range (9):
        if board[i].isdigit():
            board_copy = board.copy()
            board_copy[i] = ai_symbol
            if check_win(board_copy, ai_symbol):
                board[i] = ai_symbol
                return
    for i in range(9):
        if board[i].isdigit():
            board_copy = board.copy()
            board_copy[i] = player_symbol
            if check_win(board_copy, player_symbol):
                board[i] = ai_symbol
                return
    possible_moves = [i for i in range(9) if board[i].isdigit() ]
    move = random.choice(possible_moves)
    board[move] = ai_symbol

def check_win(board, symbol):
    win_conditions = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),
        (0, 3, 6), (1, 4, 7), (2, 5, 8),
        (0, 4, 8), (2, 4, 6)

    ]
    for  i in win_conditions:
        if board[i[0]] == board[i[1]] == board[i[2]] == symbol:
            return True
    return False

def check_full(board):
    return all(not spot.isdigit() for spot in board)

def tic_tac_toe():
    print("Welcome to Tic Tac Toe!")
    player_name = input(Fore.GREEN + "Enter your name\n")
    while True:
        board = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
        player_symbol, ai_symbol = player_choice()
        turn = 'Player'
        game_on = True
    
        while game_on:
            display_board(board)
            if turn == 'Player':
                player_move(board, player_symbol)
                if check_win(board, player_symbol):
                    display_board(board)
                    print("Congratulations! " + player_name + " You won the game")
                    game_on = False
                else:
                    if check_full(board):
                        display_board(board)
                        print("It is a tie")
                        break
                    else:
                        turn = 'AI'

            else:
                ai_move(board, ai_symbol, player_symbol)
                if check_win(board, ai_symbol):
                    display_board(board)
                    print("AI has won the game")
                    game_on = False
                else:
                    if check_full(board):
                        display_board(board)
                        print("It is a tie")
                        break
                    else:
                        turn = 'Player'

        play_again = input("Do you want to play another game?\n").lower()
        if play_again != "yes":
            print("Thank you for playing")
            break
if __name__=="__main__":
    tic_tac_toe()