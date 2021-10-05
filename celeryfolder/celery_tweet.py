#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  5 15:35:18 2021

@author: johannasundberg
"""
import json
import os
from celery import Celery

app = Celery('celery_tweet', broker='pyamqp://guest@localhost//')

@app.task
def prounoun_counter():
    all_files = os.listdir('data')#list all files containing tweets

    statistics = {'han': 0,
                  'hon': 0,
                  'den': 0,
                  'det': 0,
                  'denna': 0,
                  'denne': 0,
                  'hen': 0,
                  'total tweets': 0}
    
    for file in all_files:
        print(file)
        if not file == '.DS_Store':
            file_stat = file_scan('data/' + file)
        
        for key in statistics:
            if key in file_stat:
                statistics[key] += file_stat[key]
     
                
    #result_file = open('result.json', 'w')
    #json.dump(statistics, result_file)
    #result_file.close()
    return json.dumps(statistics)

def tweet_scan(tweet):
    count = dict()
    pronoun = ['han', 'hon', 'den', 'det', 'denna', 'denne', 'hen']
    
    t = tweet.split(' ')
    for p in pronoun:
        count[p] = t.count(p)

    return count


def file_scan(filename):
    
    file_statistics = {'han': 0,
                    'hon': 0,
                    'den': 0,
                    'det': 0,
                    'denna': 0,
                    'denne': 0,
                    'hen': 0,
                    'total tweets': 0}
    
    with open(filename) as file:
    
        for line in file:
                
            if not line.strip() == '':            
                tweet_obj = json.loads(line)
                
                if not tweet_obj['retweeted']:
                    pro_in_tweet = tweet_scan(tweet_obj['text'])
                    file_statistics['total tweets'] += 1
                    
                    for key in file_statistics:
                        if key in pro_in_tweet:
                            file_statistics[key] += pro_in_tweet[key]
                            
    return file_statistics
 