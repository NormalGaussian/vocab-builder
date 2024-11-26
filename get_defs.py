import requests
import time

def api_call(word: str) -> list:
    
    trial = 0
    time.sleep(0.5)  #0.4 sleep with 2 attempts has had best results

    while trial < 2:

        try:
            url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
            response = requests.get(url)

            if response.status_code == 200:
                    data = response.json()
                    return data          
            else:
                trial +=1
                raise Exception(f"non-200 status code returned for {word}: {response.status_code}")
            

        except Exception:
            print(f"Bad Request - no relvant url found for {word}")
            return None
    

#Returns a set of all found vocab types for a given word (e.g. {"verb", "noun"})
def word_types(word):
    
    word_types = set()
    current_call = api_call(word)
    try:
        if current_call != None:
            for items in current_call:
                for mean_items in items['meanings']:
                    word_types.add(mean_items['partOfSpeech'])
            if len((word_types)) > 0:
                return word_types

    except IndexError:
        print(f"Index Error raised in word_types for {word}.")
        return None
    
    else:
        print(f"Non-index error raised in word_types for {word}.")
                    

#Returns a list of all definitions for a given word OR definitions
#specific to a word type (e.g. noun)
def extract_defs(word, vocab_type = None):

    all_defs = []
    current_call = api_call(word)

    #Triggered if optional param specifies a vocab type (e.g. verb)
    # -> Only returns definitions of that vocab type
    if current_call != None and vocab_type != None:
        for items in current_call:
            for mean_items in items['meanings']:
                if mean_items['partOfSpeech'] == vocab_type:
                    for spec_defs in mean_items['definitions']:
                        all_defs.append(spec_defs['definition'])

        if len(all_defs) > 0:
            return all_defs
        print(f"No definitions of type {vocab_type} found for {word}")
    
    #Returns all definiitions of all types
    elif current_call != None:
        for items in current_call:
            for mean_items in items['meanings']:
                for spec_defs in mean_items['definitions']:
                    all_defs.append(spec_defs['definition'])
        if len(all_defs) > 0:
            return all_defs


print(extract_defs('nascent', 'adjective'))