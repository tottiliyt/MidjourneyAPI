import json
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/imagine', methods=['POST'])
def imagine():
    """Send slash command /imagine to Midjourney Bot.

    Example request body
    {
        "cmd": "imagine",
        "msg": "<your-prompt-here>"
        "webhook": "<response-webhook-here>"
    }
    """
    #Webhook of my channel. Click on edit channel --> Webhooks --> Creates webhook
    mUrl = "https://discord.com/api/webhooks/1099816041737101462/uI6e4cB4Gvfo4Qye4zZTcVX76eXuRaduREqC2jXPqLjrpaVKXmNW12GX-JJgFTG4JOAY"

    request_body = request.json

    metadata = json.dumps(request_body)
    response = requests.post(mUrl, json={"content": metadata})

    return {}, 200

# TODO
# improve imagine endpoint, add parameters 
# add reaction endpoint for u1, u2 ... v1, v2
# put all constants like IDs to config.yaml
# collect the picture generate and 1. store to database 2. pass to a webhook
# add protection to api requests so it will work run for authorized call
# add documentation, prefer Sphinx(auto-gen)
# ...

# Helpful Link
# https://www.thenextleg.io/docs/getting-started
# https://pythonbasics.org/flask-rest-api/
# https://github.com/Merubokkusu/Discord-S.C.U.M/tree/master/docs
# https://discordpy-self.readthedocs.io/en/latest/index.html (not using now, but might helpful)
#

app.run(debug=True)
