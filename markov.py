"""Generate Markov text from text files."""

import sys

from random import choice


def open_and_read_file(file_path):
    """Take file path as string; return text as string.

    Takes a string that is a file path, opens the file, and turns
    the file's contents as one string of text.
    """

    initial_text = open(file_path).read()

    return initial_text


def make_chains(text_string):
    """Take input text as string; return dictionary of Markov chains.

    A chain will be a key that consists of a tuple of (word1, word2)
    and the value would be a list of the word(s) that follow those two
    words in the input text.

    For example:

        >>> chains = make_chains("hi there mary hi there juanita")

    Each bigram (except the last) will be a key in chains:

        >>> sorted(chains.keys())
        [('hi', 'there'), ('mary', 'hi'), ('there', 'mary')]

    Each item in chains is a list of all possible following words:

        >>> chains[('hi', 'there')]
        ['mary', 'juanita']

        >>> chains[('there','juanita')]
        [None]
    """

    chains = {}

    split_text = text_string.split()

    split_length = len(split_text)

    #Loop through all words in the split text list expect for final two words
    for i in range(split_length - 2):
        bigram = (split_text[i], split_text[i + 1])
        if bigram in chains:
            chains[bigram].append(split_text[i + 2])
        else:
            chains[bigram] = [split_text[i + 2]]

    #Add final tuple using negative indicies
    final_tuple = (split_text[-2], split_text[-1])

    #if its in chains get the list and concat with a None type
    chains[final_tuple] = chains.get(final_tuple, []) + [None]

    return chains


def make_text(chains):
    """Return text from chains."""

    words = []
    chosen_word = ""

    #This loop means: While the chosen word is not None or "".
    while not chosen_word:
        initial_key = choice(chains.keys())
        if initial_key[0][0].isupper():
            chosen_word = choice(chains[initial_key])

    words.extend([initial_key[0], initial_key[1], chosen_word])

    new_key = (initial_key[1], chosen_word)

    #punc_count = 0
    while chosen_word is not None:
        current_key = new_key
        chosen_word = choice(chains[current_key])
        new_key = (current_key[1], chosen_word)
        if chosen_word is not None:
            words.append(chosen_word)

    return " ".join(words)


input_path = sys.argv[1]

# Open the file and turn it into one long string
input_text = open_and_read_file(input_path)

# Get a Markov chain
chains = make_chains(input_text)
# print chains

# Produce random text
random_text = make_text(chains)

print random_text
