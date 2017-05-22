from bs4 import BeautifulSoup
import urllib.request
import re

player_dictionary = {}
#Use Beautiful Soup to parse html from input url (from fantasydata.com).Use find_all method to collect all ‘div’ tags with the class ‘statsGridWrapper top border’ and store this as the player_rows list
#Use Beautiful Soup and regular expressions to isolate player name
#Check if the player name is already in the player_dictionary, if not create a player_dictionary entry with player name as a key
#Use regular expressions to isolate player scores and append them to the value for their corresponding key(player)
#Return the key value pair of {player name, [season average, 1 week ago, 2 weeks ago]
def trend_finder(url):
    global player_dictionary
    info = urllib.request.urlopen(url).read().decode('utf-8')
    parse = BeautifulSoup(info, "html.parser")
    player_rows = parse.find_all('div', attrs={'class': 'statsGridWrapper top-border'})
    for row in player_rows:
        for rank in row.find_all('table', attrs={'class': "table"}):
            for matchup in rank.find_all('tr'):
                guy = matchup.find_all('a')[0]
                scoop = guy.string
                if scoop not in player_dictionary and scoop != 'Player':
                    player_dictionary[scoop] = []
                PPG = matchup.find_all('td', attrs={'class': "center cellSorted"})
                AVG = (str(PPG))
                points = re.findall('[0-9.]+', AVG)
                if points != []:
                    player_dictionary[scoop].append(float(points[0]))
    return player_dictionary


#---Season Averages---    A call to the trend_finder fucntion. Using a url that must be UPDATED WEEKLY found on Fanatsy Stats tab of fantasy data
dict_1 = trend_finder("https://fantasydata.com/nfl-stats/nfl-fantasy-football-stats.aspx?fs=3&stype=0&sn=0&scope=0&w=13&ew=13&s=&t=0&p=2&st=FantasyPointsPerGame&d=1&ls=FantasyPointsPerGame&live=false&pid=false&minsnaps=4")
#---1 week prior-----  A call to the trend_finder fucntion. Using a url that must be UPDATED WEEKLY found on Fantasy Data by going to Fantasy Data and setting week to 1 week prior through setting Season to Game
dict_2 = trend_finder('https://fantasydata.com/nfl-stats/nfl-fantasy-football-stats.aspx?fs=3&stype=0&sn=0&scope=1&w=13&ew=13&s=&t=0&p=2&st=FantasyPointsDraftKings&d=1&ls=FantasyPointsDraftKings&live=false&pid=false&minsnaps=4')
#--2 weeks prior-----   A call to the trend_finder fucntion.UPDATE WEEKLY found on Fantasy Data by going to Fantasy Data and setting week to 2 week prior through setting Season to Game
dict_3= trend_finder('https://fantasydata.com/nfl-stats/nfl-fantasy-football-stats.aspx?fs=3&stype=0&sn=0&scope=1&w=12&ew=12&s=&t=0&p=2&st=FantasyPointsDraftKings&d=1&ls=FantasyPointsDraftKings&live=false&pid=false&minsnaps=4')

averages_dict={}
for k in dict_3:
    averages_dict[k]=dict_3[k][0]


#Iterate through each of the keys of dict_3(Trends dictionary)
#Create key:value pairs in scores_dict based on the value for the key in dict_3. The value is a numerical score based on the favorability of that key's value in dict
#Since the values in dict_3 are lists I indexed through to find the desired value
#Output scores_dict which is a {player name: score}pair
scores_dict={}
for k in dict_3:
    if len(dict_3[k])>2:
        if dict_3[k][1] > dict_3[k][0] and dict_3[k][2] > dict_3[k][0]:
            scores_dict[k]= 2
        elif dict_3[k][1] < dict_3[k][0] and dict_3[k][2] < dict_3[k][0]:
            scores_dict[k] = - 2
        elif dict_3[k][1] > dict_3[k][0]:
            scores_dict[k] = .5
        elif dict_3[k][1] < dict_3[k][0]:
            scores_dict[k] = -.5
        else:
            scores_dict[k] = 0
    else:
        scores_dict[k]= 0


