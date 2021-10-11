#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  5 15:35:18 2021
@author: johannasundberg
"""
import json
import os
from celery import Celery
from flask import Flask, jsonify, Response

#Matplotlib + IO to plot the requirements
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io

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
@flask_app.route('/plot', methods=['GET'] )
def get_count_norm():
    res = pronoun_counter.delay()
    result = res.get()
    norm = result.copy()
    norm.pop('total')
    for key in result:
        norm[key] = result[key]/result['total']
    
    keys = norm.keys()
    count = norm.values()
    
    fig = create_figure(keys, count)
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    
    return Response(output.getvalue(), mimetype='image/png')

@flask_app.route('/result', methods=['GET'] )
def get_count():
    res = pronoun_counter.delay()
    result = res.get()
    return jsonify(result)

#Celery task normalized result
@celery.task(name='make_celery.pronoun_counter')
def pronoun_counter():
    #analyzes a folder of files containing txt files containing multiple tweet json objects
    #returns pronoun statistics for the all files including number of tweets analyzed
    
    all_files = os.listdir('data')#list all files containing tweets

    statistics = {'han': 0,
                  'hon': 0,
                  'den': 0,
                  'det': 0,
                  'denna': 0,
                  'denne': 0,
                  'hen': 0,
                  'total': 0}

    #iterate thru files
    for file in all_files:
        print(file)
        #disregard 'secret file' .DS_Store from my computer
        if not file == '.DS_Store':
            #analyze file and save file statistics
            file_stat = file_scan('data/' + file)
            
            #add file statistics to overall statistics
            for key in statistics:
                    statistics[key] += file_stat[key]
                
    #result_file = open('result.json', 'w')
    #json.dump(statistics, result_file)
    #result_file.close()
    #return json.dumps(statistics)
    return statistics

def tweet_scan(tweet):
    #takes one tweet as a string and counts occurence of each pronoun
    count = dict()
    pronoun = ['han', 'hon', 'den', 'det', 'denna', 'denne', 'hen']
    
    t = tweet.split(' ')
    #counting pronouns in tweet
    for p in pronoun:
        count[p] = t.count(p)

    return count


def file_scan(filename):
    #takes a txt file containing json tweet objects and counts occurence of pronouns
    #returns pronoun statistics for the file and number of tewwts analyzed
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
                
                #disregards retweets
                if not tweet_obj['retweeted']:
                    #count for pronouns in each tweet
                    pro_in_tweet = tweet_scan(tweet_obj['text'])
                    #count total number of tweets
                    file_statistics['total'] += 1
                    #add current tweet count to statistics
                    for key in pro_in_tweet:
                        file_statistics[key] += pro_in_tweet[key]
                            
    return file_statistics
  
def create_figure(key, vals):
    fig, ax = plt.subplots(figsize = (7,5))
    fig.patch.set_facecolor('#E8E5DA')

    ax.bar(key, vals, color = "#304C89")

    plt.xticks(rotation = 0, size = 13)
    plt.ylabel("Occurence", size = 15)

    return fig

if __name__ == '__main__':
    flask_app.run(host='0.0.0.0',debug=True)
