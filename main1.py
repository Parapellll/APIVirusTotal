import json
import requests
api_url = 'https://www.virustotal.com/vtapi/v2/file/scan'
params = dict(apikey='')
with open('H:\\1405800023_17_viruses-for-ant.rar', 'rb') as file:
  files = dict(file=('H:\1405800023_17_viruses-for-ant.rar', file))
  response = requests.post(api_url, files=files, params=params)
if response.status_code == 200:
  result=response.json()
  print(json.dumps(result, sort_keys=False, indent=4))
api_url = 'https://www.virustotal.com/vtapi/v2/file/report'
params = dict(apikey='', resource='c68c2382e7108ca44e256f4e3712e821c06348cec7d052e2d2771b52b331dd15-1652556142')
response = requests.get(api_url, params=params)
if response.status_code == 200:
  result=response.json()
  print(json.dumps(result, sort_keys=False, indent=4))
