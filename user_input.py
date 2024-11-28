from textwrap import dedent
from time import sleep
from random import choice

savage1 = {"ducky": "Has feathers and goes quack quack", "red": "The colour your face should be", "cup": "sippy sippy", "feeble": "An assessment of your mental prowess..."}


def check_input(user_input):

    evaluation = False

    try:
        int(user_input)

    except ValueError:
        sleep(2)
        print("User, you were given precise instructions.")
        sleep(2)
        print("Integers 1 - 4 only.")
        sleep(2)
        print("Let's try again shall we...")
        sleep(2)
        return evaluation
    
    except:
        sleep(2)
        print("Ah... trying to be clever I see...")
        sleep(2)
    
    user_input = int(user_input)

    if (user_input) not in range(1, 5):
        sleep(2)
        print("Regardless of your verbal intellect player, you seem to be struggling with basic maths.")
        sleep(2)
        print("Let's try again shall we...")
        sleep(3)

    else:
        evaluation = True
    
    return evaluation



def check_response(wrong, conc_wrong):

    if conc_wrong == 3:
        sleep(2)
        print("That's 3 wrong answers in a row player. Shape up...\n\n")
        sleep(2)

    if conc_wrong == 5:
        sleep(2)
        print("This might be a little advanced for you player...\n\n")
        sleep(2)



