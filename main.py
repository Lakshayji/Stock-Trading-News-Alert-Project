from dotenv import load_dotenv
import os
import requests
from twilio.rest import Client
load_dotenv()  # take environment variables from .env.

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

api_key = os.getenv("APIKEY");
API = "https://www.alphavantage.co/query"
API_NEWS = " https://newsapi.org/v2/everything"

parameter = {
    "apikey" : api_key,
    "symbol" : "TSLA",
    "function" : "TIME_SERIES_DAILY",
    "q" : COMPANY_NAME,
}
response_news = requests.get(url=API_NEWS ,params=parameter)
response_news.raise_for_status()
data_news = response_news.json()["articles"][0]["title"]
print(data_news)

list = []
response_price = requests.get(url=API, params=parameter)
response_price.raise_for_status()
data = response_price.json()["Time Series (Daily)"]
for _ in data:
    data_1 = response_price.json()["Time Series (Daily)"][_]["4. close"]
    list.append(data_1)

today_close = float(list[0])
yesterday_close = float(list[1])
diff = today_close - yesterday_close
if diff > 0:
     percentage = (diff/today_close) * 100
     print(f"something positive news happened {percentage}")
else:
    percentage = diff / today_close * 100
    print(f"something bad news happened {percentage}")





## STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").

## STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.

## STEP 3: Use https://www.twilio.com
# Send a seperate message with the percentage change and each article's title and description to your phone number.


#Optional: Format the SMS message like this:
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""

account_sid = os.getenv("ACCOUNT_SID")
auth_token = os.getenv("AUTH_TOKEN")
client = Client(account_sid, auth_token)

message = client.messages \
                .create(
                     body=f"{data_news}, {percentage}%",
                     from_='+16814914935',
                     to='+919896996570'
                 )
print(message.status)