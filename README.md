# Introduction

This template is built for services that provide a webhook for LINE bot integration.

# Getting Started

   Simply use `pip3 install -r requirements.txt`


# Need a webhook for local testing?

Ngrok is your friend

1.  Sign-up for Ngrok for yourself: https://dashboard.ngrok.com/
2.  Go to 'Your Authtoken` tab in Ngrok dashboard and copy it
3.  Install it in your environment: `brew install ngrok/ngrok/ngrok`
4.  Run command: `ngrok config add-authtoken {your_auth_token}`
5.  You'll see 'Authtoekn saved to configuration file: ...' which means you are set!
6.  Then set your localhost port to ngrok's https domain like `ngrok http 127.0.0.1:8216` (depends on your local settings)
7.  Update webhook url in LINE Developers Console: https://developers.line.biz/console/channel/1657898222/messaging-api
    - for example: `https://ae76-220-130-33-111.ngrok-free.app/line-chatbot-service/callback`
8.  response = requests.post('https://ae76-220-130-33-111.ngrok-free.app/line-chatbot-service/callback', verify=False)

# API Reference

1. Local
   - when running your application locally, go to `localhost:5000/docs` for OpenAPI documentation
   - or `http://127.0.0.1:5000/docs` depends on your settings
