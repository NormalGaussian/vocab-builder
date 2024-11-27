from random import choice
from textwrap import dedent
from random import sample
from time import sleep

#from user_input import user_choice
from pickle_vocab import unpickle_vocab
from set_choose import setChoice
from set_choose import setChooseN
from user_input import check_response
from user_input import check_input




usr_vocab_def = (unpickle_vocab('known_vocab.pickle')[0])
usr_vocab_type = (unpickle_vocab('vocab_by_type.pickle')[0])


#This will likely be useful later on when trying to specify
#which words are to be trained (words that have been
#incorrect more often in previous games etc.)

def choose_from_correct(vocab_by_word: dict, vocab_by_type: dict):

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


# Current default selection based on a sample from a
# random vocab type (one of many issues being unrepresentative
# sampling from rarer word types)

def choice_by_type(vocab_by_type: dict):
    
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

        print(f"Your score is currently {player_score}. You require 5 points to leave and continue with your life...")
        
        answer, answer_type, vocab_selection = choice_by_type(usr_vocab_type)
        print(f"\n\"{choice(usr_vocab_def[answer][answer_type])}\"")

        print("\nTo which of the following options does this definition pertain?")

        for option in vocab_selection:
            print("     ", option)

        user_input = input("\nPlease enter an integer from 1 - 4\n>>> ")
        evaluation = check_input(user_input)

        if evaluation == None:
            continue
        

        #Without defining a range of acceptable types, a 0 indexes to list's end
        if answer == vocab_selection[int(user_input) -1]:
            print("Excellent - you are correct!")
            player_score +=1
            conc_wrong = 0

        else:
            wrong +=1
            conc_wrong +=1
            print(f"\nFor shame... The correct answer was: {answer}")
            check_response(wrong, conc_wrong)



    
    print("Congratulations. You are a scholar!")
    quit()

print("\n   #####Welcome player!#####")
sleep(2)
start()
