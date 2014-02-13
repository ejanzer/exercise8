#!/usr/bin/env python

import sys
from random import randint
import twitter
import os

def make_chains(input_text, n_gram_size):
    # TODO: Make it accept an n-gram size as an argument.
    """Takes an input text as a string and returns a dictionary of
    markov chains."""

    # Split text into words
    words = input_text.split()

    # create an empty dictionary
    d = {}

    # for i in length - size of what's prompted from the user (n_gram_size)
    for i in range(len(words) - n_gram_size):
        # build a key that's the size of the n_gram_size   
        # within the words list, start at the index and go n_gram_sized steps
        n_gram = words[i:i + n_gram_size]
        # turn n_gram into a tuple
        key = tuple(n_gram)

        if not d.get(key):
            # if it's not there, create the key, add whatever comes after the n-gram as a list
            d[key] = [words[i + n_gram_size]]
        else:
            # if it is there, just append whatever comes after the n-gram to the value list
            d[key].append(words[i + n_gram_size])


    # Return the dictionary
    return d

def make_text(chains):
    """Takes a dictionary of markov chains and returns random text
    based off an original text."""

    # using the random number to find the tuple in the list of keys
    key = capitalized_words(chains)

    # puts the tuple with capitalized first item into a list
    words = list(key)
    
    # while the randomly chosen tuple exists in the list
    while chains.get(key):
        # get a random value from the values list
        random_number = randint(0, len(chains[key]) - 1)
        random_word = chains[key][random_number]

        # Call the end_on_period function
        if end_on_period(words):
            break

        #if words + random_word is over 140, we want to break this loop
        if tweet_sized(words, random_word):
            # Add the selected word to the list of words
            words.append(random_word)
        else:
            break

        # Update the key with a new pair of words from 2nd word of key and 
        # selected word.
        tmp = list(key[1:])
        tmp.append(random_word)
        key = tuple(tmp)
    
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

def tweet_sized(words, appended_word):
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

def tweet(text):
    """Takes the text and tweets it on a twitter account using their API"""
    api_key = os.environ.get("TWITTER_API_KEY")    
    api_secret = os.environ.get("TWITTER_API_SECRET")
    access_token = os.environ.get("TWITTER_ACCESS_TOKEN")
    token_secret = os.environ.get("TWITTER_TOKEN_SECRET")

    api=twitter.Api(api_key, api_secret, access_token, token_secret)
    
    #print api.VerifyCredentials()

    api.PostUpdate(text)

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
    print "Enter size of n-gram"
    input_number = raw_input("> ")
    # error handling
    while not input_number.isdigit():
        print "That's a not a digit. Please enter a digit."
        input_number = raw_input("> ")

    n_gram_size = int(input_number)

    chain_dict = make_chains(input_text, n_gram_size)
    random_text = tweet_end_on_period(chain_dict)
    print random_text
    print "Do you want to tweet this? Press Y to select this tweet or press q to quit or press any other key to see another tweet"
    verify = raw_input("> ")
    while verify.lower() != "y":
        if verify == 'q':
            exit(0)
        random_text = tweet_end_on_period(chain_dict)
        print random_text
        print "Do you want to tweet this? Press Y to select this tweet or press q to quit or press any other key to see another tweet"
        verify = raw_input("> ")

    tweet(random_text)
  
         

if __name__ == "__main__":
    main()