# AUTHOR: PHAN HOAI HUONG NGUYEN (SYLVIA)
# PURPOSE: CREATE A CHAT BOT TO ASSIST ME IN SMALL LITTLE ANNOYING TASKS (MORE OF AN ENTERTAINING PURPOSE THOUGH)

# PACKAGE
import nltk # Natural Language Toolkit
from nltk.chat.util import Chat, reflections # reflections contain a helpful default dictionary

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

import numpy as np # Handy package to work with arrays
import string # Handy package to work with strings
import random # Generate random integer numbers

import sys # Interact with interpreter
from io import StringIO

    # Helpful dataset
nltk.download('punkt')
nltk.download('wordnet')

flag = True

# TEACH HER SOME BASIC PHRASES
talking = [
    # GREETING
    [
        r"Hey|Hi|Hello|Good Morning|Good Afternoon",
        ["Hi!", "Hey there!", "Hey, how are you?", "Hello, how can I help you today?",]
    ],
    [
        r"My name is (.*)",
        ["Hi %l, how can I help you today?", "Hey %l, I'm Giggle Bot!",]
    ],
    # GOODBYE
    [
        r"quit|Bye|Good day!",
        ["Bye~", "Have a good one!",]
    ]
]
BYE = ("quit","Bye","Good day!",)

# SOME TOPICS TO TALK
f = open(r'Topic/programming.txt', 'r', errors = 'ignore')
raw = f.read()
raw = raw.lower()

sent_tokens = nltk.sent_tokenize(raw) # Operate at sentence-level
word_tokens = nltk.word_tokenize(raw) # Operate at word-level
    
    # Lemmatization
lemmer = nltk.stem.WordNetLemmatizer()
def LemTokens(tokens):
    return[lemmer.lemmatize(token) for token in tokens]

    # Remove punctuation
remove_punct = dict((ord(punct), None) for punct in string.punctuation)
def LemNormalize(text):
    return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct)))

    # Chatting trivial topics
def chatting(user_response):
    giggle_response = ""
    sent_tokens.append(user_response) # Try to understand user's request
    # Thinking, thinking, thinking...
    TfidfVec = TfidfVectorizer(tokenizer = LemNormalize) # Change to Giggle's more familiar language
    tfidf = TfidfVec.fit_transform(sent_tokens)
    # Searching through Giggle's books
    vals = cosine_similarity(tfidf[-1], tfidf)
    idx = vals.argsort()[0][-2]
    # Check if the topic is familiar
    flat = vals.flatten()
    flat.sort()
    req_tfidf = flat[-2]
    # Response
    if(req_tfidf==0):
        return "Sorry, I don't feel like talking about that topic right now."
    else:
        giggle_response = giggle_response + sent_tokens[idx]
        return giggle_response

# GIGGLE BOT
def giggle():
    chat = Chat(talking, reflections)
    user_input = quit
    try:
            user_input = input(">")
    except EOFError:
            print(user_input)
    if user_input:
        user_input = user_input[:-1]
        if chat.respond(user_input) != None:
            print(chat.respond(user_input))
        else:
            user_response = user_input
            user_response=user_response.lower()
            if(user_response in BYE):
                flag = False
                print("Have a good one!")
            else:
                print(chatting(user_response))
                sent_tokens.remove(user_response)

# GIGGLE ON-THE-STAGE
if __name__ == "__main__":
    start = True
    while(flag == True):
        if(start == True):
            print("Howdy! Aren't it a beautiful day today :D")
            start = False
        giggle()