import os.path


# This file reading is good, but it can be done better.

## Immediate things:
# Sanitization can be done better; at the very least 
#
## Quick things:
# Better comments about what is happening.
# Add some context to the error messages - what file does not exist?
# exit with a non-zero status code on error - this is a good practice and probably a new concept for you.
#
## Harder future things:
# - consider offering an interface over a singleton
# - we can look at logging in more detail
# - consider caching.
# - consider more complex techniques for parsing and cleaning data

filename = "kindle_highlights.txt"

if not os.path.isfile(filename):
    print('File does not exist.')
    quit()
else:
    with open(filename) as f:
        content = f.read().splitlines()

def remove_non_character(word):
    # Whats going on here? What is happening is neither trivial nor obvious, thus it is prone to bugs.
    # Also consider the name of your assigned variable; it is not a word, but a list of characters.
    edited_word = [character for character in word if ord(character) in range (97, 123)]
    # `"".join(edited_word)`` repeated is a bit of a code smell; we can just do it once.
    if len("".join(edited_word)) > 0:
        return "".join(edited_word) 
    # This was implicit before; its not great to have a function `(str) -> str | None``
    return None

# nb. sort was not necessary
# nb. the two sets were not necessary

clean_vocab = set()
for line in content:

    # Removes any leading or trailing whitespace
    line = line.strip()

    if " " in line:
        # Skip any lines that contain spaces, as they are probably not single words
        continue

    # sanitizes the word by removing any non-alphabetic characters and converting to lowercase
    word = remove_non_character(line.lower())

    if word is not None:
        clean_vocab.add(word)

#print("This is clean_vocab: ", clean_vocab)
