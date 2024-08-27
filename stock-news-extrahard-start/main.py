import requests
from twilio.rest import Client
import random

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
stock_api_key = " ['stock_key']"
stock_url = "https://www.alphavantage.co/query"
news_url = "https://newsapi.org/v2/everything?q=TSlA"
news_api_key = "['news_key']"
account_sid = '["account_id"]'
auth_token = "['twilio_token']"


news_parameters = {
    "keyword": COMPANY_NAME,
    "from": "2024-08-24",
    "to": "2024-08-24",
    "apikey": news_api_key,
}
stock_parameters = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "outputsize": "compact",
    "apikey": stock_api_key,
}

# ## STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
stock_response = requests.get(stock_url, stock_parameters)
stock_response.raise_for_status()
stock_data = stock_response.json()["Time Series (Daily)"]
yesterday = float(stock_data["2024-08-23"]["4. close"])
day_before = float(stock_data["2024-08-22"]["4. close"])
diff_in_stock_val = yesterday - day_before
percent_of_change = round((diff_in_stock_val/yesterday)*100)
up_down = None
if percent_of_change > 0:
    up_down = "🔺"
else:
    up_down = "🔻"
# # STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME. 
if abs(percent_of_change) >= 4:
    news_response = requests.get(news_url, news_parameters)
    news_response.raise_for_status()
    news_data = news_response.json()["articles"]
    three_news_list = news_data[:3]
# print(three_news_list)
# ## STEP 3: Use https://www.twilio.com

# Send a seperate message with the percentage change and each article's title and description to your phone number. 
    print_news = [f"{STOCK}: {up_down}{percent_of_change}%\nHeading: {i["title"]}\n Brief: {i["description"]}\n"
                  for i in three_news_list]
    client = Client(account_sid, auth_token)
    message = client.messages.create(
      from_='whatsapp:["twilio number"]',
      body=f'{random.choice(print_news)}',
      to='whatsapp:["your number"]'
    )

# Optional: Format the SMS message like this:
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors 
are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, 
near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent 
investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 
31st, near the height of the coronavirus market crash.

"""
