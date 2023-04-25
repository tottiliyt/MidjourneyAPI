# a place to write random things, need to be removed eventually

from discum.utils.slash import SlashCommander
import discum
import json

# To obtain your token, https://discordpy-self.readthedocs.io/en/latest/token.html
TOKEN= 'NTUyNzI2NTQ2ODIyMDcwMjgy.YdPFng.uUxKSWpVFtSdVfVM-cUkgnogxCk'

bot = discum.Client(token=TOKEN,log=False)

WEBHOOK_BOT_ID = "1099816041737101462"
MIDJOURNEY_BOT_ID = "936929561302675456"
IMAGINE_PREFIX = "@IMAGINE"

def imagine(resp):
  if resp.event.message:
    msg = resp.parsed.auto()

    # check owner send message
    if msg['author']['id'] == WEBHOOK_BOT_ID:
        content_string = msg['content']

        try:
            content_json = json.loads(content_string)
            cmd = content_json["cmd"]
            prompt = content_json["msg"]
            webhook = content_json["webhook"]
        except:
            # not able to parse request body
            return

        if cmd == "imagine":
            channelID = msg['channel_id']
            guildID = msg['guild_id']

            bot.sendMessage(channelID,f"got request: /imagine {prompt}")
            slashCmds = bot.getSlashCommands(MIDJOURNEY_BOT_ID).json()
            slashCmd = SlashCommander(slashCmds)
            metadata = slashCmd.get(['imagine'])

            # modify slash command metadata 
            metadata['options'] = [{
                "type": 3,
                "name": "prompt",
                "value": prompt
            }]
            bot.triggerSlashCommand(MIDJOURNEY_BOT_ID, channelID,guildID=guildID, data=metadata)

bot.gateway.command({"function": imagine})
bot.gateway.run(auto_reconnect=True)
