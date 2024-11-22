import requests

# In this file, focus on:
# - error handling as a concept
# - not calling your most expensive API function so frequently

def api_call(word: str) -> list:
    
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    response = requests.get(url)

    if response.status_code == 200:
            data = response.json()
            #print(f"Data found for {word}")
            return data
    else:
            # Silent failure like this is a bad idea.
            # Look into exceptions and error handling.
            raise Exception(f"non-200 status code returned for {word}: {response.status_code}")
            #print(f"Bad Request - no relvant url found for {word}")
            return None
    

#Returns a set of all found vocab types for a given word (e.g. {"verb", "noun"})
def word_types(word):
    
    word_types = set({}) # set() is a better way to create an empty set. set({}) is creating a set by iterating over an empty dictionary.

    try:
        # Using error handling simplifies this call
        if api_call(word) != None:
            # Oh no! we are calling the API with the exact same word twice in rapid succession; its better not to do that.
            for items in api_call(word):
                for mean_items in items['meanings']: # Naming
                    word_types.add(mean_items['partOfSpeech'])
            if len(list(word_types)) > 0: # You can just len(word_types) - it is a set.
                return word_types
            
    except:
        # Is it better to return None, the empty set, or raise an exception?
        return None
                    

#Returns a list of all definitions for a given word OR definitions
#specific to a word type (e.g. noun)
def extract_defs(word, vocab_type = None):

    all_defs = []

    #Triggered if optional param specifies a vocab type (e.g. verb)
    # -> Only returns definitions of that vocab type
    if api_call(word) != None and vocab_type != None:
        for items in api_call(word):
            for mean_items in items['meanings']:
                if mean_items['partOfSpeech'] == vocab_type:
                    for spec_defs in mean_items['definitions']:
                        all_defs.append(spec_defs['definition'])
                else:
                    pass
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
    

    else:
        # 👀
        return None

