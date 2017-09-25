import pandas
import csv

table = pandas.read_csv("table.csv",index_col=0)
games = []
with open('October5.csv') as csvfile:
	spamreader = csv.reader(csvfile)
	for row in spamreader:
		games.append(row)

def who_qualifies():
	if table["Points"].iloc[4] > table["Points"].iloc[5] :
		table["Qualified"].iloc[0:5] += 1 #Means no ties
		table["Eliminated"].iloc[5:] += 1
	else :
		table["Dif"].iloc[4] += 1
		for i in range(1,5):
			if table["Points"].iloc[4] != table["Points"].iloc[4-i] :
				table["Qualified"].iloc[0:4-i+1] += 1
				break;
			else:
				table["Dif"].iloc[4-i] += 1

		for j in range(1,6):
			if table["Points"].iloc[4] != table["Points"].iloc[4+j] :
				table["Eliminated"].iloc[4+j:] += 1
				break;
			else:
				table["Dif"].iloc[4+j] += 1

def result_of_game(game_num):

	if game_num >= len(games):
		global table #BAD
		table = table.sort_values(["Points"],ascending=False)
		who_qualifies()
		return

	#Home wins
	points(games[game_num][0],3)
	result_of_game(game_num + 1)
	points(games[game_num][0],-3)

	#Tie
	points(games[game_num][0],1)
	points(games[game_num][1],1)
	result_of_game(game_num + 1)
	points(games[game_num][0],-1)
	points(games[game_num][1],-1)

	#Visit wins
	points(games[game_num][1],3)
	result_of_game(game_num + 1)
	points(games[game_num][1],-3)

def points(team,point):
	table.loc[team,"Points"] += point

print(table)
result_of_game(0)
table["Possibility %"] = round(((2*table["Qualified"]+table["Dif"])/(table["Qualified"]+table["Eliminated"]+table["Dif"]))*50,2)
print(table)