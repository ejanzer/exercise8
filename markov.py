#!/usr/bin/env python

import sys

def make_chains(corpus):
    """Takes an input text as a string and returns a dictionary of
    markov chains."""

    # Split text into words
    words = corpus.split()

    #print words
    # create an empty dictionary
    d = {}

    # account for index out of range at the end
    length = len(words) - 2

    # Iterate through the list one at a time
    # Check if that pair is in the dictionary
    # If not, add it
    # If it is, add the next word to the value list

    for i in range(length):
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
    # Randomly pick a value for the key
    keys = chains.keys()
    starting_key = keys[0]

    print starting_key, chains[starting_key]
    # When do we stop?
    # Make a new pair of words from 2nd word of key and 
    # randomly selected word from value.
    # Look up that key.
    # Repeat!
    return None


def main():
    args = sys.argv

    # Change this to read input_text from a file
    script, filename = args
    
    f = open(filename)
    input_text = f.read()
    #print input_text

    chain_dict = make_chains(input_text)
    random_text = make_text(chain_dict)
    # print random_text

if __name__ == "__main__":
    main()