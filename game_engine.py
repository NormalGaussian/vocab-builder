from random import choice
from time import sleep
import os.path

# from user_input import user_choice
from pickle_vocab import create_pickles
from gen_game_choices import generate_and_ask_question
from responses_to_user import check_response


user_vocab_file = "known_vocab.pickle"
user_bytype_file = "vocab_by_type.pickle"


# Create pickle files of dicts if either of them are not found
if not os.path.isfile(user_vocab_file) or not os.path.isfile(user_bytype_file):
    create_pickles()


   
def start():

    """
    Main game loop.
    """

    player_score = 0
    total_incorrect_answers = 0
    consecutive_incorrect_answers = 0

    while player_score < 5:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"Your score is {player_score} and you require 5 points to continue with your life.")
        
        if generate_and_ask_question() == True:
            player_score +=1
            consecutive_incorrect_answers = 0
        else:
            total_incorrect_answers +=1
            consecutive_incorrect_answers +=1
            check_response(total_incorrect_answers, consecutive_incorrect_answers)


    print("Congratulations! You are a scholar and a Gentle(person)")
    sleep(2)
    quit()


print("\n   #####Welcome player!#####")
sleep(1)
start()
