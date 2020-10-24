from tweepy import OAuthHandler
from tweepy import API
from tweepy import Cursor
from datetime import datetime, date, time, timedelta
from collections import Counter
import sys
import os
import pandas as pd
import numpy as np
from numpy.compat import long
from tweepy.error import TweepError
import csv
from homer.analyzer import Article
from textstat.textstat import textstatistics, easy_word_set, legacy_round
from textblob import TextBlob
from fkscore import fkscore
import nltk
import re
import ssl

DEFAULT_PATH = "C:\\Users\\eduardo\\Desktop\\jupyter\\twitter-filter\\twitter-scraper\\dataset\\"
CONSUMER_KEY = "z5IGwfi4AYHzYEWPE603JLSlo"
CONSUMER_SECRET = "Q7oCmuFoAH7j6DhvyX7ZgrniyBdXwupIfXTuBrW4hbDpzugSDH"
ACCESS_TOKEN = "1265835995741794310-rnsOUjJ6lAoSW0jY0j6GYiu3qGyXdx"
ACCESS_TOKEN_SECRET = "vV5yjsFTjGPT6KpuQDgwbdNhdkSsGeHEjg1xA76m5ZfV4"
REGEX_EMAIL = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"

# Lee Direcctorio y carga archivos de forma recursiva


def get_files(path):
    files = []
    # r=root, d=directories, f = files
    for r, d, f in os.walk(path):
        for file in f:
            if '.csv' in file:
                files.append(os.path.join(r, file))
    return files

# Inicia sesion en Twitter API


def auth_in_twitter(consumer_key, consumer_secret, access_token, access_token_secret):
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    auth_api = API(auth)
    print(auth_api)
    return auth_api

# Crea Archivo


def create_csv_file():
    with open('corona_tweets.csv', 'a', newline="") as csvfile:
        filewriter = csv.writer(csvfile, delimiter='|',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        filewriter.writerow(['tweetId', 'text', 'userName',  'userId', 'followers', 'like_count', 'retweet_count', 'verified', 'Num_Urls', 'Num_words',
                             'Num_Syllables', 'Num_Sentences', 'Flesh.Kincaid', 'Avg_Words_in_Sentences', 'Avg_Syllables', 'Num_Big_words', 'Num_Short_Sentences'])

# Escribe en archivo


def reg_to_csv_file(tweetId, text, userName,  userId, followers, likes, retweet, verified, num_urls, num_words,  num_syllables, num_sentences, FleshKincaid, avg_words_in_sentences, avg_syllables_per_word, num_big_words, num_short_sentences):
    with open('corona_tweets.csv', 'a', newline="", encoding="utf-8") as csvfile:
        filewriter = csv.writer(csvfile, delimiter='|',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        filewriter.writerow([str(tweetId), ' '.join([line.strip() for line in text.strip().splitlines()]), userName,  (userId), (followers), (likes), (retweet), verified,
                             num_urls, (num_words),  (num_syllables), (num_sentences), FleshKincaid, avg_words_in_sentences, avg_syllables_per_word, num_big_words, num_short_sentences])


def avg_words_in_sentences(text):
    sentence = text
    words = sentence.split()
    lengths = [len(word) for word in words]
    return sum(lengths)/len(lengths)


def avg_syllables_per_word(text, syllables_count, word_count):
    ASPW = float(syllables_count) / float(word_count)
    return legacy_round(ASPW, 1)


def num_big_words(text):
    bigWord = 0
    tb = TextBlob(text)
    for w in tb.words:
        if(len(w) > 6):
            bigWord += 1
    return bigWord


def num_short_sentences(text):
    shortSentence = 0
    tokens = nltk.sent_tokenize(text)
    for sentence in tokens:
        print(sentence)
        tb = TextBlob(sentence)
        if(len(tb.words) < 8):
            shortSentence += 1
    return shortSentence


def num_urls(text):
    # regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
    url = re.findall(REGEX_EMAIL, text)
    print('num_urls')
    print(url)
    return [x[0] for x in url]


def build_dataset(path):
    create_csv_file()

    if(path):
        files = get_files(path)
    else:
        files = get_files(DEFAULT_PATH)

    for f in files:
        ds = pd.read_csv(f)
        tweetsList = ds.iloc[:, 0]
        for id in tweetsList:
            find_tweet_by_id(id)
            # try:
            #     if (tweet) :

            # except TweepError as e:
            #     continue



def find_tweet_by_id(id_tweet):
    auth_api = auth_in_twitter(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    print(id_tweet)
    try:
        tweet = auth_api.get_status(id_tweet)
        if(tweet) :
            print("The text of the status is : \n\n" + tweet.text)
            print("\nThe status was posted by : " + tweet.user.screen_name)
            print("\nThe status was ID posted by  : " + str(tweet.user.id))
            print("\nThe number of folowers from  posted by : " + str(tweet.user.followers_count))
            print("The status has been liked " +  str(tweet.favorite_count) + " number of times.")
            print("The status has been retweeted " +  str(tweet.retweet_count) + " number of times.")
            print("\nThe status was posted is  verified: " + str(tweet.user.verified))
            f = fkscore(tweet.text)
            print(f.stats['num_words'])
            print(f.stats['num_syllables'])
            print(f.stats['num_sentences'])
            print(f.score['readability'])
            print(avg_words_in_sentences(tweet.text))
            print(avg_syllables_per_word(tweet.text,
                                        f.stats['num_syllables'], f.stats['num_words']))
            print(num_big_words(tweet.text))
            print(num_short_sentences(tweet.text))
            print("num_urls->"+str(len(num_urls(tweet.text))))
            reg_to_csv_file(id_tweet, tweet.text, tweet.user.screen_name, tweet.user.id, tweet.user.followers_count, tweet.favorite_count, tweet.retweet_count, tweet.user.verified,
                            len(num_urls(tweet.text)), f.stats['num_words'], f.stats['num_syllables'], f.stats['num_sentences'], f.score['readability'], avg_words_in_sentences(tweet.text),
                            avg_syllables_per_word(tweet.text, f.stats['num_syllables'], f.stats['num_words']), num_big_words(tweet.text), num_short_sentences(tweet.text))

    except TweepError as e:
        print(e)
    #     continue


def build_metrics_socialnet() :
    return None

def build_metrics_leng() :
    return None