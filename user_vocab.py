import os.path


filename = "kindle_highlights.txt"

if not os.path.isfile(filename):
    print('File does not exist.')
    quit()
else:
    with open(filename) as f:
        content = f.read().splitlines()

def rmv_non_charac(word):
    edited_word = [character for character in word if ord(character) in range (97, 123)]
    if len("".join(edited_word)) > 0:
        return "".join(edited_word) 

unclean_vocab = sorted({words.lower() for words in content if " " not in words}) #issue here: as single words with spaces excluded
clean_vocab = {rmv_non_charac(word) for word in unclean_vocab}

#print("This is clean_vocab: ", clean_vocab)
