import pickle
from time import sleep

from user_vocab import clean_vocab
from get_defs import word_types
from get_defs import extract_defs


def generate_user_defs(user_vocab):
    """
    Takes in a list of single string words
    Returns a dictionary of found vocab, with dictionaries for each 
    found word_type (verb, noun etc) containing a list of all
    relevant definitions. Any words that were not found to have any
    types, either due to no url, no word found at url, or api limit
    reached etc.   
    
    """
    vocab_defs = dict({})
    unknown_vocab = []
    iterations = 0
    print("Now creating pickle file 1 of 2")

    for vocab in list(user_vocab):

        iterations += 1
        input_length = len(user_vocab)

        if iterations % 10 == 0:
            print(f"{iterations} of {input_length} words now processed")

        defin_by_type = dict({})
        vocab_types = word_types(vocab)

        if vocab_types == False:
            unknown_vocab.append(vocab)
            continue
        
        for word_type in vocab_types:
            defin_by_type[word_type] = extract_defs(vocab, word_type)
            vocab_defs[vocab] = defin_by_type

    print("No vocab definitions found for these words:", unknown_vocab)
    print("These are all the words not found for pickle 1:", len(unknown_vocab))
    sleep(10)
    return vocab_defs



def generate_wrd_types(user_vocab):

    """
    Creates a dictionary storing all words according
    to type (verb/noun etc.) for quick lookup in-game
    """

    vocab_by_types = {'noun': {}, 'pronoun': {}, 'verb': {}, 'adjective': {}, 'adverb': {}, 'preposition': {}}
    no_types_found = []
    iterations = 0
    print("Now creating pickle file 2 of 2")

    for vocab in list(user_vocab):

        iterations += 1
        input_length = len(user_vocab)

        if iterations % 10 == 0:
            print(f"{iterations} of {input_length} words now processed")

        vocab_forms = word_types(vocab)

        if vocab_forms == False:
            no_types_found.append(vocab)
            continue

        else:

            for each_type in vocab_forms:
                    
                try:
                    vocab_by_types[each_type][vocab] = {}
                    vocab_by_types[each_type][vocab]["concurrent_correct"] = 0
                    vocab_by_types[each_type][vocab]["concurrent_wrong"] = 0
                
                except KeyError:
                    print(f"{vocab} has {each_type} type which is currently unsupported")
                    pass

    print("These are all the words not found for pickle 2:", len(no_types_found))
    sleep(10)

    return vocab_by_types

def pickle_vocab(location, gherkins):
    """
    Create/overwrite to pickle. Takes in a location name(str) and
    something to be stored(any obj)
    """
    with open(location, 'wb') as file:
        pickle.dump(gherkins, file)



def append_to_pickle(location, gherkins):
    """
    Add to pickle without overwriting.
    """

    with open(location, 'ab') as file:
        pickle.dump(gherkins, file)



def unpickle_vocab(location):
    """
    Returns all objects that have been pickled.
    """

    pickle_obj = []

    with open(location, 'rb') as file:
        while 1:
            try:
                pickle_obj.append(pickle.load(file))
            except EOFError:
                break
    return pickle_obj


def create_pickles():

    """
    Creates and writes 2 new pickle files. Stores 1 dict in each.
    "known_vocab.pickle" stores definitions by each words type
    "working_vocab.pickle" stores words only, according to type
    """

    print("Pickling has begun.")
    try:
        pickle_vocab("known_vocab.pickle", generate_user_defs(clean_vocab))
        pickle_vocab("working_vocab.pickle", generate_wrd_types(clean_vocab))
    except Exception as e:
        print(f"Error occurred when trying to create files <known_vocab.pickle> and <vocab_by_type.pickle>: {e}")
        print("Please inform the manufacturer. Have a pleasant day.")
        quit()

    print("Pickling complete")