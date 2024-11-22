import os.path


filename = "kindle_highlights.txt"

if not os.path.isfile(filename):
    print('File does not exist.')
    quit()
else:
    with open(filename) as f:
        content = f.read().splitlines()

def remove_non_character(word):
    edited_word = [character for character in word if ord(character) in range (97, 123)]
    if len("".join(edited_word)) > 0:
        return "".join(edited_word) 
    # This was implicit before; its not great to have a function `(str) -> str | None``
    return None

# nb. sort was not necessary

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
