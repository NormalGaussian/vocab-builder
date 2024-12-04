from textwrap import dedent
from time import sleep
from random import choice

savage1 = {"ducky": "Has feathers and goes quack quack", "red": "The colour your face should be", "cup": "sippy sippy", "feeble": "An assessment of your mental prowess..."}



def answer_not_valid(user_input):

    """
    Provides only a text response if invalid input detected from player.
    """

    try:
        input = int(user_input)
    
    except ValueError:

        print("Regardless of your verbal intellect player, you seem to be struggling with basic maths.")
        sleep(1)
        print("Let's try again shall we...")
        sleep(1)
        return False

    if user_input not in [1, 2, 3, 4]:
        
        print("\nUser, you were given precise instructions.")
        print("Integers 1 - 4 only.")
        sleep(1)
        print("Let's another one shall we...")
        sleep(1)
        return False





def check_response(wrong, concurrent_wrong):

    """
    Provides text response to player based on their stats.
    """

    if concurrent_wrong == 3:
        ex_string = "That's three wrong answers in a row player. Shape up."
        output = ""
        for character in ex_string:
            sleep(0.02)
            output += character
            print(output, end="")
            print("\r", end="")
        sleep(1)

    if concurrent_wrong == 5:
         
        ex_string = "5 wrong now... You are a fool user, a troglodyte, a bafoon, a plague on the intellect of others."
        output = ""
        for character in ex_string:
            sleep(0.02)
            output += character
            print(output, end="")
            print("\r", end="")
        sleep(1)


