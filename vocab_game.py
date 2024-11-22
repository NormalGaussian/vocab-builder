import get_defs
from user_vocab import clean_vocab
from get_defs import word_types
from get_defs import extract_defs

from random import sample
from random import choice


def check_correct():
    """
    Checks to see if a given word has a url associated
    Checks to see if a given word has vocab_types associated
    Generates a new word if not
    """

    answer = choice(list(clean_vocab))

    while word_types(answer) == None:
        answer = choice(list(clean_vocab))
        
    return answer
 


#returns set of relevant words (defined as relevant if they share
#the chosen vocab_type of the correct word)
def vocab_choices():
    
    vocab_selection = []
    answer = check_correct()
    answer_type = choice(list(word_types(answer)))
    misdirect_vocab = check_correct()

    while len(vocab_selection) < 3:
        types = word_types(misdirect_vocab)
        
        # Handle an edge case, which is likely a bug elsewhere.
        if types == None:
            misdirect_vocab = check_correct()
            continue

        l_word_types = list(types)
        if answer_type in l_word_types:
            vocab_selection.append(misdirect_vocab)
        misdirect_vocab = check_correct()

    vocab_selection.append(answer)
    return vocab_selection, answer, answer_type


#returns definitions of the relevant type from the chosen words
def answer_definition():
    
    vocab_selection, answer, answer_type = vocab_choices()

    answer_def = choice(extract_defs(answer, answer_type))

    return vocab_selection, answer, str(answer_def)

def user_choice():

    vocab_selection, answer, answer_def = answer_definition()
    
    print("Welcome player!")
    print(f"Definition: \'{answer_def}\'")
    print("Which of the following words does this definition pertain to: ")
    for items in vocab_selection:
        print("      ", items)

    if input("(lower case) >>> ") == answer:
        print("Excellent!")
        return 1

    else:
        print("Incorect. For shame...")
        return 0

def start():

    player_score = 0
    while player_score < 3:
        print(f"Your score is currently {player_score}. You require 3 points to leave.")
        
        player_score += user_choice()

    print("Congratualtions. You are a scholar!")
    quit()


start()