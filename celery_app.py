#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  5 15:35:18 2021

@author: johannasundberg
"""
import json
import os
from celery import Celery
from flask import Flask, jsonify

def make_celery(app):
    #from https://flask.palletsprojects.com/en/2.0.x/patterns/celery/
    celery = Celery(app.import_name, backend='rpc://',
                    broker='pyamqp://guest@localhost//')
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery

flask_app = Flask(__name__)
celery = make_celery(flask_app)

# Flask methods
@flask_app.route('/norm', methods=['GET'] )
def get_count():
    norm_res = pronoun_counter.delay()
    norm_result = norm_res.get()
    return jsonify(norm_result)


#@celery.task(name='task_celery.prounoun_counter')
@celery.task(name='make_celery.pronoun_counter')
def pronoun_counter():
    all_files = os.listdir('data')#list all files containing tweets

    statistics = {'han': 0,
                  'hon': 0,
                  'den': 0,
                  'det': 0,
                  'denna': 0,
                  'denne': 0,
                  'hen': 0}
    
    total_tweets = 0
    
    for file in all_files:
        print(file)
        if not file == '.DS_Store':
            file_stat, total_tweets = file_scan('data/' + file, total_tweets)
        
        for key in statistics:
                statistics[key] += file_stat[key]
     
    #Normalize
    norm = statistics
    for key in statistics:
        norm[key] = statistics[key]/total_tweets
                
    #result_file = open('result.json', 'w')
    #json.dump(statistics, result_file)
    #result_file.close()
    #return json.dumps(statistics)
    return norm

def tweet_scan(tweet):
    count = dict()
    pronoun = ['han', 'hon', 'den', 'det', 'denna', 'denne', 'hen']
    
    t = tweet.split(' ')
    for p in pronoun:
        count[p] = t.count(p)

    return count


def file_scan(filename, total):
    
    file_statistics = {'han': 0,
                    'hon': 0,
                    'den': 0,
                    'det': 0,
                    'denna': 0,
                    'denne': 0,
                    'hen': 0}
    
    with open(filename) as file:
    
        for line in file:
                
            if not line.strip() == '':            
                tweet_obj = json.loads(line)
                
                if not tweet_obj['retweeted']:
                    pro_in_tweet = tweet_scan(tweet_obj['text'])
                    total += 1
                    
                    for key in pro_in_tweet:
                        file_statistics[key] += pro_in_tweet[key]
                            
    return file_statistics, total

if __name__ == '__main__':
    flask_app.run(host='0.0.0.0',debug=True)
 
