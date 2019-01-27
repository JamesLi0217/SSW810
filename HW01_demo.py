from random import choice

def get_computer_choice():
    ''' randomly choose and return one of "rock","paper","scissors"'''
    move_computer = choice(["rock","paper","scissors"])
    return move_computer

def get_player_choice():
    ''' players simultaneously choose one of "rock", "paper", or "scissors"'''
    
    move_player=input("Please choose 'R', 'P', 'S' or 'Q' to quit: ")

    if move_player in ["R", "r"]:
        move_player = "rock"
    elif move_player in ["P" , "p"]:
        move_player = "paper"
    elif move_player in ["S" , "s"]:
        move_player = "scissors"
    
    return move_player 


def main():
    
    while True:
        move_computer = get_computer_choice()

        move_player = get_player_choice()

        moves=[]
        moves.append(move_computer)
        moves.append(move_player)
        result_computer_win=[['paper', 'rock'],['rock','scissors'],['scissors','paper']]
        result_player_win=[['rock','paper'],['scissors','rock'],['paper','scissors']]
        result_tie=[['rock','rock'],['scissors','scissors'],['paper','paper']]

        if moves in result_computer_win:
            
            result ="I win!"
        elif moves in result_player_win:
            result= "You win!"
        elif moves in result_tie:
            result = "Tie!"
        else:
            if move_player in ["Q" , "q"]:
                result = "Thanks for playing!"
                print(result)
                break
            else:
                result = "Please choose again!"
        print(result)

if __name__ == "__main__":
    main()