#!/usr/local/bin/python3
import requests
url = 'https://notify-api.line.me/api/notify'
token = 'aaaa'
# token = 'zF6vCpjCLYunEQfBYksHZMr8kiw0Dr6l4fWG3sAIZhu'
headers = {'content-type':'application/x-www-form-urlencoded','Authorization':'Bearer '+token}

msg = 'Hello LINE Notify\ntest\ntest'
# msg = input()
r = requests.post(url, headers=headers, data = {'message':msg})
print (r.text)
