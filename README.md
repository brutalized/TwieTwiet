## TwieTwiet - The Rhyming Tweet Finder and Tweet Bot

TwieTwiet is a project made by students of the University of Groningen.
The goal of the program is to find two tweets that rhyme on each other.
This is being done by using Twitter's JSON feed of an hour, and with a filtered
selection of them finding matching tweets.
The matching is done by using the last word of two tweets and comparing them thru the CELEX Corpus.
The result is showed in a GUI. 

### Installation Requirements

To run the program you'll need to have Python 3 and PyQt4 installed.

For the program to work you need to get a copy of CELEX's `dpw.cd` for a chosen language.
Futher more, you'll need enough tweets to match from the Twitter JSON stream, and put this in a compressed file named `demodata.gz`.
Put both files in the root map, and you should be ready to go.

### Usage

You can run the program by running `TwieTwiet.py`, found in the root map (e.g. `path/to/python3/python3 path/to/TwieTwiet/TwieTwiet.py`).

**Posting Tweets on Twitter**

With the paramater `-tweet` you will enter the TweetBot interface, requiring you to input valid 
credentials for your Twitter App (e.g. `TwieTwiet.py -tweet`).
The program will then post a tweet every hour and optionally will post one directly.
Note that to get a different tweet every hour, you will need to use another dataset of tweets.

### Resources

**CELEX**

The Centre for Lexical Information (CELEX) corpus contains lexical databases available in English, Dutch and German. 
CELEX was developed as a joint enterprise of the University of Nijmegen, the Institute for Dutch Lexicology in Leiden, the Max Planck Institute for Psycholinguistics in Nijmegen, and the Institute for Perception Research in Eindhoven.
This corpus can be found on https://catalog.ldc.upenn.edu/LDC96L14, although it is only available for research purposes.
Note that the program is only tested to work with the Dutch lexicon.

**PyQy4**

PyQt4 is a set of Python bindings for Digia's Qt application framework. This frameworks allows UIs to run on any screen and any platform.
You can get a copy on http://www.riverbankcomputing.co.uk/software/pyqt/download, but note that
PyQt4 is dual licensed on all supported platforms under the GNU GPL v3 and the Riverbank Commercial License.

**Python 3**

Python 3 is a open source programming language. You can get a free copy on https://www.python.org/downloads/.

### License

Copyright (c) 2015 http://twitter.com/TwieTwietNL.
All rights reserved.

Redistribution and use in source and binary forms are permitted
provided that the above copyright notice and this paragraph are
duplicated in all such forms and that any documentation,
advertising materials, and other materials related to such
distribution and use acknowledge that the software was developed
by students of the University of Groningen. The name of the
University of Groningen may not be used to endorse or promote products derived
from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED "AS IS" AND WITHOUT ANY EXPRESS OR
IMPLIED WARRANTIES, INCLUDING, WITHOUT LIMITATION, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.
