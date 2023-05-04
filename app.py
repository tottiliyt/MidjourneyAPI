import json
from flask import Flask, request, jsonify
from flask_jwt_extended import (JWTManager,
    jwt_required, create_access_token,
    create_refresh_token, get_jwt_identity, set_access_cookies,
    set_refresh_cookies)
import requests
import uuid
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from pymongo import MongoClient
from bson import json_util


app = Flask(__name__)

# disabled for testing purpose
app.config['JWT_COOKIE_CSRF_PROTECT'] = False
app.config['JWT_SECRET_KEY'] = 'hentai'

limiter = Limiter(get_remote_address, app=app)
jwt = JWTManager(app)

#Webhook of my channel. Click on edit channel --> Webhooks --> Creates webhook
WEBHOOK_BOT_URL = "https://discord.com/api/webhooks/1099816041737101462/uI6e4cB4Gvfo4Qye4zZTcVX76eXuRaduREqC2jXPqLjrpaVKXmNW12GX-JJgFTG4JOAY"

def get_database():
 
    # Provide the mongodb atlas url to connect python to mongodb using pymongo
    CONNECTION_STRING = "mongodb+srv://alan:CVqTP2WEkqnwGmr8@ai-painting.c5uwx70.mongodb.net/test"
    # create the database and collection to start with
    client = MongoClient(CONNECTION_STRING)
    db_client = client['ai_painting']
    db_job = db_client['job']
    # db_job.create_index("prompt")

    return db_job

db_job = get_database()

@app.route('/auth', methods=['POST'])
def auth():
    user_id = str(uuid.uuid4())
    access_token = create_access_token(identity=user_id)
    refresh_token = create_refresh_token(identity=user_id)

    resp = jsonify({
        'auth': True,
        'access_cookies': access_token,
        'refresh_cookies': refresh_token
    })
    set_access_cookies(resp, access_token)
    set_refresh_cookies(resp, refresh_token)

    return resp, 200

# Same thing as login here, except we are only setting a new cookie
# for the access token.
@app.route('/auth/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    # Create the new access token
    current_user = get_jwt_identity()
    access_token = create_access_token(identity=current_user)

    # Set the JWT access cookie in the response
    resp = jsonify({'access_token': access_token})
    set_access_cookies(resp, access_token)

    return resp, 200

@app.route('/imagine', methods=['POST'])
@jwt_required()
@limiter.limit("100/day;50/hour;5/minute")
def imagine():
    """Send slash command /imagine to Midjourney Bot.

    Example request body
    {
        "user_id": "<your user_id>"
        "cmd": "imagine",
        "msg": "<your-prompt-here>"
    }
    """
    
    request_body = request.json

    request_body["user_id"] = get_jwt_identity()

    metadata = json.dumps(request_body)
    response = requests.post(WEBHOOK_BOT_URL, json={"content": metadata})

    return {}, 200

@app.route('/button', methods=['POST'])
@jwt_required()
@limiter.limit("100/day;50/hour;5/minute")
def button():
    """Send button command to Midjourney Bot

    Example request body
    {
        "cmd": "button",
        "button_name": "<your button_name here>",
        "metadata": <imagine response metadata>, 
        "user_id": "<your user_id>"
    }
    """

    request_body = request.json

    metadata = json.dumps(request_body)
    response = requests.post(WEBHOOK_BOT_URL, json={"content": metadata})

    return {}, 200

@app.route('/result', methods=['GET'])
@jwt_required()
@limiter.limit("20/minute")
def result():
    request_body = request.json
    
    prompt = request_body['prompt']
    user_id = get_jwt_identity()
    print(user_id)
    #dynamo get by prompt

    cursor = db_job.find({"prompt": prompt, "user_id":user_id}, {'_id': False})
        
    return {"results": list(cursor)}, 200



# TODO

# put all constants like IDs to config.yaml
# add documentation, prefer Sphinx(auto-gen)
# ...

# Helpful Link
# https://www.thenextleg.io/docs/getting-started
# https://pythonbasics.org/flask-rest-api/
# https://github.com/Merubokkusu/Discord-S.C.U.M/tree/master/docs
# https://discordpy-self.readthedocs.io/en/latest/index.html (not using now, but might helpful)
#

app.run(host='0.0.0.0', port=8080)
