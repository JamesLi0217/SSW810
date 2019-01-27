'''
@Title: Rock, Paper, Scissors
@Author: PuzhuoLi  CWID:10439435
@Date: 2019-01-27 12:24:15
'''

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
    

    '''
    rock beats scissors (rock smashes scissors)
    scissors beats paper (scissors cut paper)
    paper beats rock (paper covers rock)
    a tie occurs if both players choose the same option, e.g. both choose "paper"
    '''
    while True:
        move_computer =get_computer_choice()

        move_player=get_player_choice()
        if move_player == "rock":
            if move_computer== "scissors":
                result= "%s beats %s - You win!"%(move_player,move_computer)
            
            elif move_computer=="paper":
                result= "%s beats %s - I win!"%(move_player,move_computer)
            
            else:
                result= "Tie: we both chose %s!" %move_player

        elif move_player == "paper":
            if move_computer== "rock":
                result= "%s beats %s - You win!"%(move_player,move_computer)
            
            elif move_computer=="scissors":
                result= "%s beats %s - I win!"%(move_player,move_computer)

            else:
                result= "Tie: we both chose %s!" %move_player

        elif move_player == "scissors":
            if move_computer== "paper":
                result= "%s beats %s - You win!"%(move_player,move_computer)
            
            elif move_computer=="rock":
                result= "%s beats %s - I win!"%(move_player,move_computer)
            
            else:
                result= "Tie: we both chose %s!" %move_player

        elif move_player in ["Q" , "q"]:
            result = "Thanks for playing!"
            print(result) 
            break
        else:
            result = "Please choose again!"
        

        print(result) 



if __name__ == "__main__":
    main()









