from random import choice
from textwrap import dedent
from random import sample
from time import sleep
from typing import TypeVar, Set
import os.path

# from user_input import user_choice
from pickle_vocab import create_pickles
from pickle_vocab import unpickle_vocab
from set_choose import setChoice
from set_choose import setChooseN
from user_input import check_response
from user_input import check_input

user_vocab_file = "known_vocab.pickle"
user_bytype_file = "vocab_by_type.pickle"


if not os.path.isfile(user_vocab_file) or not os.path.isfile(user_bytype_file):
    create_pickles()


usr_vocab_def = (unpickle_vocab(user_vocab_file)[0])
usr_vocab_type = (unpickle_vocab(user_bytype_file)[0])



def choose_from_correct(vocab_by_word: dict, vocab_by_type: dict):

    """ Not currently utilised. Resolves sampling error caused by smaller
    sets of vocab types (e.g. fewer pronouns samples as often as adjectives) """

    answer = setChoice(vocab_by_word)
    vocab_selection = set()
    answer_types = []

    for v_types in vocab_by_word[answer]:
        answer_types.append(v_types)

    answer_type = choice(answer_types)

    if len(vocab_by_type[answer_type]) > 3:
        vocab_selection.add(answer)
        while len(vocab_selection) < 4:
            vocab_selection.add(choice(vocab_by_type[answer_type]))

    else:
        raise Exception(dedent(f"""Not enough word_types of 
            correct answer to provide selection"""))

    return answer, answer_type, vocab_selection




def choice_by_type(vocab_by_type: dict):

    """ Current default selection based on a sample from a
    random vocab type (one of many issues being unrepresentative
    sampling from rarer word types) """
    
    vocab_selection = None
    answer_type = setChoice(vocab_by_type)
    attempt = 0

    while len(vocab_by_type[answer_type]) < 4:
        answer_type = setChoice(vocab_by_type)
        if attempt > 4:
            raise Exception("Insufficient range of vocab types available for\nthis function")
        attempt +=1
    vocab_selection = sample(vocab_by_type[answer_type], 4)

    answer = choice(vocab_selection)
    
    return answer, answer_type, vocab_selection



def start():

    player_score = 0
    wrong = 0
    conc_wrong = 0

    while player_score < 5:

        sleep(1)
        os.system('cls' if os.name == 'nt' else 'clear')

        print(f"Your score is currently {player_score}. You require 5 points to leave and continue with your life...")
        
        answer, answer_type, vocab_selection = choice_by_type(usr_vocab_type)
        print(f"\n\"{choice(usr_vocab_def[answer][answer_type])}\"")

        print("\nTo which of the following options does this definition pertain?")

        count = 1
        for option in vocab_selection:
            print(f"    {count}.)", option)
            count +=1

        user_input = input("\nPlease enter an integer from 1 - 4\n>>> ")
        evaluation = check_input(user_input)

        if evaluation == False:
            continue
        

        # Without defining a range of acceptable types, a 0 indexes to list's end
        if answer == vocab_selection[int(user_input) -1]:
            print("Excellent - you are correct!")
            player_score +=1
            conc_wrong = 0

        else:
            wrong +=1
            conc_wrong +=1
            print(f"\nFor shame... The correct answer was: {answer}")
            sleep(1)
            check_response(wrong, conc_wrong)



    
    print("Congratulations. You are a scholar!")
    quit()



print("\n   #####Welcome player!#####")
sleep(1)
start()
