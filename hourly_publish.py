#!/usr/bin/python

import gzip
import StringIO
import time
import traceback
import json
import requests
import tweepy
import os
import tinyurl
from urlparse import urlparse
from urllib2 import urlopen
from collections import defaultdict
from datetime import datetime, timedelta

current_time = datetime.now()
time_difference = timedelta(hours=4)
gh_archive_time = current_time - time_difference
fmt = '%Y-%m-%d'
real_time = datetime.strftime(gh_archive_time, fmt)
real_time += '-' + str(gh_archive_time.hour)

half_a_month = timedelta(days=30)
half_a_month_ago = current_time - half_a_month
new_repo_begin_time = datetime.strftime(half_a_month_ago, fmt)

# Form the right url
file_url = 'http://data.githubarchive.org/' + real_time + ".json.gz"

while(True):
    try:
        # f = urlopen(file_url)
        f = urlopen(file_url)
        break
    except:
        traceback.print_exc()
        time.sleep(60)

compressed_data = f.read()
compressed_stream = StringIO.StringIO(compressed_data)


# Decompress the gzipped json file and load it into a list
data = []
with gzip.GzipFile(fileobj=compressed_stream) as f:
    for line in f:
        if not line.get('repository'):
            continue
        if line['repository']['created_at'] < new_repo_begin_time:
            data.append(json.loads(line))

