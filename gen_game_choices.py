from random import choice
from textwrap import dedent
from random import sample
from time import sleep
from colorama import Fore, Back, Style
import sys
import os

from pickle_vocab import pickle_vocab
from pickle_vocab import unpickle_vocab
from set_choose import setChoice
from set_choose import setChooseN
from responses_to_user import answer_not_valid

user_vocab_file = "known_vocab.pickle"
user_bytype_file = "working_vocab.pickle"

working_vocab_dict = (unpickle_vocab(user_vocab_file)[0])
working_bytype_dict = (unpickle_vocab(user_bytype_file)[0])


def clear_stdin():

    if os.name == 'nt':  # For Windows, use msvcrt
        import msvcrt
        while msvcrt.kbhit():
            msvcrt.getch()
    else:  # For Unix-like systems
        import sys, termios
        termios.tcflush(sys.stdin, termios.TCIFLUSH)


def player_save_choice():

    """
    Option to save the current game state and concurrent wrong/correct
    answers for a future playthrough. Updates working_vocab.picle
    """

    while True:
        print("Would you like to save your progress for the next playthrough?")

        for option in ["     1.) Yes", "     2.) No"]:
            print(option)
        print("\nPlease press integer 1 or 2 to proceed ")
        clear_stdin()
        user_input = input(">>> ")

        if user_input == "1":
            pickle_vocab("working_vocab.pickle", working_bytype_dict)
            print("Great. Your progress has been saved.")
            return
        elif user_input == "2":
            print("Understood. Your next game will ignore this sessions progress.")
            return
        else:
            print("I didn't catch that user. Please try again")
            sleep(1)
            continue
    


def get_player_answer(humiliation = None):

    """
    Default request for input - which calls a seperate function which evaluates
    the user input and checks validity (i.e. is string 1-4 or something else).
    Also contains a nested function which clears standard in.
    """

    print("\nPlease enter an integer from 1 - 4")
        
    clear_stdin()
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


def update_correct(word, word_type):

    """
    Finds a particular word_defs concurrect_correct count and add 1. 
    If conc_correct == 3, player is given the option to remove 
    the word from their working, testable vocab.
    """
    working_bytype_dict[word_type][word]["concurrent_correct"] +=1
    working_bytype_dict[word_type][word]["concurrent_wrong"] = 0

    if working_bytype_dict[word_type][word]["concurrent_correct"] > 2:  
        
        while True:

            print(f"\nYou seem to have mastered the {word_type} definition for {word}.")
            print("Would you like to remove this from your working vocab library?\n")

            for option in ["     1.) Yes", "     2.) No"]:
                print(option)

            print("\nPlease press integer 1 or 2 to proceed ")
            clear_stdin()
            user_input = input(">>> ")

            if user_input == "1":
                del working_bytype_dict[word_type][word]
                print("This has now been removed from your working vocab list.")
                return
            
            elif user_input == "2":
                working_bytype_dict[word_type][word]["concurrent_correct"] = 1
                print("Understood. This word will remain.")
                return
            
            else:
                print("I didn't catch that user. Please try again")
                sleep(1)


def update_wrong(word, word_type):

    """
    Finds a particular word_defs concurrect_wrong count and adds 1. 
    Not currently utilised elsewhere. Possible future use for
    creating personalised game difficulties.
    """
    working_bytype_dict[word_type][word]["concurrent_wrong"] +=1
    working_bytype_dict[word_type][word]["concurrent_correct"] = 0



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
        print("At present, you have insufficient vocabulary and/or variety of word types to play the game.")
        print("Feel free to include more vocabulary for the game to utilise.")
        sleep(1)
        quit()

    # Is this random enough?
    vocab_selection.add(answer) 
      
    while len(vocab_selection) < 4:
        vocab_selection.add(setChoice(vocab_by_type[answer_type]))
    

    answer_definition = choice(definitions_by_vocab[answer][answer_type])
                                                                                                                                                                                                                                                                                          
    return answer, answer_type, answer_definition, list(vocab_selection)    



def generate_and_ask_question():
    """
    Generates and asks a question to the user.

    @return: True if the user answers correctly, False otherwise.
    """

    answer, answer_type, answer_definition, vocab_selection = choose_from_answer()

    while True:

        print(Fore.YELLOW + f"\n\"{answer_definition}\"")
        print(Style.RESET_ALL)
        print("\nWhich of the following words pertain to this definition?\n")


        count = 1
        for option in vocab_selection:
            print(f"   {count}.) {option}")
            count +=1

        player_input = get_player_answer()
        if player_input != False:
            break

        os.system('cls' if os.name == 'nt' else 'clear')


    if answer == vocab_selection[player_input -1]:
        print(Fore.GREEN + "\nCorrect!")
        print(Style.RESET_ALL)
        update_correct(answer, answer_type) # Updates the concurrent correct guesses for this definition
        sleep(1)
        return True
    else:
        print(Fore.RED + "\nYou have failed! Bow your head in shame.")
        print(Style.RESET_ALL)
        update_wrong(answer, answer_type)
        sleep(1)
        print("The correct answer was:", Fore.YELLOW + f"{answer}")
        print(Style.RESET_ALL)
        sleep(1)
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
