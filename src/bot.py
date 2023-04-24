# a place to write random things, need to be removed eventually

from discum.utils.slash import SlashCommander
import discum

TOKEN= 'NTUyNzI2NTQ2ODIyMDcwMjgy.YdPFng.uUxKSWpVFtSdVfVM-cUkgnogxCk'

bot = discum.Client(token=TOKEN,log=False)

def imagine(resp):
  if resp.event.message:
    m = resp.parsed.auto()
    if m['content'].startswith('request'):
        channelID = m['channel_id']
        guildID = m['guild_id']
        bot.sendMessage(channelID,"got request")
        slashCmds = bot.getSlashCommands("936929561302675456").json()
        s = SlashCommander(slashCmds)
        data = s.get(['imagine'])
        data['options'] = [{
            "type": 3,
            "name": "prompt",
            "value": "a bottle of water"
        }]
        print(data)
        bot.triggerSlashCommand("936929561302675456", channelID,guildID=guildID, data=data)
        print('Bumped!')

bot.gateway.command({"function": imagine})
bot.gateway.run(auto_reconnect=True)
