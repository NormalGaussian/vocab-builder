import pickle

from user_vocab import clean_vocab
from get_defs import word_types
from get_defs import extract_defs

# Takes in a list of single string words
# Returns a dictionary of found vocab, with dictionaries for each 
# found word_type (verb, noun etc) containing a list of all
# relevant definitions


#Any words that were not found to have any types, either due to no url,
#no word found at url, or api limit reached etc


def generate_user_defs(user_vocab):

    vocab_defs = dict({})
    unknown_vocab = []

    for vocab in list(user_vocab):

        defin_by_type = dict({})
        vocab_types = word_types(vocab)

        if vocab_types == None:
            unknown_vocab.append(vocab)
            continue
        
        for word_type in vocab_types:
            defin_by_type[word_type] = extract_defs(vocab, word_type)
            vocab_defs[vocab] = defin_by_type


    return vocab_defs, unknown_vocab


#Function which creates a dictionary storing all words according
#to type (verb/noun etc.) for quick lookup in-game

def generate_wrd_types(user_vocab):

    vocab_types = {'noun': [], 'pronoun': [], 'verb': [], 'adjective': [], 'adverb': [], 'preposition': []}
    no_types_fnd = []

    for vocab in list(user_vocab):

        vocab_forms = word_types(vocab)

        if vocab_forms == None:
            no_types_fnd.append(vocab)
            continue

        else:

            for each_type in vocab_forms:
                    
                try:
                    vocab_types[each_type].append(vocab)

                except KeyError:
                    print(f"{vocab} has {each_type} type which is currently unsupported")
                    pass

    print("No vocab types found for these words:", no_types_fnd)
    return vocab_types



#Create/overwrite to pickle
#Takes in a location name(str) and something to be stored(any obj)
def pickle_vocab(location, gherkins):
    with open(location, 'wb') as file:
        pickle.dump(gherkins, file)


#add without overriding
#requires mulitple load statements to unpick
def append_to_pickle(location, gherkins):
    with open(location, 'ab') as file:
        pickle.dump(gherkins, file)


#Returns all objects that have been pickled
def unpickle_vocab(location):

    pickle_obj = []

    with open(location, 'rb') as file:
        while 1:
            try:
                pickle_obj.append(pickle.load(file))
            except EOFError:
                break
    return pickle_obj


