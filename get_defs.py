import urllib.request
import time
import json

def lookup_word(word: str, interRequestDelay: float = 0.3, attempts: int = 2) -> list:
    print(f"Looking up word '{word}'")

    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    headers = {
        "User-Agent": "VocabBuilder/1.0 (python)"
    }
    method = 'GET'

    request = urllib.request.Request(url, headers=headers, method=method)

    trial = 0
    while trial < attempts:
        try:
            time.sleep(interRequestDelay)  # 0.3 sleep with 2 attempts has been reliable
            print(f"Attempt {trial+1} to connect to API to lookup '{word}'")
            with urllib.request.urlopen(request) as response:
                if response.status == 200:
                    data = json.load(response)
                    return data
                
                else:
                    # This was a successful request; but it didn't return a 200
                    print(f"Did not get a 200 when looking up '{word}': {response.status}")
                
                trial +=1
               
        except Exception as e:
            # Likely either the request failed (4xx, 5xx) or the json parsing failed
            print(f"Failed to lookup word '{word}': {e}")
            return False
        
        return False
    

def word_types(word):
    
    """
    Returns a set of all found vocab types for a given word from 
    api (e.g. {"verb", "noun"})
    """

    word_types = set()
    current_call = lookup_word(word)

    if current_call != False:
        for items in current_call:
            for mean_items in items['meanings']:
                word_types.add(mean_items['partOfSpeech'])
        if len((word_types)) > 0:
            return word_types

    # returns False whem api exists but no definitions found
    return False
                    


def extract_defs(word, vocab_type = None):

    """
    Returns a list of all definitions for a given word OR 
    all definitions specific to a word type for a given word
    (e.g. noun)
    """

    all_defs = []
    api_result = lookup_word(word)

    # Triggered if optional param specifies a vocab type (e.g. verb)
    if api_result != False and vocab_type != None:
        for items in api_result:
            for mean_items in items['meanings']:
                if mean_items['partOfSpeech'] == vocab_type:
                    for spec_defs in mean_items['definitions']:
                        all_defs.append(spec_defs['definition'])

        if len(all_defs) > 0:
            return all_defs
        return False
    
    # Returns all definiitions of all types
    elif api_result != False:
        for items in api_result:
            for mean_items in items['meanings']:
                for spec_defs in mean_items['definitions']:
                    all_defs.append(spec_defs['definition'])
        if len(all_defs) > 0:
            return all_defs
        else:
            return False

