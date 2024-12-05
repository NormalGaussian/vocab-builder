from random import choice
from time import sleep
import os.path

from pickle_vocab import create_pickles
from responses_to_user import check_response

user_vocab_file = "known_vocab.pickle"
user_bytype_file = "vocab_by_type.pickle"

# Create pickle files of dicts if either of them are not found
if not os.path.isfile(user_vocab_file) or not os.path.isfile(user_bytype_file):
    create_pickles()


from gen_game_choices import generate_question


   
def start():

    """
    Main game loop.
    """

    player_score = 0
    wrong = False
    concurrent_wrong = 0

    while player_score < 5:

        was_wrong = False

        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"Your score is {player_score} and you require 5 points to continue with your life.")
        
        # Generates a question and return a state/true or false, and new player stats
        if generate_question() == True:
            player_score +=1
            concurrent_wrong = 0
        else:
            wrong +=1
            concurrent_wrong +=1
            was_wrong = True

        # Generate print statements if needed based on stats
        if was_wrong == True:
            check_response(wrong, concurrent_wrong)


    print("Congratulations! You are a scholar and a Gentle(person)")
    sleep(2)
    quit()


print("\n   #####Welcome player!#####")
sleep(1)
start()
