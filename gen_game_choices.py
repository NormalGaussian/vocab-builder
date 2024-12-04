from random import choice
from textwrap import dedent
from random import sample
from time import sleep
from colorama import Fore, Back, Style
import sys
import os


from pickle_vocab import unpickle_vocab
from set_choose import setChoice
from set_choose import setChooseN
from responses_to_user import answer_not_valid
user_vocab_file = "known_vocab.pickle"
user_bytype_file = "vocab_by_type.pickle"

working_vocab_dict = (unpickle_vocab(user_vocab_file)[0])
working_bytype_dict = (unpickle_vocab(user_bytype_file)[0])


# Stores the current state of the players dictionary.
# Removes words they have got right several times.
# Can also be checked to see quantities of word types available.


def check_option_quant(word_type):
    """
    Not implemented. Could be used to check the quantity of vocab options each time
    a question is asked to determine whether the game can still be played. This can
    later be coupled with something that removes answers that are correct.
    """
""" 
    # Here is where I need to check the numbers of vocab types available.
    while True:
        answer_type = setChoice(definitions_by_vocab[answer])
        if len(vocab_by_type[answer_type]) < 4:
            continue
        else:
            print("This is len(vocab_by_type[answer_type]): ", len(vocab_by_type[answer_type]))
            break
 """


def get_player_input(humiliation = None):

    """
    Default request for input - which calls a seperate function which evaluates
    the user input and checks validity (i.e. is string 1-4 or something else).
    Also contains a nested function which clears standard in.
    """

    def clear_standard_in():
        if os.name == 'nt':  # For Windows, use msvcrt
            import msvcrt
            while msvcrt.kbhit():
                msvcrt.getch()
        else:  # For Unix-like systems
            sys.stdin.read()


    print("\nPlease enter an integer from 1 - 4")
        
    clear_standard_in()
    user_input = input(">>> ")

    try:
        input2 = int(user_input)

        if input2 in [1, 2, 3, 4]:
            return input2
        else:
            answer_not_valid(user_input)
            return False
    
    except ValueError:
        answer_not_valid(user_input)
        return False
    


def choose_from_answer(humiliation = None):

    """
    Takes 2 dicts. Chooses an answer at random, then selects one of its word
    types and then finds relevant definition. It then finds relevant misleads based on 
    the answer definition's word type (e.g. other words that have noun_type definitions).
    [Not implemented] Default dictionaries altered if humiliation state activated through
    optional param.
    """

    definitions_by_vocab = working_vocab_dict
    vocab_by_type = working_bytype_dict

    vocab_selection = set()

    attempts = 0

    while attempts < 3:
        answer = setChoice(definitions_by_vocab)
        attempts +=1
        for type_option in definitions_by_vocab[answer]:
            if len(vocab_by_type[type_option]) < 4:
                pass
            else:
                answer_type = type_option
                break
        break

    if attempts == 3:
        print("You have insufficient vocabulary to play the game.")
        sleep(1)
        quit()

    # Is this random enough?
    vocab_selection.add(answer) 
      
    while len(vocab_selection) < 4:
        vocab_selection.add(choice(vocab_by_type[answer_type]))
    

    answer_definition = choice(definitions_by_vocab[answer][answer_type])
                                                                                                                                                                                                                                                                                          
    return answer, answer_definition, list(vocab_selection)    



def generate_question():

    """
    Calls a funtion that creates an answer, a prompt and misleads.
    Then checks this against the result of a function that asks for 
    user input.
    """

    answer, answer_definition, vocab_selection = choose_from_answer()

    while True:

        print(Fore.YELLOW + f"\n\"{answer_definition}\"")
        print(Style.RESET_ALL)
        print("\nWhich of the following words pertain to this definition?\n")
        sleep(0.5)

        count = 1
        for option in vocab_selection:
            print(f"   {count}.) {option}")
            count +=1

        player_input = get_player_input()
        if player_input != False:
            break

        os.system('cls' if os.name == 'nt' else 'clear')


    if answer == vocab_selection[player_input -1]:
        print(Fore.GREEN + "\nCorrect!")
        print(Style.RESET_ALL)
        sleep(1.5)
        return True
    else:
        print(Fore.RED + "\nYou have failed! Bow your head in shame.")
        print(Style.RESET_ALL)
        sleep(1)
        print(f"The correct answer was: {answer}")
        sleep(2)
        return False



def choice_by_type(vocab_by_type: dict):

    """
    OLD selection based on a sampling from a
    random vocab type (this causes sampling error))
    """
    
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

