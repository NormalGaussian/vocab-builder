from random import choice
from time import sleep
import os.path

from pickle_vocab import create_pickles
from responses_to_user import berate_user_for_incorrect_answer


user_vocab_file = "known_vocab.pickle"
user_bytype_file = "working_vocab.pickle"

# Create pickle files of dicts if either of them are not found
if not os.path.isfile(user_vocab_file) or not os.path.isfile(user_bytype_file):
    create_pickles()

from gen_game_choices import generate_and_ask_question
from gen_game_choices import player_save_choice


# As the dictionaries are in gen_game_choices - will need to run a function in there to save
   
def start():

    """
    Main game loop.
    """

    player_score = 0
    total_incorrect_answers = 0
    consecutive_incorrect_answers = 0

    while player_score < 10:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"Your score is {player_score} and you require 10 points to continue with your life.")
        
        if generate_and_ask_question() == True:
            player_score +=1
            consecutive_incorrect_answers = 0
        else:
            total_incorrect_answers +=1
            consecutive_incorrect_answers +=1
            berate_user_for_incorrect_answer(total_incorrect_answers, consecutive_incorrect_answers)

    ex_string = "##### Congratulations! You are a scholar and a Gentle(person)  #####"
    output = ""
    for character in ex_string:
        sleep(0.02)
        output += character
        print(output, end="")
        print("\r", end="")
    sleep(1)
    player_save_choice()
    quit()

os.system('cls' if os.name == 'nt' else 'clear')
print("\n\n\n")

ex_string = "#####  Welcome player!  #####"
output = ""
for character in ex_string:
    sleep(0.02)
    output += character
    print(output, end="")
    print("\r", end="")

sleep(1)
start()
