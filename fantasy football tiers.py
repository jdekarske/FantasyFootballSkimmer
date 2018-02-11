##import urllib.request
##page = urllib.request.urlopen('https://s3-us-west-1.amazonaws.com/fftiers/out/current/text_DST.txt');
import urllib.request
Team = {'QB': [['Drew Brees']],
        'WR': [['Tyreek Hill'], ['Devin Funchess'], ['Josh Gordon'], ['Lary Fitzgerald'], ['DeVante Parker']],
        'RB': [['Demarco Murray'], ['Melvin Gordon'], ['Lamar Miller'], ['Jerick McKinnon'], ['Bilal Powell'], ['Rex Burkhead']],
        'TE': [['Jared Cook'], ['Greg Olsen']],
        'K':  [['Justin Tucker']],
        'D':  [['Baltimore']]}


Pages = ['https://s3-us-west-1.amazonaws.com/fftiers/out/text_QB.txt',
         'https://s3-us-west-1.amazonaws.com/fftiers/out/text_WR.txt',
         'https://s3-us-west-1.amazonaws.com/fftiers/out/text_RB.txt',
         'https://s3-us-west-1.amazonaws.com/fftiers/out/text_TE.txt',
         'https://s3-us-west-1.amazonaws.com/fftiers/out/text_K.txt',
         'https://s3-us-west-1.amazonaws.com/fftiers/out/text_DST.txt']

flexPage = ['https://s3-us-west-1.amazonaws.com/fftiers/out/text_Flex.txt']

flexTeam = {'WR': Team['WR'],
            'RB': Team['RB']}

def checkList(name, lst):
    for i, item in enumerate(lst):
        if name in lst[i]:
            return (i+1)
        
def getTiers(page):
    req = urllib.request.Request(page)
    with urllib.request.urlopen(req) as response:
       the_page = response.read()
    the_page = the_page.decode('utf-8')
    Tierstrings = the_page.split('\n')
    print(the_page)
    del Tierstrings[-1]
    return Tierstrings

def checkPlayer(player,flex):
    if flex:
        playertier = checkList(player[0],getTiers(Pages[2]))
        if playertier != None:
            return playertier
    else:
        for i, item in enumerate(Pages):
            playertier = checkList(player[0],getTiers(Pages[i]))
            if playertier != None:
                return playertier
                 
def printTeamList(teamList):
    print(teamList.items())
    for pos, players in teamList.items():
        print('\n' + pos + '\n')
        players.sort()
        for i, item in enumerate(players):
            print(repr(str(teamList[pos][i][0][0])).rjust(2), repr(teamList[pos][i][1]).rjust(3), end=' ')
#            print('{0:2d} {1:3d}'.format(teamList[pos][i][0][0],teamList[pos][i][1]))
            print('\n')
                 
#check flex
for pos, players in flexTeam.items():
    for i, item in enumerate(players):
        playertier = checkPlayer(item,1)
        flexTeam[pos][i] = [item , playertier]
        print('checking flex: {}%'.format(int((i+1)*100/len(players))))

        
print('--------------------Roster--------------------')
printTeamList(Team)
##printTeamlist(flexTeam)
input('Enter to quit')
#TODO: add flex, print stuff in ranks
