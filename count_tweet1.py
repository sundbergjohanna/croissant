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
from integrate_celery_flask import make_celery

#def make_celery(app):
#    celery = Celery(app.import_name, backend='rpc://',
#                    broker='pyamqp://guest@localhost//')
#    celery.conf.update(app.config)
#
#    class ContextTask(celery.Task):
#        def __call__(self, *args, **kwargs):
#            with app.app_context():
#                return self.run(*args, **kwargs)
#
#    celery.Task = ContextTask
#    return celery

flask_app = Flask(__name__)
flask_app.config.update(
    CELERY_BROKER_URL= 'pyamqp://guest@localhost//',
    CELERY_RESULT_BACKEND= 'rpc://')

celery = make_celery(flask_app)

#flask_app = Flask(__name__)
#celery = make_celery(flask_app)
#app = Celery('celery_tweet', broker='pyamqp://guest@localhost//')

#flask_app = Flask(__name__)
#flask_app.config.update(
#    #CELERY_BROKER_URL="pyamqp://localhost//",
#    #CELERY_RESULT_BACKEND="rabbitmq://"
#    CELERY_BROKER_URL=os.environ.get("CELERY_BROKER_URL"),
#    CELERY_BACKEND_URL=os.environ.get("CELERY_BACKEND_URL"),
#)
#celery = make_celery(flask_app)

# Flask methods
@flask_app.route('/', methods=['GET'] )
def get_count():
    result = pronoun_counter.delay()
    return jsonify(result.get())


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
                  'hen': 0,
                  'total': 0}
    
    for file in all_files:
        #print(file)
        if not file == '.DS_Store':
            file_stat = file_scan('data/' + file)
        
            for key in statistics:
                if key in file_stat:
                    statistics[key] += file_stat[key]
     
                
    #result_file = open('result.json', 'w')
    #json.dump(statistics, result_file)
    #result_file.close()
    #return json.dumps(statistics)
    return statistics

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
                    'total': 0}
    
    with open(filename) as file:
    
        for line in file:
                
            if not line.strip() == '':            
                tweet_obj = json.loads(line)
                
                if not tweet_obj['retweeted']:
                    pro_in_tweet = tweet_scan(tweet_obj['text'])
                    file_statistics['total'] += 1
                    
                    for key in file_statistics:
                        if key in pro_in_tweet:
                            file_statistics[key] += pro_in_tweet[key]
                            
    return file_statistics

if __name__ == '__main__':
    flask_app.run(host='0.0.0.0',debug=True)
 
