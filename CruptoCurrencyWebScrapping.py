import os
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json

url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest' 
#Original Sandbox Environment: 'https://sandbox-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
parameters = {
  'start':'1',
  'limit':'15',
  'convert':'USD'
}
headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': '0ad53085-1cb2-4eb8-ad9e-3ffbd7e56509',
}

session = Session()
session.headers.update(headers)

try:
  response = session.get(url, params=parameters)
  data = json.loads(response.text)
  #print(data)
except (ConnectionError, Timeout, TooManyRedirects) as e:
  print(e)

type(data)

import pandas as pd
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

df = pd.json_normalize(data['data'])
df['timestamp'] = pd.to_datetime('now', utc=True)
df


def api_runner():
    global df
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest' 
    #Original Sandbox Environment: 'https://sandbox-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    parameters = {
      'start':'1',
      'limit':'15',
      'convert':'USD'
    }
    headers = {
      'Accepts': 'application/json',
      'X-CMC_PRO_API_KEY': '0ad53085-1cb2-4eb8-ad9e-3ffbd7e56509',
    }

    session = Session()
    session.headers.update(headers)
    
    try:
      response = session.get(url, params=parameters)
      data = json.loads(response.text)
      #print(data)
    except (ConnectionError, Timeout, TooManyRedirects) as e:
      print(e)
    
    df2 = pd.json_normalize(data['data'])
    df2['timestamp'] = pd.to_datetime('now', utc=True)
    df = pd.concat([df, df2], ignore_index=True)
    
    if not os.path.isfile("api.csv"):
        df.to_csv("api.csv", header="column_names")
    else:
        df.to_csv('api.csv', mode='a', header=False )

import os 
from time import time
from time import sleep

for i in range(333):
    api_runner()
    print('API Runner completed sucessfully!!')
    sleep(60)
exit()

df.shape

pd.set_option('display.float_format', lambda x: '%.5f' % x)

df3 = df.groupby('name', sort=False)[['quote.USD.percent_change_1h','quote.USD.percent_change_24h','quote.USD.percent_change_7d','quote.USD.percent_change_30d','quote.USD.percent_change_60d','quote.USD.percent_change_90d']].mean()
df3

df4 = df3.stack().to_frame(name='values').reset_index().rename(columns={'level_1': 'percent_change'})
df4['percent_change'] = df4['percent_change'].replace(['quote.USD.percent_change_1h','quote.USD.percent_change_24h','quote.USD.percent_change_7d','quote.USD.percent_change_30d','quote.USD.percent_change_60d','quote.USD.percent_change_90d'],['1h','24h','7d','30d','60d','90d'])
df4

import seaborn as sns
import matplotlib.pyplot as plt


sns.catplot(x='percent_change', y='values', hue='name', data=df4, kind='point')

df5 = df[['name','quote.USD.price','timestamp']]
df5 = df5.query("name == 'Bitcoin'")
df5

# list of coins to plot
coins = ['Bitcoin', 'Ethereum', 'Tether', 'BNB', 'USD Coin', 'XRP', 'Cardano', 
         'Dogecoin', 'Polygon', 'Binance USD', 'Solana', 'Polkadot', 'Litecoin', 'Shiba Inu', 'TRON']

# loop over coins and plot each one
for coin in coins:
    df_coin = df.query("name == @coin")
    sns.lineplot(x='timestamp', y='quote.USD.price', data=df_coin)
    plt.title(coin)
    plt.show()


