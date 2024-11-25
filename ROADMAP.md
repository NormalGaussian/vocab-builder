Roads can be long and windy, with many steps along the way.

The difficulty of the journey is mainly in how nice each pitstop is!

Here is a path; maybe not the path that will be taken - but a path that goes forwards with some nice stops along the way:

# Overview

From a high level, this is what we need to do:

1. Game in the terminal written in python
2. Add a minimal Web Interface so it can be played in a browser from a "question list" using js/ts.
4. Add scoring to the web interface to make it more like a game
5. Save scoring in a database 
6. Add a minimal web scraper for kindle with a browser extension, saving results to a database


Eventually:
* Make it a multi-user system
* Add more scrapers
* Add more games
* Make it look better
* offline mode
* vocab packs
* lots more!

# What next?

Getting a Terminal User Interface (TUI) running for a python game.

What do we need for this to work?

* Project I/O: A way to take an input list of words (`highlights.txt`) and generate a list of questions and answers (`q_and_a.json`) from it.
* Project TUI: A way to take a list of questions and answers (`q_and_a.json`) and ask a "user" to answer each question over the command line - letting them respond, and telling them whether their response was right.

The best way to do these things is "to get something working" then play around with other ways of doing it.

## Project I/O

This is written in the "way the program works", but you might get more reward from doing sections in a different order.

### Extract the vocab

[This](https://pythonspot.com/read-file/) is a good guide for reading a text file in python:


```python
with open(filepath, "r"):
    lines = f.readlines()
```

You'll need to parse the `highlights.txt` to get a list of highlights. Then process your list to get your vocab words - `vocab`. It would be good for vocab to be a [set](https://docs.python.org/3/tutorial/datastructures.html#sets) but its OK if it is a list.

We have vocab!

### Get definitions for the words

[This website](https://dictionaryapi.dev/) lets you get definitions for words. Its probably not got everything, but its a good starting point.

How do we use it?

For each vocab word you are going to need to:
- create a url, `url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{vocab_word}"`
- load the JSON

```python
import urllib.request, json 
with urllib.request.urlopen(url) as response:
    data = json.load(url)
```

You are going to have to work out how to get the right definition, and how to handle the dictionary not having the word! Remember, at this stage, perfect is the enemy of the good enough.

Choose a way to hold the definition for each vocab word for use later. We should come back and talk about caching external requests for performance and reliability, but that doesn't stop us getting it working!

### Make some questions

The easiest form of question you described was "given a definition, allow the user to choose the correct word from a list of words". It seems implicit the other words should be randomly selected.

Python offers a few helpers most languages don't for random selection - look [at the docs](https://docs.python.org/3/library/random.html#functions-for-sequences) for `random.choice`, `random.choices`, and `random.sample` to make some good decisions.

We can come back and talk about "seeding" (or go look it up).

The output from this should be some type of datastructure. Try and only make it from dicts and lists so that the next step is easier. It should have a list of questions and answers, with something to indicate what the right answer is!

### Save the output

In python its pretty easy to save data. You can ["pickle"](https://docs.python.org/3/library/pickle.html) it really easily, which saves python objects in a way that can be read by other python programs. 

However as we intend to use this not just with python, lets do the next easiest - JSONify it with the [json](https://docs.python.org/3/library/json.html#module-json) module. So long as we are using primitives, dicts, and lists in our `output` data structure this is easy.

```python
with open(filepath, 'w') as file:
    json.dump(output, file, indent=2)
```

This can then be easily read with

```python
with open(filepath, 'r') as file:
    data = json.load(file)
```

## Project TUI

Given questions and answers, play a game!

Its possible to build this before the I/O by faking the input file.

The basics are:
* Read questions
* For each question
    * Ask the user
    * Wait for response
    * Be judgy about the response
* Program ends

You need to know how to ask the user a question.

Python has an "input" module

```python
response = input("What is your favourite fruit?")
```

That lets people type an answer and press enter.

To get just a single key we can use the built in libary curses (linux/mac) or mscrvt (windows). Or simply `pip install keyboard` and:

```python
import keyboard

while True:
    # Wait for a key press
    event = keyboard.read_event()
    if event.event_type == keyboard.KEY_DOWN:
        print(f"You pressed: {event.name}")
        if event.name == 'esc':
            break
```

Or to simplify the lot, use a TUI library - e.g. PyInquirer

```python
# nb. I didn't test this code

from PyInquirer import prompt

def ask_question():
    questions = [
        {
            'type': 'list',
            'name': 'language',
            'message': 'What is your favorite programming language?',
            'choices': ['Python', 'Java', 'C++', 'JavaScript'],
        }
    ]

    # Ask the question
    answers = prompt(questions)
    print(f"You chose: {answers['language']}")

ask_question()
```

I'm sure you can have fun with how the question is asked, and how you judge the responses!
