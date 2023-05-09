from auth import *
import requests
import os
import tweepy
import pandas as pd
import numpy as np
from datetime import *
from glob import glob
import streamlit as st
from streamlit_option_menu import option_menu

################################################################
path = "./data"
keyWordList = [folder for folder in os.listdir(path) if os.path.isdir(os.path.join(path, folder))]

################################################################


def twitterAPI(query, max_results, day_num):
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
    # print(df)
    # if df.bool():
    if not os.path.exists(f"./data/{query}"):
        os.mkdir(f"./data/{query}")
    df.to_csv('./data/{0}/twitter_{0}_{1}.csv'.format(query,datetime.now().strftime('%Y_%m_%d_%H_%M')), index=False, encoding='utf-8-sig')
    return tweets_data

with st.sidebar:
    name = option_menu("Twitter API", ["New Keyword", "Old Keyword"],
                       menu_icon="app-indicator")

st.sidebar.header("키워드로 찾아보세요.")

if name == "New Keyword":
    st.title("TEST")
    st.write("### 키워드로 찾아보세요.")
    query = st.text_input("query", value="")
    max_results = st.text_input("max_results", value="100")
    day_num = st.text_input("day_num", value="0")
    st.text(keyWordList)
    if query in keyWordList:
        path_csv = f'./data/{query}/*.csv'
        csv_list = glob(path_csv)
        all_df = pd.DataFrame()
        for csv in csv_list:
            tmp_df = pd.read_csv(csv)
            all_df = pd.concat([all_df, tmp_df])
    if st.button("Confirm"):
        df = twitterAPI(query, int(max_results), int(day_num))
        st.dataframe(df, use_container_width=True)
        all_df = pd.concat([all_df, df])
        all_df.drop_duplicates(subset=['id', 'text', 'created_at'], keep='first')
        st.dataframe(all_df, use_container_width=True)

elif name == "Old Keyword":

    
    st.title("Dataframe list")
    keywordsList = os.listdir('./data')
    selected_option = st.radio('Select an option', keywordsList)
    if selected_option:
        st.write(f"You selected {selected_option}")
        df = pd.read_csv(selected_option)
        st.dataframe(df, use_container_width=True)