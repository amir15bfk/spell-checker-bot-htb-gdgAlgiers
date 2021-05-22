################################################################################
#                                                                              #
#                        spell chacker bot main file                           #
#                          by languistic bot team                              #
#                   for Hack The Bot hackaton gdg Algiers                      #
#                                                                              #
################################################################################


from api_connect import check
from replit import db
import os
import discord
from keep_alive import keep_alive

client = discord.Client()
TOKEN = os.environ['TOKEN']

#reset 
#db["conf"]={}
#db["workingON"]=[]
#the databasse architacture
#db={"workingON":[ liste of the channals the bot is ON in it ],
#    "conf":{"channelID":[langconf ex:"en-us",mode 1 | 2 | 3],...}
#   }
help=""":regional_indicator_s: :regional_indicator_p: :regional_indicator_e: :regional_indicator_l: :regional_indicator_l:  :small_orange_diamond:    :regional_indicator_c: :regional_indicator_h: :regional_indicator_e: :regional_indicator_c: :regional_indicator_k: :regional_indicator_e: :regional_indicator_r:
:scroll: :regional_indicator_h: :regional_indicator_e: :regional_indicator_l: :regional_indicator_p: :scroll:
To turn ON :green_circle: in a channal use
`>ON `
To turn OFF :red_circle: in a channal use
`>OFF `
To get status :mag:  in a channal use
`>status `
To use without activate :yellow_circle:  start your message by
`!`
To get conf :page_facing_up:   in a channal use
`>conf `
To change language config use 
`>langconf <the numbre of lang> `
ex:`>langconf 1 `
:one: english :flag_us: 
:two: français :flag_fr:
:three: العربية :flag_sa: (Beta)
To change mode :wrench: in channal use
:regional_indicator_r: replace :repeat: 
`>formconf R`
:b:  best suggestion :sparkles:
`>formconf B`
:a: all suggestions :scroll:
`>formconf A`"""

@client.event
async def on_rady():
  print('We have logged {0.user}'.format(client))
    
    

@client.event
async def on_message(message):
  
  cid=str(message.channel.id)
  if message.author == client.user:
    return
  #ping the bot
  if message.content.startswith('>hello'):
    #to show >help in the bottom of bot name 
    await client.change_presence(activity=discord.Game(">help"))
    await message.channel.send('Hello!')
  
  #load data base
  temp_dict = db["conf"]
  temp_list = db["workingON"]

  #put the message content in varaible
  mc=message.content

  #print the man of the bot
  if message.content.startswith('>help'):
    await message.channel.send(help)
    return
  

  #to see the confuguration
  if message.content.startswith('>conf'):
    result = f"conf :page_facing_up: in this channal is\nlang : {temp_dict[cid][0]}\nmode :"
    if temp_dict[cid][1]==1:
      result+=":regional_indicator_r: replace :repeat:"
    elif temp_dict[cid][1]==2:
      result+=":b:  best suggestion :sparkles:"
    elif temp_dict[cid][1]==3:
      result+=":a: all suggestions :scroll:"
    await message.channel.send(result)
    return
  
  #to change languege conf (this option make the api work beter)
  if message.content.startswith('>langconf'):
    
    if not (cid in temp_dict.keys()):
      temp_dict[cid]=["en-us",3]
    if mc[10]== "1":
      temp_dict[cid][0]="en-us"
      await message.channel.send("done you chose\n:one: english :flag_us:")
    elif mc[10]== "2":
      temp_dict[cid][0]="fr-ca"
      await message.channel.send("done you chose\n:two: français :flag_fr:")
    elif mc[10]== "3":
      temp_dict[cid][0]="ar"
      await message.channel.send("done you chose\n:three: العربية :flag_sa:")
    db["conf"] = temp_dict
    return
  
  #change printing form conf
  if message.content.startswith('>formconf'):
    mc=mc.split()[1].lower()
    if not (cid in temp_dict.keys()):
      temp_dict[cid]=["en-us",1]
    
    if mc in ["replace","r"]:
      temp_dict[cid][1]=1
      await message.channel.send("done :white_check_mark:  you chose replace :repeat: ")
    elif mc in [ "best","b"]:
      temp_dict[cid][1]=2
      await message.channel.send("done :white_check_mark: \nyou chose best suggestion :sparkles:")
    elif mc in [ "all","a"]:
      temp_dict[cid][1]=3
      await message.channel.send("done :white_check_mark:  you chose all suggestions :scroll:  ")
    db["conf"] = temp_dict
    return
  
  #to turn on 
  if message.content.startswith('>ON'):
    await message.channel.send(":green_circle: is ON ")
    temp_list.append(str(message.channel.id))
    temp_list=list(set(temp_list))
    db["workingON"]=temp_list
    if not (cid in temp_dict.keys()):
      temp_dict[cid]=["en-us",3]
      db["conf"] = temp_dict
    return 
  #to turn off
  if message.content.startswith('>OFF'):
    await message.channel.send(":red_circle: is OFF")
    temp_list.remove(cid)
    db["workingON"]=temp_list
    return 
  
  #to see the status on or off
  if message.content.startswith('>status'):
    if cid in temp_list:
      await message.channel.send(":green_circle: is ON")
    else:
      await message.channel.send(":red_circle: is OFF")
    return 
  
  #if it's off
  if message.content.startswith('!'):
    if (cid in temp_dict.keys()):
      result = check(message.content,temp_dict[cid])
    else :
      result = check(mc,["en-us",3])
    if result!="" or result==mc:
      await message.channel.send(result)
    else:
      await message.add_reaction( "✅")
    return

  #chacking and send the correction
  if (cid in temp_list):
    result = check(message.content,temp_dict[cid])
    if result!="":
      await message.channel.send(result)
    return




keep_alive()
client.run(TOKEN)