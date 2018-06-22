import tweepy
import json
import sys
import secret_data
import nltk
import csv

from collections import Counter

username = sys.argv[1]
num_tweets = sys.argv[2]

consumer_key = secret_data.CONSUMER_KEY
consumer_secret = secret_data.CONSUMER_SECRET
access_token = secret_data.ACCESS_KEY
access_secret = secret_data.ACCESS_SECRET


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

api = tweepy.API(auth)

user_tweets = api.user_timeline(id=username,count=num_tweets)
tweets_text=[]
for tweets in user_tweets:
	tweets_text.append(tweets.text)


def tokenize_tweets(tweets_caught):
    tweet_tokens = []
    for tweet in tweets_caught:
        tweet_tokens += nltk.word_tokenize(tweet.text)
    return tweet_tokens

def stop_words(tweet_tokens):
    alphabet = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
    words_to_ignore = ['http','https','RT']
    tweet_tokens_cleared = []
    for word in tweet_tokens:
        word_lower = word.lower()
        if word_lower[0] in alphabet:
            if word not in words_to_ignore:
                tweet_tokens_cleared.append(word)
    return tweet_tokens_cleared

def tag_token(tweet_tokens_cleared):
	tagged_token = nltk.pos_tag(tweet_tokens_cleared)
	return tagged_token

def verb_list_generator(tagged_token):
	verb_list=[]
	for token in tagged_token:
		if token[1].startswith("VB"):
			verb_list.append(token[0])
	return verb_list

def noun_list_generator(tagged_token):
	noun_list=[]
	for token in tagged_token:
		if token[1].startswith("NN"):
			noun_list.append(token[0])
	return noun_list

def adj_list_generator(tagged_token):
	adj_list=[]
	for token in tagged_token:
		if token[1].startswith("JJ"):
			adj_list.append(token[0])
	return adj_list

def top_five_words(tweet_tokens_cleared):
	tweet_tokens_freq = Counter(tweet_tokens_cleared)
	top_five_words = tweet_tokens_freq.most_common(5)
	return top_five_words

def string_for_output(top_five_words):
	common_word = ""
	for token in top_five_words:
		common_word+=token[0]+"("+str(token[1])+") "
	return common_word



tweet_tokens = tokenize_tweets(user_tweets)
tweet_tokens_cleared = stop_words(tweet_tokens)
tagged_token = tag_token(tweet_tokens_cleared)
verb_list=verb_list_generator(tagged_token)
noun_list=noun_list_generator(tagged_token)
adj_list=adj_list_generator(tagged_token)
top_verb=top_five_words(verb_list)
top_noun=top_five_words(noun_list)
top_adj=top_five_words(adj_list)
common_verb=string_for_output(top_verb)
common_noun=string_for_output(top_noun)
common_adj=string_for_output(top_adj)

with open('noun_data.csv','w') as f:
	csv_out = csv.writer(f)
	for row in top_noun:
		csv_out.writerow(row)

original_timeline = api.user_timeline(include_rts=False,id=username,count=num_tweets)
def original_tweets(original_timeline):
	original_counter=0
	for tweet in original_timeline:
			original_counter+=1
	return original_counter

def fav_tweets(original_timeline):
	fav_counter=0
	for tweet in original_timeline:
		fav_counter+=tweet.favorite_count
	return fav_counter

def retweet_tweets(original_timeline):
	retweet_counter=0
	for tweet in original_timeline:
		retweet_counter+=tweet.retweet_count
	return retweet_counter

def output(username,num_tweets):
	print('User:',username)
	print('TWEETS ANALYZED:',num_tweets)
	print('VERBS:',common_verb)
	print('NOUNS:',common_noun)
	print('ADJECTIVES:',common_adj)
	print('ORIGINAL TWEETS:',original_tweets)
	print('TIMES FAVORITED (ORIGINAL TWEETS ONLY):',fav_tweets)
	print('TIMES RETWEETED (ORIGINAL TWEETS ONLY):',retweet_tweets)

original_tweets=original_tweets(original_timeline)
fav_tweets=fav_tweets(original_timeline)
retweet_tweets=retweet_tweets(original_timeline)
output(username,num_tweets)
