################################################################################
#                                                                              #
#                             api connect file                                 #
#                   If we need to change the API to a better                   #
#                        one we modify this file only                          #
#                                                                              #
################################################################################




import os
import requests
import json

#api conf
api_key = os.environ['api_key']
endpoint = "https://api.bing.microsoft.com/v7.0/SpellCheck"
headers = {
      'Content-Type': 'application/x-www-form-urlencoded',
     'Ocp-Apim-Subscription-Key': api_key,
      }


#check : the main function of the file
def check(text,conf):
  dict = ask_API(text,conf[0])
  return format_result(dict,text,conf)
  
#api call
def ask_API(text,setLang):
  params = {
    'mode':'proof',
    'setLang':setLang}
    
  data = {'text': text}
  
  response = requests.post(endpoint, headers=headers, params=params, data=data)
  json_response = response.json()
  string = json.dumps(json_response)
  return json.loads(string)


#formation the result
def format_result(dict,text,conf):
  result=""
  if conf[1]==1:#mode 1
    for x in dict["flaggedTokens"]:
      text=text.replace(x['token'],x['suggestions'][0]['suggestion'])
    return text
  else :
    for x in dict["flaggedTokens"]:
      if conf[1]==3:#mode 3
        result+= x['token']+" = > "
        for suggestion in x['suggestions']:
          result+=suggestion['suggestion']+" | "
      else:#mode2
       result+= x['token']+" = > "+x['suggestions'][0]['suggestion']
      result+="\n"
    return result