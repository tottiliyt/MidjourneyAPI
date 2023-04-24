import json
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/imagine', methods=['POST'])
def imagine():

    #Webhook of my channel. Click on edit channel --> Webhooks --> Creates webhook
    mUrl = "https://discord.com/api/webhooks/1099816041737101462/uI6e4cB4Gvfo4Qye4zZTcVX76eXuRaduREqC2jXPqLjrpaVKXmNW12GX-JJgFTG4JOAY"

    data = {"content": 'request'}
    response = requests.post(mUrl, json=data)

    print(response.status_code)

    print(response.content)
    # To obtain your token, https://discordpy-self.readthedocs.io/en/latest/token.html
    return jsonify({'test': 'ok'})

# TODO
# improve imagine endpoint, add parameters 
# add reaction endpoint for u1, u2 ... v1, v2
# put all constants like IDs to config.yaml
# collect the picture generate and 1. store to database 2. pass to a webhook
# add protection to api requests so it will work run for authorized call
# add documentation, prefer Sphinx(auto-gen)
# 




app.run(debug=True)
