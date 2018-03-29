'''
Created on Dec 23, 2017

@author: jean-francis
'''

import tweepy 
import re
import time
import math
from poloniex import Poloniex


class Keys:
    API_KEY=''
    SECRET_KEY=''

CONSUMER_KEY=""
CONSUMER_SECRET=""

ACCESS_TOKEN=""
ACCESS_TOKEN_SECRET=""

PAIRS=['BTC_XRP','BTC_BCH','BTC_DGB','BTC_NXT','BTC_ETH','BTC_SC','BTC_LTC','BTC_STR',
       'BTC_STRAT','BTC_XMR','BTC_DOGE','BTC_BURST','BTC_DASH','BTC_XEM','BTC_ARDR',
       'BTC_BTS','BTC_ETC','BTC_LSK','BTC_ZEC','BTC_REP','BTC_BCN','BTC_EMC2','BTC_OMG',
       'BTC_GNT','BTC_STEEM','BTC_ZRX','BTC_VTC','BTC_MAID','BTC_EXP','BTC_CVC','BTC_FCT',
       'BTC_SYS','BTC_BELA','BTC_DCR','BTC_BLK','BTC_FLDC','BTC_GAME','BTC_LBC','BTC_AMP',
       'BTC_NAV','BTC_BTCD','BTC_CLAM','BTC_POT','BTC_PINK','BTC_FLO','BTC_NXC','BTC_STORJ',
       'BTC_GAS','BTC_HUC','BTC_VIA','BTC_PASC','BTC_GNO','BTC_VRC','BTC_GRC','BTC_SBD','BTC_BCY',
       'BTC_OMNI','BTC_NEOS','BTC_XCP','BTC_PPC','BTC_RIC','BTC_XBC','BTC_RADS','BTC_XPM','BTC_NMC','BTC_XVC','BTC_BTM']

def search_ticker(last_tweet):
    
    for word in last_tweet:
        try:
            if word.isupper():
                return word
        except:
            return None
        
    return None #no ticker found

if __name__ == '__main__':
    
    
    exchange=Poloniex(Keys.API_KEY,Keys.SECRET_KEY)
    
    begin=['Coin','of','the','day']
    next_trade_pair=None

    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    
    api = tweepy.API(auth)
    
    
    go=True
    
    while go==True:
    
        time.sleep(2)
        
        timeline=api.user_timeline(screen_name='officialmcafee',count=1)
    
        
        last_tweet=timeline[0].text
        last_tweet=re.sub(r'[^a-zA-Z ]', '', last_tweet).split() #delete non alphabetical characters
        
        if(last_tweet[:4]==begin):
            ticker=search_ticker(last_tweet)
            if ticker != None:
                print("McAfee's coin of the day is: " + str(ticker))
                for pair in PAIRS:
                    if ticker in pair:
                        next_trade_pair=pair
                if next_trade_pair==None: print("Not on poloniex :(") 
            else: print("No coin of the day found in COD tweet.")
        else: print("Not a coin of the day tweet.")    
    
        if next_trade_pair != None:
            go=False
        
    
    #Buy coin of the day
    
    balance = float(exchange.returnBalances()['BTC'])
    time.sleep(0.5)
    rate = float(exchange.returnTicker()[next_trade_pair]['lowestAsk'])*1.01
    amount=(math.floor((balance*0.995/rate)*1000000)/1000000)
    
    exchange.buy(next_trade_pair, rate, amount)
    
    print("Just bought!")
    print(next_trade_pair)
    
    
    