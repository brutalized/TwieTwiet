#!/usr/bin/python3

''' TwieTwie Application by Arend-Eric, Lesley and Micha '''

from classes.tweets import Tweets
from operator import attrgetter

def main():
    db = Tweets() # init db
    tweets = db.getTweets() # get all tweets   

    for i in range(0,5):
       print(tweets[i])

if __name__ == "__main__":
    main()
