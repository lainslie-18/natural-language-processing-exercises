import unicodedata
import re
import json

import nltk
from nltk.tokenize.toktok import ToktokTokenizer
from nltk.corpus import stopwords

import pandas as pd
import numpy as np

from time import strftime

import acquire

def basic_clean(str):
    '''
    This function takes in a string and converts all characters to lowercase, normalizes them, removes special
    characters, and returns a string
    '''
    # convert all to lowercase
    str = str.lower()
    # normalize
    str = unicodedata.normalize('NFKD', str)\
    .encode('ascii', 'ignore')\
    .decode('utf-8', 'ignore')
    # remove anything that is not a letter, number, single quote, or white space
    str = re.sub(r"[^a-z0-9'\s]", '', str)

    stopword_list = stopwords.words('english')

    words = str.split()

    filtered_words = [w for w in words if w not in stopword_list]

    str = ' '.join(filtered_words)

    return str



def tokenize(str):
    '''
    This function takes in a string and uses a tokenizer to break words, punctuation, etc. into discrete units
    '''
    # create tokenize item
    tokenizer = nltk.tokenize.ToktokTokenizer()
    # apply tokenizer to str and assign result to variable 'str'
    str = tokenizer.tokenize(str, return_str=True)
    
    return str


def stem(str):
    '''
    This function takes in a string and uses a stemmer object to attempt to convert words to their base form
    '''
    # create the stemmer object
    ps = nltk.porter.PorterStemmer()
    # split string and loop through each word to apply stemmer
    stems = [ps.stem(word) for word in str.split()]
    # join the split and stemmed words back together on a space
    str = ' '.join(stems)
    
    return str


def lemmatize(str):
    '''
    This function takes in a string and uses a lemmatizer object to attempt to convert words to their root word
    '''
    # create the lemmatizer object
    wnl = nltk.stem.WordNetLemmatizer()
    # split string and loop through each word to apply lemmatizer
    lemmas = [wnl.lemmatize(word) for word in str.split()]
    # join the split and lemmatized words back together on a space
    str = ' '.join(lemmas)
    
    return str


def remove_stopwords(str, extra_words=[], exclude_words=[]):
    '''
    This function takes in a string and removes words that have little or no significance
    '''
    # pull in english stopwords and assign to a variable
    stopword_list = stopwords.words('english')
    # extend stopword_list if additional words are specified
    if extra_words:
        stopword_list = stopword_list.extend(extra_words)
        # remove words if exclusion words are specified
    if exclude_words:
        stopword_list = [stopword_list.remove(word) for word in exclude_words]
    # split string to create a list of words
    words = str.split()
    # filter out words that are not in stopword list
    not_stopwords = [w for w in words if w not in stopword_list]
    
    str = ' '.join(not_stopwords)
    
    return str


def clean_news_data(news_df):
    '''
    This function takes in a dataframe and creates columns that contain cleaned, stemmed, and lemmatized data and returns a dataframe
    '''
    # rename content column to original
    news_df = news_df.rename(columns={'content':'original'})
    # create a clean column with functions applied to original to clean and tokenize content
    news_df['clean'] = news_df.original.apply(lambda x:basic_clean(x)).apply(lambda x:tokenize(x))
    # create stemmed and lemmatized columns with functions applied to original to further clean
    news_df = news_df.assign(stemmed = news_df.clean.apply(stem), lemmatized = news_df.clean.apply(lemmatize))

    return news_df


def clean_codeup_data(codeup_df):
    '''
    This function takes in a dataframe and creates columns that contain cleaned, stemmed, and lemmatized data and returns a dataframe
    '''
    # rename content column to original
    codeup_df = codeup_df.rename(columns={'content':'original'})
    # fill one null value with the reason for it's lack of content
    codeup_df.original.fillna('video', inplace=True)
    # create a clean column with functions applied to original to clean and tokenize content
    codeup_df['clean'] = codeup_df.original.apply(lambda x:basic_clean(x)).apply(lambda x:tokenize(x))
    # create stemmed and lemmatized columns with functions applied to original to further clean
    codeup_df = codeup_df.assign(stemmed = codeup_df.clean.apply(stem), lemmatized = codeup_df.clean.apply(lemmatize))

    return codeup_df


def prep_clean_codeup_data():
    '''
    This function pulls in the codeup blog articles dataframe, cleans and preps it, and returns a dataframe
    '''
    # use function to pull in dataframe
    codeup_df = acquire.read_blog_articles(refresh = False)
    codeup_df = clean_codeup_data(codeup_df)

    return codeup_df


def prep_clean_news_data():
    '''
    This function pulls in the news articles dataframe, cleans and preps it, and returns a dataframe
    '''
    # use function to pull in dataframe
    news_df = acquire.read_news_articles(refresh = False)
    news_df = clean_news_data(news_df)

    return news_df