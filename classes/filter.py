class Filter():
    def __init__(self, message):
        pass

    def filterRetweets(self, message):
        ''' Filters all messages starting with RT '''
        
        if(tweet['text'].split(' ')[0] == 'RT'):
            return True

    def filterShortMessages(self, message):
        ''' Check if the tweet contains at least > 3 words '''
        
        if(len(tweet['text'].split(' ')) <= 3):
            return True

    def filterRedudants(self, message):
        ''' Check if the tweet is not already in the list '''
        
        if(any(t.message == tweet['text'] for t in self.tweets)):
            return True
