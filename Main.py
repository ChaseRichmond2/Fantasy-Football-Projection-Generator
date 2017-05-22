import urllib.request
import plotly.plotly as py
import plotly.graph_objs as go
import csv

req = urllib.request.Request(
    'http://www.fantasyfootballnerd.com/service/weather/json/tcmdyhj8qti7/',
    data=None,
    headers={
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
    }
)
import Matchup
import Weather
import Trend

matchup_scores= Matchup.get_matchup("https://fantasydata.com/nfl-stats/daily-fantasy-football-salary-and-projection-tool.aspx?fs=1&stype=0&sn=0&scope=0&w=14&ew=14&s=&t=0&p=2&st=FantasyPointsDraftKings&d=1&ls=&live=false&pid=false&minsnaps=4")
#Calls get_matchup function in the Matchup script --UPDATE URL WEEKLY-- Found on Fantasy Data by using the salary tab
salary_dict= Matchup.get_salary('https://fantasydata.com/nfl-stats/daily-fantasy-football-salary-and-projection-tool.aspx?fs=1&stype=0&sn=0&scope=0&w=14&ew=14&s=&t=0&p=2&st=DraftKingsSalary&d=1&ls=DraftKingsSalary&live=false&pid=false&minsnaps=4')
#Calls get_salary function in the Matchup script---UPDATE WEEKLY---  Found on Fantasy Data using the salary tab.
#Must SORT by salary on page before getting URL





adjust_dict= {}  #Creates an adjustment dictionary which sums the values for Weather, Trend and Matchup score adjustment for a particular key
for k in matchup_scores:
    if k in Weather.siphon.keys() and k in Trend.scores_dict.keys():
        adjust_dict[k]= matchup_scores[k] + Weather.siphon[k] + Trend.scores_dict[k]



averages = Trend.averages_dict
projection_dict={}   #Creates a projection dictionary which adds the adjust_dict value to a given player's weekly average to generate his projection for the week
for k in adjust_dict:
    if k in averages:
        projection_dict[k]=averages[k]+ adjust_dict[k]



rankings= sorted(projection_dict,key=lambda x:projection_dict[x],reverse = True)   #Produces a sorted list of players based on their weekly projection in descending order
num_rank=(list(enumerate(rankings)))

for person in rankings[:32]:
    print (person,projection_dict[person])  #Outputs a player name with their corresponding projection

s_rankings = sorted(salary_dict,key=lambda x:salary_dict[x],reverse=True)   #Produces a sorted list of players based on their salary cost in descending order
num_sal=(list(enumerate(s_rankings)))

points_per_cost={}  #Creates a points_per_cost dictionary which assigns a each player a value based on a players projection divided by their salary
for k in projection_dict:
    if k in salary_dict:
        points_per_cost[k]=projection_dict[k]/salary_dict[k]
print (points_per_cost)

value_rankings = sorted(points_per_cost,key=lambda x:points_per_cost[x],reverse=True)  #Produces a sorted list of players based on value produced in the points_per_cost dictionary


adjust_list=[]
viz_values_list=[]
for person in value_rankings[:25]:    #Creates lists of values from the adjust_dict and point_per_cost dictionary so they can be used in the Plotly visulaization
    adjust_list.append(adjust_dict[person])
    viz_values_list.append(points_per_cost[person])



data = [
    go.Scatter(
        x= viz_values_list,
        y= value_rankings[:25],
        mode='lines+markers',
        error_y=dict(
            type='data',
            symmetric=False,
            array=adjust_list
        )
    )
]   #Creates a plotly scatter with player value score on the x axis and player names on the Y axis.

layout = dict(title = 'Player Projections Divided by DraftKings Salary',
              xaxis = dict(title = 'Value Score')
              #yaxis = dict(title = 'Player Name'),
              )
fig = dict(data=data, layout=layout)
py.plot(fig, filename='error-bar-asymmetric-array')

with open('Projections.csv', 'w', newline='') as csvfile:
    fieldnames = ['Rankings','Player', 'Projection','Projection/Salary']
    Ranker = writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    counter=0
    for p in rankings[:20]:
        counter += 1
        writer.writerow({'Rankings':counter,'Player':p,'Projection': projection_dict[p],'Projection/Salary':points_per_cost[p] })
#Creates a CSV file that has columns of Ranking, Player, Projection, and Projection/Salary for each player in the top 20.
