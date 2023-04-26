from auth import *
import requests
import tweepy
import pandas as pd
import numpy as np
from datetime import *

from fastapi import FastAPI , Depends
# from pydantic import BaseModel, validator


# from database import Base, engine, SessionLocal
# from sqlalchemy.orm import Session 

from fastapi import FastAPI, Query
import json

app = FastAPI()

def main(query, max_results, day_num):
    client = tweepy.Client(bearer_token=BEARER_TOKEN, 
                        consumer_key=consumer_key, 
                        consumer_secret=consumer_secret, 
                        access_token=access_token, 
                        access_token_secret=access_token_secret, 
                        return_type = requests.Response,
                        wait_on_rate_limit=True)
    end_time = datetime.utcnow() - timedelta(days=day_num)
    end_time = end_time.strftime('%Y-%m-%dT%H:%M:%SZ')
    # get max. 100 tweets
    tweets = client.search_recent_tweets(query=query, 
                                        tweet_fields=['author_id', 'created_at','in_reply_to_user_id','lang','source'],
                                        # place_fields=['country'],
                                        # expansions=['geo.place_id'],
                                        end_time=end_time,
                                        max_results=max_results)


    # Save data as dictionary
    tweets_dict = tweets.json() 

    # Extract "data" value from dictionary
    tweets_data = tweets_dict['data'] 
    df = pd.json_normalize(tweets_data) 
    df.to_csv('./data/twitter_{0}_{1}.csv'.format(query,datetime.now().strftime('%Y_%m_%d_%H_%M')), index=False, encoding='utf-8-sig')
    return tweets_data

@app.get("/search")
async def search(query: str, max_results: int = 100, day_num: int = 1):
    return main(query, max_results, day_num)

