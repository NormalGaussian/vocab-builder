import requests
import time

def api_call(word: str) -> list:
    
    trial = 0
    time.sleep(0.5)  #0.4 sleep with 2 attempts has had best results
    while trial < 2:
        trial +=1
        try:
            url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
            response = requests.get(url)

            if response.status_code == 200:
                    data = response.json()
                    #print(f"Data found for {word}")
                    return data
            
            else:
                print(f"This was the error code: {response.status_code}")
        except:
            print(f"Bad Request - no relvant url found for {word}")
            return None
    

#Returns a set of all found vocab types for a given word (e.g. {"verb", "noun"})
def word_types(word):
    
    word_types = set({})
    current_call = api_call(word)
    try:
        if current_call != None:
            for items in current_call:
                for mean_items in items['meanings']:
                    word_types.add(mean_items['partOfSpeech'])
            if len(list(word_types)) > 0:
                return word_types
            else:
                return None
    except:
        return None
                    

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
    elif api_call(word) != None:
        for items in api_call(word):
            for mean_items in items['meanings']:
                for spec_defs in mean_items['definitions']:
                    all_defs.append(spec_defs['definition'])
        if len(all_defs) > 0:
            return all_defs
    
    return None

