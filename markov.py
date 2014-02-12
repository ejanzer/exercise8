#!/usr/bin/env python

import sys
from random import randint

def make_chains(input_text):
    # TODO: Make it accept an n-gram size as an argument.
    """Takes an input text as a string and returns a dictionary of
    markov chains."""

    # Split text into words
    words = input_text.split()

    #print words
    # create an empty dictionary
    d = {}

    # account for index out of range at the end

    # Iterate through the list one at a time
    # Check if that pair is in the dictionary
    # If not, add it
    # If it is, add the next word to the value list

    # TODO: Make this work with other n-gram sizes.
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

    # using the random number to find the tuple in the list of keys
    key = capitalized_words(chains)

    # create an empty list
    # TODO: Accept different sizes of n-grams. Use a for loop?
    words = [key[0], key[1]]

    # while the randomly chosen tuple exists in the list
    while chains.get(key) and tweet_sized(words):
        # get a random value from the values list
        random_number = randint(0, len(chains[key]) - 1)
        random_word = chains[key][random_number]

        # Call the end_on_period function
        if end_on_period(words):
            break

        # Add the selected word to the list of words
        words.append(random_word)

        # Update the key with a new pair of words from 2nd word of key and 
        # selected word.
        # TODO: Adjust for different n-gram sizes. key[-1]?
        key = (key[1], random_word)
    
    
    # Join list into a string
    return ' '.join(words)

def capitalized_words(d):
    """Returns a tuple that starts with a capital letter."""
    # putting the keys into a list
    keys = d.keys()

    # Repeat until we find one that's capitalized
    while True:
        # random number to find a valid index within the keys list
        random_index = randint(0, len(keys) - 1)

        # get the first letter of the first word in the randomly selected tuple
        first_letter = keys[random_index][0][0]
        #print first_letter

        # Check the ASCII value of the first letter of the first word
        if ord(first_letter) >= 65 and ord(first_letter) <= 90:
            #print "It's capitalized! Returning the tuple: ",
            #print keys[random_index]

            # Return the capitalized tuple
            return keys[random_index]
        #else:
            #print "Not capitalized!"

def end_on_period(words):
    """Verifies the list of words ends in a period."""
    # Grab the last word
    last_word = words[-1]
    # print last_word
    last_letter = last_word[-1]
    # print last_letter

    # if the last letter of the word ends in a period return True
    if last_letter == "." or last_letter == "?" or last_letter == "!":
        return True    

    return False

def tweet_end_on_period(chain_dict):
    """End the tweet on a period."""

    # loop through each tweet until it finds one that ends in a period
    while True:
        tweet = make_text(chain_dict)
        #print set_of_words
        split_words = tweet.split()
        #print split_words
        if end_on_period(split_words):
            return tweet
        #else:
            #print "This does not end in a period"

def tweet_sized(words):
    """If longer than 140 characters return False, otherwise return True."""

    # determine how many characters words consists of
    string = ' '.join(words)
    length_of_string = len(string)

    if length_of_string > 140:
        # print length_of_string
        return False
    else:
        # print length_of_string
        return True        

def main():
    args = sys.argv

    # accept an arbitrary number of source files
    filenames = args[1:]

    # put all of the source files into one string
    
    input_text = ""

    for f in filenames:
        o = open(f)
        input_text += o.read()
        o.close()

    # Prompt for size of n-gram.
    # print "Enter size of n-gram"
    # n_gram_size = int(raw_input("> "))
    # TODO: yell at them to only put in an int

    # TODO: Pass n_gram_size to make_chains as an argument.
    chain_dict = make_chains(input_text)
    random_text = tweet_end_on_period(chain_dict)
    print random_text

if __name__ == "__main__":
    main()