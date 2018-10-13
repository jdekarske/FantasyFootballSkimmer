from yahoo_oauth import OAuth2 #https://github.com/josuebrunel/yahoo-oauth
import urllib.request

#load token
oauth = OAuth2(None, None, from_file='keys.json')

#refresh token
if not oauth.token_is_valid():
    oauth.refresh_access_token()

# url must be https
#url = 'https://fantasysports.yahooapis.com/fantasy/v2/league/380.l.1083258/teams' # to find your team key >380.l.1083258.t.8

def cleanplayers(players): # returns dictionary of {'playername': {'position': position}
    result = {}
    for key,value in players.items():
        playerdata = {}
        try:
            for i in value['player'][0]:
                playerdata.update(i)
        except:
            continue
        x = {}
        pos = {}
        pos['position'] = playerdata['display_position']
        x[playerdata['name']['full']] = pos  # I only need name and position
        result.update(x)
    return result

def getavailableplayers(leaguekey,n=200): # returns dictionary of top n {'playername': 'position'}
    availableplayers = {}
    start = 0
    while start < n: #api can only get 25 players at a time
        url = 'https://fantasysports.yahooapis.com/fantasy/v2/league/' + leaguekey + '/players;sort=AR;sort_type=season;status=A;start=' + str(start)
            
        response = oauth.session.get(url, params={'format': 'json'}).json()
        
        players = response['fantasy_content']['league'][1]['players']
        
        availableplayers.update(cleanplayers(players))
        
        start += 25
    return availableplayers

def getmyteam(leaguekey,teamid):
    myplayers = {}
    url = 'https://fantasysports.yahooapis.com/fantasy/v2/team/' + leaguekey + '.t.' + teamid + '/roster'
    response = oauth.session.get(url, params={'format': 'json'}).json()
    myrosterdata = response['fantasy_content']['team'][1]['roster']['0']['players']
    myplayers.update(cleanplayers(myrosterdata))
    return myplayers

####################boris chen####################################

def getTiers():
    Pages = ['https://s3-us-west-1.amazonaws.com/fftiers/out/text_QB.txt',
            'https://s3-us-west-1.amazonaws.com/fftiers/out/text_WR.txt',
            'https://s3-us-west-1.amazonaws.com/fftiers/out/text_RB.txt',
            'https://s3-us-west-1.amazonaws.com/fftiers/out/text_TE.txt',
            'https://s3-us-west-1.amazonaws.com/fftiers/out/text_K.txt',
            'https://s3-us-west-1.amazonaws.com/fftiers/out/text_DST.txt'] #,
            #'https://s3-us-west-1.amazonaws.com/fftiers/out/text_Flex.txt']

    positions = ['QB','WR','RB','TE','K','DST'] #,'Flex']
    allplayers = {}

    for pos, page in enumerate(Pages):
        req = urllib.request.Request(page)
        with urllib.request.urlopen(req) as response:
            the_page = response.read()
        the_page = the_page.decode('utf-8')
        Tierstrings = the_page.split('\n')
        del Tierstrings[-1]
        players = {}
        p = {}
        for i,name in enumerate(Tierstrings):
            Tierstrings[i] = Tierstrings[i].split(': ')
            Tierstrings[i] = Tierstrings[i][1].split(', ')
            for person in Tierstrings[i]:
                tier = {}
                tier['tier'] = i + 1
                tier['position'] = positions[pos]
                p[person] = tier
                
                players.update(p)
        allplayers.update(players)
    return allplayers

#######################################################

leaguekey = '380.l.1083258'
teamid = '8'

myteam = getmyteam(leaguekey,teamid)
availableplayers = getavailableplayers(leaguekey,500)
tiers = getTiers()

#check if available players are on the tiers
availabletier = {}
for item in tiers.keys():
    if item in availableplayers:
        newitem = {item: tiers[item]}
        availabletier.update(newitem)

#assign my players tiers
myteamtier = {}
for item in tiers.keys():
    if item in myteam:
        newitem = {item: tiers[item]}
        myteamtier.update(newitem)

#see if available players are better than mine
print('Boris thinks you should pickup:')
betterplayers = {}
for item in myteamtier.keys():
    for newitem in availabletier.keys():
        if availabletier[newitem]['tier'] < myteamtier[item]['tier'] and availableplayers[newitem]['position'] == myteamtier[item]['position']:
            print(newitem + ' for ' + item)

#my roster according to boris
print('Boris thinks you should start:')

QB = {}
RB = {}
WR = {}
TE = {}
K = {}
DST = {}
FLEX = {}
for value in myteamtier: #this is gross
    if myteamtier[value]['position'] == "QB":
        QB.update({value: myteamtier[value]})
    if myteamtier[value]['position'] == "RB":
        RB.update({value: myteamtier[value]}) 
    if myteamtier[value]['position'] == "WR":
        WR.update({value: myteamtier[value]}) 
    if myteamtier[value]['position'] == "TE":
        TE.update({value: myteamtier[value]}) 
    if myteamtier[value]['position'] == "K":
        K.update({value: myteamtier[value]}) 
    if myteamtier[value]['position'] == "DST":
        DST.update({value: myteamtier[value]}) 
    if myteamtier[value]['position'] == "FLEX":
        FLEX.update({value: myteamtier[value]})  

# sort the players
QB = sorted(QB.items(), key = lambda tup: (tup[1]["tier"]))
RB = sorted(RB.items(), key = lambda tup: (tup[1]["tier"]))
WR = sorted(WR.items(), key = lambda tup: (tup[1]["tier"]))
TE = sorted(TE.items(), key = lambda tup: (tup[1]["tier"]))
K  = sorted( K.items(), key = lambda tup: (tup[1]["tier"]))

# pick the team
print(QB[0][0])
print(WR[0][0])
print(WR[1][0])
print(RB[0][0])
print(RB[1][0])
print(TE[0][0])
print(K[0][0])


#todo flex, bye week, and trim defense