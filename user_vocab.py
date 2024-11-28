import os.path

filename = "kindle_highlights.txt"


#checks file exists
if not os.path.isfile(filename):
    raise Exception('File does not exist.')


#checks file is of supported type (.txt only at present)
if filename.endswith('.txt'):
    pass
else:  
    raise Exception("user_vocab parsing curently unsupported file type")

    
with open(filename) as f:

    content = f.read().splitlines()

#removes any characters that are not letters ('abc')
def remove_non_alpha_characters(word):

    edited_word = [character for character in word if ord(character) in range (97, 123)]
    only_characters = "".join(edited_word) 
    if len(only_characters) > 0:
        return only_characters


clean_vocab = set()
for line in content:

    # Removes any leading or trailing whitespace
    line = line.strip()

    if " " in line:
        # Skip any lines that contain spaces, as they are probably not single words
        continue

    # sanitizes the word by removing any non-alphabetic characters and converting to lowercase
    word = rmv_non_charac(line.lower())

    if word is not None:
        clean_vocab.add(word)


