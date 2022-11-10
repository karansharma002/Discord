import requests
import json

TOKEN = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6ImExNDFkY2QzLTMzYmYtNGMxNi1hMzY1LTJlOGI4NmE1NmY4ZSIsImlhdCI6MTYyMTMzNDgxOCwic3ViIjoiZGV2ZWxvcGVyL2JlMDE1ZjMxLWZiYWYtZTk3My01MjQ3LTU0ZTRlNTEwZDYxYiIsInNjb3BlcyI6WyJyb3lhbGUiXSwibGltaXRzIjpbeyJ0aWVyIjoiZGV2ZWxvcGVyL3NpbHZlciIsInR5cGUiOiJ0aHJvdHRsaW5nIn0seyJjaWRycyI6WyIxMDMuNDEuMjUuMjUzIl0sInR5cGUiOiJjbGllbnQifV19.L8MPAKvAD8cCIW4nFBtazJtTfsq__e5IDdgaO3fQ6Xoi9_8BrRga6r94s88lDRuTWl8m9NkOnMy-tJE-oVNEcA'

headers = {'Authorization':"Bearer %s" %TOKEN}

#! CLARN WAR FUNCTIONS
#? NOT WORKING RIGHT NOW TEMP OFF
'''
params = {'name':'SOFIA'}
r = requests.get('https://api.clashroyale.com/v1/clans',headers = headers,params = params)
content = json.loads(r.content)
print(content)
'''

#! FINISH BOT FUNCTIONS

'''
clanTag = 'QGLC9GGR'
params = {'clantag':'QGLC9GGR','limit':5}
r = requests.get(f'https://api.clashroyale.com/v1/clans/%23{clanTag}/members',headers = headers,params = params)
print(r.status_code)
content = json.loads(r.content)
for x in range(len(content['items'])):
    user = content['items'][x]
    name = user['name']
    tag = user['tag']
    trophies = user['trophies']
    rank = user['clanRank']
    print(name,tag,trophies,rank)
    #- Ingame name
    #- Player Tag
    #- Trophy’s
    #- Rank in clan  
'''


#! TOURNAMENT BOT FUNCTIONS

clanTag = '29P9UGYU'
params = {'clantag':'29P9UGYU'}
r = requests.get(f'https://api.clashroyale.com/v1/tournaments/%23{clanTag}',headers = headers,params = params)
content = json.loads(r.content)
for x in range(len(content['membersList'])):
    user = content['membersList'][x]
    tag = user['tag']
    name = user['name']
    score = user['score']
    rank = user['rank']
    print(tag,name,score,rank)
    if x == 2:
        break


#! DISTRIBUTION OF THE POINTS

