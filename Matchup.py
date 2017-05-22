import urllib.request

import re
#Use Beautiful Soup to parse html from input url (from fantasydata.com).Use find_all method to collect all ‘div’ tags with the class ‘statsGridWrapper top border’ and store this as the player_rows list
#Filter player_rows to isolate the matchup difficulty number by using regular expressions and beautiful soup methods
#Append this number to the matchup_list
#Use regular expressions to isolate player name and append to player_list
#Zip together player_list and the matchup_list to form matchup_dict

def get_matchup(url):
    page = urllib.request.urlopen(url).read().decode('utf-8')
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(page,"html.parser")
    player_rows = soup.find_all('div', attrs={'class': 'statsGridWrapper top-border'})
    player_list=[]
    matchup_list =[]
    for row in player_rows:
        for rank in row.find_all('table', attrs={'class': "table"}):
            for matchup in rank.find_all('tr'):
                    guy = matchup.find_all('a')[0]
                    scoop = str(guy)
                    tags=matchup.find_all('td', attrs={'class':re.compile(('bold'))})
                    if len(tags)> 1:
                        matchup_list.append(tags[1].text)
                    elif len(tags)> 0:
                        matchup_list.append(tags[0].text)
                    if re.search('/nfl-stats.+', scoop) != None:
                        dude = guy.string
                        player_list.append(dude)
    matchup_dict={}
    for p, v in zip(player_list, matchup_list):
        matchup_dict[p]=v
#Iterate through each of the keys of matchup_dict
#Create key:value pairs in scores_dict based on the value for the key in matchup_dict. The value is a numerical score based on the favorability of that key's value in matchup_dict
#Output scores_dict which is a {player name: score}pair
    scores_dict = {}
    for k in matchup_dict:
        opp= int(matchup_dict[k])
        if opp >= 25:
            scores_dict[k]= 3
        elif opp>= 20:
            scores_dict[k]= 2
        elif opp >= 15:
            scores_dict[k] = 0
        elif opp >= 10:
            scores_dict[k] = -1
        elif opp >=5:
            scores_dict[k] = -2
        elif opp<5:
            scores_dict[k]= -3
    return scores_dict



#Use Beautiful Soup to parse html from input url (from fantasydata.com).Use find_all method to collect all ‘div’ tags with the class ‘statsGridWrapper top border’ and store this as the player_rows list
#Filter player_rows to isolate the salary number by using regular expressions and beautiful soup methods
#Append this number to the salary_list
#Use regular expressions to isolate player name and append to player_list
#Zip together player_list and the salary_list to form salary_dict


def get_salary(url):
    inputs = urllib.request.urlopen(url).read().decode('utf-8')
    salary_dict = {}
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(inputs,"html.parser")
    player_rows = soup.find_all('div', attrs={'class': 'statsGridWrapper top-border'})
    player_list = []
    salary_list = []
    for row in player_rows:
        for rank in row.find_all('table', attrs={'class': "table"}):
            for matchup in rank.find_all('tr'):
                guy = matchup.find_all('a')[0]
                scoop = guy.string
                if scoop != 'Player':
                    player_list.append(scoop)
                PPG = matchup.find_all('td', attrs={'class': " cellSorted"})
                AVG = (str(PPG))
                points = re.findall('[0-9.,]+', AVG)
                if points != []:
                    points= int(points[0].replace(',',''))
                    sal= points/1000
                    salary_list.append((sal))

    salary_dict = {}
    for p, v in zip(player_list, salary_list):
        salary_dict[p] = v


    return salary_dict

