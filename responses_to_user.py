from time import sleep


def answer_not_valid(user_input):
    """
    Provides only a text response if invalid input detected from player.
    """

    try:
        input = int(user_input)
    
    except ValueError:

        print("Regardless of your verbal intellect player, you seem to be struggling basic counting...")
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





def berate_user_for_incorrect_answer(total_incorrect_answers, consecutive_incorrect_answers):
    """
    Provides text response to player based on their stats.
    """

    if consecutive_incorrect_answers == 3:
        ex_string = "That's three wrong answers in a row player. Shape up."
        output = ""
        for character in ex_string:
            sleep(0.02)
            output += character
            print(output, end="")
            print("\r", end="")
        sleep(1)

    if consecutive_incorrect_answers == 5:
         
        ex_string = "5 wrong now... You are a fool user, a troglodyte, a bafoon, a plague on the intellect of others."
        output = ""
        for character in ex_string:
            sleep(0.02)
            output += character
            print(output, end="")
            print("\r", end="")
        sleep(1)


