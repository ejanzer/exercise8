#!/usr/bin/env python

import sys
from random import randint

def make_chains(corpus):
    """Takes an input text as a string and returns a dictionary of
    markov chains."""

    # Split text into words
    words = corpus.split()

    #print words
    # create an empty dictionary
    d = {}

    # account for index out of range at the end

    # Iterate through the list one at a time
    # Check if that pair is in the dictionary
    # If not, add it
    # If it is, add the next word to the value list

    for i in range(len(words) - 2):
        key = (words[i], words[i + 1])
        if not d.get(key):
            d[key] = [words[i + 2]]
        else:
            d[key].append(words[i + 2])

    #for key, value in d.iteritems():
        #print key, value


    # Return the dictionary
    return d

def make_text(chains):
    """Takes a dictionary of markov chains and returns random text
    based off an original text."""
    # putting the keys into a list
    keys = chains.keys()
    # random number to find a valid index within the keys list
    starting_index = randint(0, len(keys) - 1)
    # using the random number to find the tuple in the list of keys
    key = keys[starting_index]

    # create an empty list
    words = [key[0], key[1]]

    # while the randomly chosen tuple exists in the list
    while chains.get(key) and len(words) < 500:
        # get a random value from the values list
        random_number = randint(0, len(chains[key]) - 1)
        random_word = chains[key][random_number]

        # Add the selected word to the list of words
        words.append(random_word)

        # Update the key with a new pair of words from 2nd word of key and 
        # selected word.
        key = (key[1], random_word)
    
    
    # Join list into a string
    return ' '.join(words)


def main():
    args = sys.argv

    script, filename1, filename2 = args
    
    f = open(filename1)
    g = open(filename2)
    input_text = f.read()
    input_text += g.read()
    f.close()
    g.close()

    chain_dict = make_chains(input_text)
    random_text = make_text(chain_dict)
    print random_text

if __name__ == "__main__":
    main()