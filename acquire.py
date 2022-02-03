import requests
from bs4 import BeautifulSoup
import pandas as pd
import os


# create a function that makes the request and saves response to a variable using BeautifulSoup library
def get_soup(link):
    response = requests.get(link, headers={'user-agent': 'codeup data science hopper cohort'})
    soup = BeautifulSoup(response.text, features="lxml")
    
    return soup


# create a function that retrieves title and link and returns a dictionary with these items
def parse_article_info(article):
    # get the article text which is the title
    title = article.text
    # get the link which is tagged with 'a' and has 'href' attribute
    link = article('a')[0]['href']
    # return a dictionary with that info
    return {
        'title': title, 'link': link
    }


# create a function that makes the request and retrieves article content
def parse_article_content(link):
    # use function to make the request and save response to a variable using BeautifulSoup library
    soup = get_soup(link)
    # extract content text under class 'entry-content'
    content = soup.select('.entry-content')[0].text.strip()
    
    return content


# create a function that incorporates other functions to do the entire process
def get_blog_articles():
    # assign link to a variable
    link = 'https://codeup.com/blog/'
    # use function to make the request and save response to a variable using BeautifulSoup library
    soup = get_soup(link)
    # extract content under tag 'h2'
    articles = soup('h2')
    
    # use function to get article link and title
    article_info = pd.DataFrame([parse_article_info(article) for article in articles])
    # create a column and use function to get each article's contentm
    article_info['content'] = article_info.link.apply(parse_article_content)
    
    return article_info


def read_blog_articles(refresh=False):
    if refresh:
        # use function to request data
        df = pd.DataFrame(get_blog_articles())
        # write data locally to a file
        df.to_csv('codeup_blog.csv')

    else:
         # read in data from csv file, if it exists locally
        if os.path.isfile('codeup_blog.csv'):
            df = pd.read_csv('codeup_blog.csv', index_col = 0)
        else:
            # use function to request data
            df = pd.DataFrame(get_blog_articles())
            # write data locally to a file
            df.to_csv('codeup_blog.csv')
        
    return df


    # create a function that retrieves title and content and returns a dictionary with these items
def parse_news_article_info(article, category):
    # parse text under attributes listed to get title
    title = article.find(attrs={"itemprop": "headline"}).text
    # parse text under attributes listed to get content
    content = article.find(attrs={"itemprop": "articleBody"}).text
    # return a dictionary with that info
    return {
        'title': title, 'content': content, 'category': category
    }


# create a function that runs through different topics and returns title, content, and category for each article
def get_news_articles():
    categories = ['business', 'sports', 'technology', 'entertainment']
    news_articles = []
    for category in categories:
        link = 'https://inshorts.com/en/read/' + category
        soup = get_soup(link)
        # parse data under class 'news-card' and assign to a variable
        articles = soup.select('.news-card')
        for article in articles:
            article_info = parse_news_article_info(article, category)
            news_articles.append(article_info)

    return news_articles


def read_news_articles(refresh = False):
    if refresh:
        # use function to request data
        df = pd.DataFrame(get_news_articles())
        # write data locally to a file
        df.to_csv('news_articles.csv')

    else:
         # read in data from csv file, if it exists locally
        if os.path.isfile('news_articles.csv'):
            df = pd.read_csv('news_articles.csv', index_col = 0)
        else:
            # use function to request data
            df = pd.DataFrame(get_news_articles())
            # write data locally to a file
            df.to_csv('news_articles.csv')
        
    return df