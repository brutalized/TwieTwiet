#!/usr/bin/python3

''' TwieTwie Application by Arend-Eric, Lesley and Micha '''

import re
from classes.tweets import Tweets
from classes.rhyme import Entry, Rhyme

def main():
    db = Tweets() # init db
    tweets = db.getTweets() # get all tweets
    rhyme = Rhyme('')


    usedTweet = tweets[0].message.split()
    wantedRhymeWord = re.sub(r'\W+', '', usedTweet[len(usedTweet)-1])
    
    for tweet in tweets:
        parts = tweet.message.split()
        lw = re.sub(r'\W+', '', parts[len(parts)-1])

        # Filter if the last word is a URL or empty
        if(lw.find('http') != -1 and lw.strip() != ''):
            continue

        # Ignore if same word as wanted word
        if(wantedRhymeWord == lw):
            continue

        try:
            if(rhyme.compare(wantedRhymeWord, lw)):
                print(tweets[0].message, tweet.message, sep='\n')
                print()
                print()
        except:
            continue            

        

if __name__ == "__main__":
    main()
