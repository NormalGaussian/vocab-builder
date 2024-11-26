from user_vocab import clean_vocab
from get_defs import word_types
from get_defs import extract_defs
from textwrap import dedent
from time import sleep

from random import choice
from set_choose import setChoice

"""
Checks to see if a given word has a url associated
Checks to see if a given word has vocab_types associated
Generates a new word if not
"""
def check_viable():


    # This looping structure is causing the code to run slow.
    # The more words have no word_types, the slower the code will run.
    # Any kind of loop like this can be considered a potential infinite loop; we should have a way to guarantee it will end.
    # The most ideal guarantee is one that ends in constant time - as then our program will remain fast.

    answer = setChoice(clean_vocab)

    while word_types(answer) == None:
        answer = setChoice(clean_vocab)
        
    return answer
 


#returns set of relevant words (defined as relevant if they share
#the chosen vocab_type of the correct word)
def vocab_choices():
    
    vocab_selection = []
    answer = check_viable()
    answer_type = setChoice(word_types(answer))
    misdirect_vocab = check_viable()

    while len(vocab_selection) < 3:
        types = word_types(misdirect_vocab)
        
        # Handle an edge case, which is likely a bug elsewhere.
        if types == None:
            misdirect_vocab = check_viable()
            continue

        l_word_types = list(types)
        if (answer_type in l_word_types and 
                misdirect_vocab not in vocab_selection and
                misdirect_vocab != answer):
            vocab_selection.append(misdirect_vocab)
        misdirect_vocab = check_viable()

    vocab_selection.append(answer)
    return vocab_selection, answer, answer_type


#returns definitions of the relevant type from the chosen words
def answer_definition():
    
    vocab_selection, answer, answer_type = vocab_choices()

    answer_def = choice(extract_defs(answer, answer_type))

    return vocab_selection, answer, str(answer_def)

def user_choice():
    # This is good. Would you rather the user type out the answer as it is now, or select from a list (e.g. enter 1/2/3?

    vocab_selection, answer, answer_def = answer_definition()
    
    print(dedent(f"""Definition: \'{answer_def}\' \nWhich of the following words does this definition pertain to (enter 1, 2, 3, 4)"""))
    
    count = 1
    for items in vocab_selection:
        print(count, ".)      ", items)
        count +=1

    usr_input = input(("(Integer 1, 2, 3, or 4) >>> "))

    try:
        int(usr_input)

    except ValueError:
        print("User, you were given precise instructions. Integers 1 - 4 only.\nLet's try again shall we...")
        return 0
    
    usr_input = int(usr_input)

    if (usr_input -1) not in range(0, len(vocab_selection)):
        print("Regardless of your verbal intellect player, you seem to be struggling with basic maths.")
        sleep(2)
        print("Let's try again shall we...")
        sleep(2)
        return 0

    if vocab_selection[usr_input -1] == answer:
        print("Excellent!")
        return 1

    else:
        print("Incorect. For shame...")
        return 0

def start():

    player_score = 0
    while player_score < 3:
        print(f"Your score is currently {player_score}. You require 3 points to leave and continue with your life.")
        
        # The interactive part of the game is fragmented across this function and user_choice. It might be easier to read if it was all in one place.
        player_score += user_choice()

    # I never got here
    print("Congratualtions. You are a scholar!")
    quit()

print("Welcome player!")
start()