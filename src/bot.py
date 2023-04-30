from discum.utils.slash import SlashCommander
from discum.utils.button import Buttoner
import discum
import json
import requests

# To obtain your token, https://discordpy-self.readthedocs.io/en/latest/token.html
TOKEN= 'NTUyNzI2NTQ2ODIyMDcwMjgy.YdPFng.uUxKSWpVFtSdVfVM-cUkgnogxCk'

bot = discum.Client(token=TOKEN,log=False)

WEBHOOK_BOT_ID = "1099816041737101462"
MIDJOURNEY_BOT_ID = "936929561302675456"
IMAGINE_PREFIX = "@IMAGINE"

current_job = {}

TEST_WEBHOOK_URL = "https://webhook.site/4ab0ea73-7086-434d-9797-dd47f87009b2"
LOCALHOST_WEBHOOK_URL = "http://127.0.0.1:5000/webhook"

def endpoints(resp):
  if resp.event.message or resp.event.message_updated:
    msg = resp.parsed.auto()
    # Listening to owner sent message
    if msg['author']['id'] == WEBHOOK_BOT_ID:
        content_string = msg['content']
        try:
            content_json = json.loads(content_string)
            cmd = content_json["cmd"]
        except:
            # Not able to parse request body
            return

        if cmd == "imagine":
            try:
                prompt = content_json["msg"]
                webhook_id = content_json["webhook_id"]
            except:
                # Not able to parse request body
                return
            try:
                channelID = msg['channel_id']
                guildID = msg['guild_id']
                slashCmds = bot.getSlashCommands(MIDJOURNEY_BOT_ID).json()
                slashCmd = SlashCommander(slashCmds)
                metadata = slashCmd.get(['imagine'])
            except:
                # Not able to fetch neccessary info to send the slash command
                return

            # Modify slash command metadata 
            metadata['options'] = [{
                "type": 3,
                "name": "prompt",
                "value": prompt
            }]

            bot.triggerSlashCommand(MIDJOURNEY_BOT_ID, channelID,guildID=guildID, data=metadata)

            # add to current job
            if prompt not in current_job:
                current_job[prompt] = []
            current_job[prompt].append(webhook_id)

        elif cmd == "button":
            try:
                metadata = content_json['metadata']
                button_name = content_json['button_name']
                webhook_id = content_json["user_id"]
                prompt: content_json['prompt']

            except:
                # Not able to parse request body
                return
            buts = Buttoner(metadata["components"])
            bot.click(
                MIDJOURNEY_BOT_ID,
                channelID=metadata["channel_id"],
                guildID=metadata["guild_id"],
                messageID=metadata["id"],
                messageFlags=metadata["flags"],
                data=buts.getButton(button_name),
            )
            
    # Listening to midjourney bot sent message
    elif msg['author']['id'] == MIDJOURNEY_BOT_ID:
        prompt_identifier = "**"
        content = msg['content']

        prompt = content[content.find(prompt_identifier)+len(prompt_identifier):content.rfind(prompt_identifier)]
        
        print(current_job)
        # determine which webhook to send
        webhook_id = current_job[prompt][0]

        # job wait to start
        if len(msg['attachments']) == 0:
            result_metadata = {
                "msg": msg["content"],
                "webhook_id": webhook_id
            }
            response = requests.post(LOCALHOST_WEBHOOK_URL, json=result_metadata)
        # job started or finished
        elif len(msg['attachments']) == 1:
            
            #job in progress
            if len(msg['components']) == 0:
                result_metadata = {
                    "msg": msg["content"],
                    "webhook_id": webhook_id
                }
                response = requests.post(LOCALHOST_WEBHOOK_URL, json=result_metadata)

            #job finished
            else:
                try:
                    result_metadata = {
                        'channel_id':msg["channel_id"],
                        'guild_id':msg["guild_id"],
                        'id':msg["id"],
                        'flags':msg["flags"],
                        'components':msg['components'],
                        'attachments':msg['attachments'],
                        'prompt': prompt
                    }
                
                except:
                    # Not able to parse request body
                    return
                response = requests.post(LOCALHOST_WEBHOOK_URL, json=result_metadata)

bot.gateway.command({"function": endpoints})
bot.gateway.run(auto_reconnect=True)
