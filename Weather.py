import urllib.request
import json
import re
req = urllib.request.Request(
    'http://www.fantasyfootballnerd.com/service/weather/json/tcmdyhj8qti7/',
    data=None,
    headers={
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
    }  #The weeks weather forecast from http://www.fantasyfootballnerd.com/fantasy-football-api
)       #UPDATE EACH WEEK


#Use Beautiful Soup to parse html from input url (from fantasydata.com).Use find_all method to collect all ‘div’ tags with the class ‘statsGridWrapper top border’ and store this as the player_rows list
#Filter player_rows to isolate the matchup difficulty number by using regular expressions and beautiful soup methods
#Append this number to the team_list
#Use regular expressions to isolate player name and append to player_list
#Zip together player_list and the team_list to form team_dict
def team_getter(url):
    stuff = urllib.request.urlopen(url).read().decode('utf-8')
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(stuff, "html.parser")
    player_rows = soup.find_all('div', attrs={'class': 'statsGridWrapper top-border'})
    player_list = []
    team_list = []
    for row in player_rows:
        for rank in row.find_all('table', attrs={'class': "table"}):
            for matchup in rank.find_all('tr'):
                guy = matchup.find_all('a')[0]
                scoop = guy.string
                if scoop != 'Player':
                    player_list.append(scoop)
                PPG = matchup.find_all('td', attrs={'class': "center"})
                if PPG != []:
                    AVG = (str(PPG))
                    p = AVG.split(',')[2]
                    points = re.findall('[A-Z]{2,3}',p)
                    team_list.append(points[0])

    team_dict={}
    for p, v in zip(player_list, team_list):
        if v not in team_dict.values():
            team_dict[p]=v
    return team_dict


#***Use JSON loads to decode the incoming JSON (from Fantasy Football Nerd API)***
#Initialize a dictionary called dict
#Iterate through for each Game in the JSON output
#Set variables of opponent, forecast,low,dome, and wind to equal their corresponding value in the JSON output.
#Use dict[opponenet] to store the away team as a key that takes on the same values as the home team.
#Pass on dict which pairs keys of each NFL team to the weather values of their specific stadium based on the variables mentioned above
weather=urllib.request.urlopen(req).read().decode('utf-8')
new = json.loads(weather) #json.loads() decodes incoming json #Line below is form Salary tab on Fantasy Football Data. UPDATE EACH WEEK
skeet= team_getter('https://fantasydata.com/nfl-stats/daily-fantasy-football-salary-and-projection-tool.aspx?fs=1&stype=0&sn=0&scope=0&w=13&ew=13&s=&t=0&p=2&st=FantasyPointsDraftKings&d=1&ls=&live=false&pid=false&minsnaps=4')
games = new["Games"]
dict={}
for game in games:
    opponent= games[game]['awayTeam']
    forecast =games[game]['forecast']
    low =games[game]['low']
    wind = games[game]['windSpeed']
    dome = games[game]['isDome']
    dict[game]= {"forecast": forecast, "low": low, "wind": wind, "dome": dome}
    dict[opponent] = {"forecast": forecast, "low": low, "wind": wind, "dome": dome}

#Iterate through each of the keys of dict (Weather dictionary)
#Create key:value pairs in scores_dict based on the value for the key in dict. The value is a numerical score based on the favorability of that key's value in dict
#Use regular expressions to create categories for forecast values
#Output scores_dict which is a {player name: score}pair
scores_dict = {}
for k in dict:
    temp= int((dict[k]['low']))
    forecast = (dict[k]['forecast'])
    dome = (dict[k]['dome'])
    if temp > 70:
        scores_dict[k] = 2
    elif temp > 50:
        scores_dict[k] = 1
    elif temp > 35:
        scores_dict[k] = 0
    elif temp > 25:
        scores_dict[k]= -1
    elif temp > 10:
        scores_dict[k]= -2
    elif temp <= 10:
        scores_dict[k] = -3
    if re.search('.*Snow.*', forecast) != None:
        scores_dict[k] -=3
    elif (re.search('.*Showers|Thunder|Rain.*',forecast)) != None:
        scores_dict[k] -=2
    elif re.search('Cloudy',forecast)!= None:
        scores_dict[k] += 0
    elif re.search('.*Sun.+', forecast) != None:
        scores_dict[k] += 0
    else:
        scores_dict[k]+=0
    if dome == '1':
        scores_dict[k]= 3
scores_dict['JAX']=scores_dict['JAC']
siphon={}
#Iterate through for each key in scores_dict and skeet. Skeet is a dictionary with {player,team}.
#Check if the value of a particular key in skeet is a in scores_dict.
#If so set the skeet key and the scores_dict value for the key as a key value pair in the Siphon dictionary
for k in scores_dict:
    for s in skeet:
        if skeet[s]== k:
            siphon[s]=scores_dict[k]

#Check to make sure every skeet key was assigned to a value in the siphon dictionary
for k in skeet.keys():
    if k not in siphon:
        print (k)
