#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 30 13:49:36 2021

@author: johannasundberg
"""

import json

f = open("testfile",'r') 

pro_dict = {'han' : 0, 'hon' : 0,
             'den' : 0, 'det' : 0,
             'denna': 0, 'denne' : 0,
             'hen' : 0, 'tweet_total' : 0}

pronomen = ['han', 'hon', 'den', 'det', 'denna', 'denne', 'hen']


# for i in range(1,300):
#     line = f.readline()
#     if len(line) > 1:
#         tweet = json.loads(line)
#         t = tweet['text']
#         if not tweet['retweeted']:
#             pro_dict['tweet_total'] += 1
#             for p in pronomen:
#                 pro_dict[p] = t.count(p)

with open(filename) as f:

    pronoun_file = {
        'han': 0,
        'hon': 0,
        'den': 0,
        'det': 0,
        'denna': 0,
        'denne': 0,
        'hen': 0,
        'total': 0,
    }

    for line in f:
        if len(line) > 1: # ignore empty lines
            tweet_obj = json.loads(line)
            if not tweet_obj['retweeted']: # ignore retweets
                pronoun_line = count_pronoun(tweet_obj['text'])
                pronoun_file['total'] += 1 # total plus one
                for key, value in pronoun_line.items():
                    pronoun_file[key] += value

        
         


        

    