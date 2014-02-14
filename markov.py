#!/usr/bin/env python

import sys
from random import randint
import twitter
import os

def clean_up_text(text):
    words = text.split()
    for word in words:
        if word == 'Valentine' or word == 'Day':
            word = word.lower()
    return words

def make_chains(input_text, n_gram_size):
    """Takes an input text as a string and returns a dictionary of
    markov chains."""

    words = clean_up_text(input_text)

    d = {}

    # iterate through the words creating n-grams, stopping an n-gram short of the end
    for i in range(len(words) - n_gram_size):
        # build an n-gram to serve as the key in the dictionary (as a tuple)
        key = tuple(words[i:i + n_gram_size])

        # check if the n-gram is already in the dictionary
        if not d.get(key):
            d[key] = [words[i + n_gram_size]]
        else:
            d[key].append(words[i + n_gram_size])

    return d

def make_text(chains, starter_keys):
    """Takes a dictionary of markov chains and returns random text
    based off an original text."""

    key = get_starting_key(starter_keys)

    # Initialize list with the words in the starter key
    words = list(key)
    
    # while the randomly chosen tuple exists in the chains dictionary
    while chains.get(key):
        # get a random value from the values list
        random_number = randint(0, len(chains[key]) - 1)
        random_word = chains[key][random_number]

        # If it ends in a period, break.
        if ends_on_period(words):
            break

        # Check if adding this word will put us over character count. If so, break.
        if is_over_tweet_char_count(words, random_word):
            break

        words.append(random_word)

        # Generate the next key from the existing key and the new word
        new_key = list(key[1:])
        new_key.append(random_word)
        key = tuple(new_key)
    
    return ' '.join(words)

def generate_starter_keys(chains):
    # TODO: Exclude Valentine's, Day or I...?
    starter_keys = []
    """Create a list of all tuples that start with a capital letter."""
    keys = chains.keys()

    for key in keys:
        if ord(key[0][0]) >= ord('A') and ord(key[0][0]) <= ord('Z'):
            starter_keys.append(key)

    return starter_keys

def get_starting_key(starter_keys):
    """Returns a tuple that starts with a capital letter."""
    random_index = randint(0, len(starter_keys) - 1)
    return starter_keys[random_index]

def ends_on_period(words):
    """Return true if the list of words ends in a period."""
    return words[-1][-1] in ['!','?','.']

def generate_tweet(chain_dict, starter_keys):
    """Generate tweets until we find one that ends in a period."""
    while True:
        tweet = make_text(chain_dict, starter_keys)
        if ends_on_period([tweet]):
            return tweet

def is_over_tweet_char_count(words, appended_word):
    """Check if the string is over the character count for twitter"""
    return len(' '.join(words)) > 140

def set_up_twitter_api():
    """Set up the twitter API using the API keys in the local environment."""
    api_key = os.environ.get("TWITTER_API_KEY")    
    api_secret = os.environ.get("TWITTER_API_SECRET")
    access_token = os.environ.get("TWITTER_ACCESS_TOKEN")
    token_secret = os.environ.get("TWITTER_TOKEN_SECRET")

    api = twitter.Api(api_key, api_secret, access_token, token_secret)
    #print api.VerifyCredentials()

    return api

def tweet(api, text):
    """Tweets text using existing twitter API."""
    api.PostUpdate(text)

def main():

    # get filenames from command line arguments
    args = sys.argv

    if len(args) == 1:
        print "Please enter one source file as a command line argument."
        exit(0)

    filenames = args[1:]

    input_text = ""

    for filename in filenames:
        with open(filename) as f:
            input_text += f.read()

    # Prompt for size of n-gram.
    # print "Enter size of n-gram"
    # input_number = raw_input("> ")
    # # error handling
    # while not input_number.isdigit():
    #     print "That's a not a digit. Please enter a digit."
    #     input_number = raw_input("> ")

    # n_gram_size = int(input_number)
    n_gram_size = 2

    chain_dict = make_chains(input_text, n_gram_size)
    starter_keys = generate_starter_keys(chain_dict)
    api = set_up_twitter_api()

    while True:
        tweet_text = generate_tweet(chain_dict, starter_keys)
        print tweet_text
        print "Do you want to tweet this? Press Y to select this tweet or press q to quit or press any other key to see another tweet"
        ans = raw_input("> ")
        if ans.lower() == "y":
            tweet(api, tweet_text)
        elif ans == 'q':
            exit(0)
    

if __name__ == "__main__":
    main()



