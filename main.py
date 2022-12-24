import os
import requests
from twilio.http.http_client import TwilioHttpClient
from twilio.rest import Client

proxy_client = TwilioHttpClient()
proxy_client.session.proxies = {"https": os.environ["https_proxy"]}
api_key = os.environ.get("OWM_API_KEY")
OMW_Endpoint = "https://api.openweathermap.org/data/2.5/onecall"
account_sid = ""
auth_token = os.environ.get("AUTH_TOKEN")  # Need to export token via terminal. Twilio suspended the account

params = {
    "lat": 55.755825,
    "lon": 37.617298,
    "exclude": "current,minutely,daily",
    "appid": api_key,
}

response = requests.get(OMW_Endpoint, params=params)
response.raise_for_status()
data = response.json()

take_umbrella = False

weather_slice = data["hourly"][:12]

for hour in weather_slice:
    condition_id = int(hour["weather"][0]["id"])
    if condition_id < 700:
        take_umbrella = True

if take_umbrella:
    client = Client(account_sid, auth_token, http_client=proxy_client)
    message = client.messages \
                    .create(
                        body="It is going to rain today. Bring an umbrella ☔︎",
                        from_= "",
                        to="+79878073472"
                            )
    print(message.status)

# Upload this to pythonanywhere to run this code every morning on schedule



