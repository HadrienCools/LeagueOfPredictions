import requests
import sqlite3
import json
import time


#print(json_data)


#c.execute(" INSERT INTO matches VALUES(?,'red')", (id_match,))
'''
value = fetchFromDB("SELECT * FROM matches")
print(yannic.fetchone())
'''



'''
----------------------------------------------------------------------------
----------------------------------------------------------------------------
Function definitions
----------------------------------------------------------------------------
----------------------------------------------------------------------------
'''


'''
-------------------------------------------
sqlite3 gesture
-------------------------------------------
'''


def configDb():
	conn = sqlite3.connect('data.db')
	c = conn.cursor()
	return [conn,c]

def closeDb(c, conn):
	try:
		c.commit()
		conn.close()
		return True
	except:
		return False

'''
-------------------------------------------
Loading data from API
-------------------------------------------
'''

def fetchFromAPI(url, payload):
	try:
		response = requests.get(url, params = payload)
		json_data = json.loads(response.text)
		#If the game doesn't exist, the request send back a "status" error
		if 'status' in json_data:
			code = json_data['status']['status_code'] 
			print("error code "+str(code)+" from fetchFromAPI")
			if(str(code) == "429"):
				print("limit exceeded. Wait 1 min.")
				time.sleep(60)
				return "429"
		
		return json_data
	except:
		return False

def fetchFromChampionGGApi(rank,championId):
	#'BRONZE', 'SILVER', 'GOLD', 'PLATINUM', 'PLATINUM,DIAMOND,MASTER,CHALLENGER'
	unranked = False
	
	if(rank == 'BRONZE'):
		championGGtier = 'BRONZE'
	elif(rank == 'SILVER'):
		championGGtier = 'SILVER'
	elif(rank == 'GOLD'):
		championGGtier = 'GOLD'
	elif(rank == 'PLATINUM'):
		championGGtier = 'PLATINUM'
	elif(rank == None):
		unranked = True
	else:
		unranked = True

	
	#Char global winrate
	if(unranked == True):
		call = "http://api.champion.gg/v2/champions/"+str(championId)+"?&api_key="+championGGApiKey
	else:
		call = "http://api.champion.gg/v2/champions/"+str(championId)+'?elo='+str(championGGtier)+"&api_key="+championGGApiKey

	try:
		response = requests.get(call)
		json_data = json.loads(response.text)
		#print(json_data)
		#winrate = json_data['data'][0]['winrate']
		winrate=json_data[0]['winRate']
		#print(winrate)
		return winrate
	except:
		return False

'''
-------------------------------------------
Table creation and gesture
-------------------------------------------
'''

def createMatchesTable(c):
	try:
		c.execute('''CREATE TABLE matches (match_id integer, win_side text)''')
		return True
	except:
		return False

def createMatchTable(id):

	struct_match = 'summonerId int, char_id int, side string, char_global_wr long, mastery_point long, elo long' #elo a verifier
	
	try:
		#Only way to insert a parameter table name!
		c.execute('CREATE TABLE `{}` (summonerId int, char_id int, side string, char_global_wr long, mastery_point long, elo long)'.format(id))
		return True
	except:
		return False
	

'''
-------------------------------------------
Table insertion
-------------------------------------------
'''


def insertIntoMatchesTable(id_match, winside):
	
	try:
		c.execute("INSERT INTO matches VALUES(?,?)",(int(id_match),str(winside)))
		return True
	except:
		return False


def insertIntoMatchTable(id, params):

	#--!-- NO WINRATE FOR THE MOMENT BECAUSE NO CHAMPION.GG CALL
	#params["char_global_wr"] = 50
	#print("helloOut")
	try:
		try:
			c.execute("INSERT INTO `{}` VALUES(?,?,?,?,?,?)".format(id), (int(params["summonerId"]),int(params["char_id"]),str(params["side"]),params["char_global_wr"],params["mastery_point"],params["elo"]))
			c.commit()
		except sqlite3.Error as er:
			print('er:', er.message)
	
		print('we inserted data in the table '+str(id))
		return True
	except:
		return False

'''
-------------------------------------------
Loading data from DB
-------------------------------------------
'''

def fetchFromDB(c, request):
	return c.execute(request)

'''
-------------------------------------------
Procedural Functions
-------------------------------------------
'''

def leaguePointToElo(tier, rank, leaguePoints):
	
	#Based on https://boards.euw.leagueoflegends.com/en/c/champions-gameplay-en/ONXtEyFR-estimated-mmr-values-of-each-and-every-division-placements-explained
	if(tier == "BRONZE"):
		if(rank == "V"):
			return 0+869*(leaguePoints/100)
		if(rank == "IV"):
			return 870+69*(leaguePoints/100)
		if(rank == "III"):
			return 940+69*(leaguePoints/100)
		if(rank == "II"):
			return 1010+69*(leaguePoints/100)
		if(rank == "I"):
			return 1080+69*(leaguePoints/100)

	elif(tier == "SILVER"):
		if(rank == "V"):
			return 1150+69*(leaguePoints/100)
		if(rank == "IV"):
			return 1220+69*(leaguePoints/100)
		if(rank == "III"):
			return 1290+69*(leaguePoints/100)
		if(rank == "II"):
			return 1360+69*(leaguePoints/100)
		if(rank == "I"):
			return 1430+69*(leaguePoints/100)

	elif(tier == "GOLD"):
		if(rank == "V"):
			return 1500+69*(leaguePoints/100)
		if(rank == "IV"):
			return 1570+69*(leaguePoints/100)
		if(rank == "III"):
			return 1640+69*(leaguePoints/100)
		if(rank == "II"):
			return 1710+69*(leaguePoints/100)
		if(rank == "I"):
			return 1780+69*(leaguePoints/100)

	elif(tier == "PLATINUM"):
		if(rank == "V"):
			return 1850+69*(leaguePoints/100)
		if(rank == "IV"):
			return 1920+69*(leaguePoints/100)
		if(rank == "III"):
			return 1990+69*(leaguePoints/100)
		if(rank == "II"):
			return 2060+69*(leaguePoints/100)
		if(rank == "I"):
			return 2130+69*(leaguePoints/100)
	elif(tier == "DIAMOND"):
		if(rank == "V"):
			return 2200+69*(leaguePoints/100)
		if(rank == "IV"):
			return 2270+69*(leaguePoints/100)
		if(rank == "III"):
			return 2340+69*(leaguePoints/100)
		if(rank == "II"):
			return 2410+69*(leaguePoints/100)
		if(rank == "I"):
			return 2480+69*(leaguePoints/100)
	elif(tier == "MASTER"):
		#We estimate that challenger ~= master 400 lp
		return 2585+349*(leaguePoints/400)
	elif(tier == "CHALLENGER"):
		return 2900


#Get recent game through the "featuredGame" API call
def getRecentGame():
	
	while(True):
		jsonData = fetchFromAPI(featuredGamesURL, {'api_key': key})
		
		if(jsonData != False):
			for game in jsonData["gameList"]:
				return game["gameId"]
			print("No summoner Rift game found in featured games")
			return False
		elif(jsonData == "429"):
			continue
		else:
			return False

		#We arrived at the end
		break
	
#Verify if the game is correct for the database
#Correct means an existing, good patch and SR game	
def verifyGame(id):
	
	#Gathering data
	while(True):
		jsonData = fetchFromAPI(matchInfoURL+'/'+str(id), {'api_key': key})
	
		if(jsonData == False):
			print("Error matchInfoURL from API")
			return False
		elif(jsonData == "429"):
			continue

		#If the game doesn't exist, the request send back a "status" error
		if 'status' in jsonData:
			code = jsonData['status']['status_code']
			print("Wrong game. Error code: "+str(code))
			return False

		#We check if it's a Summoner's Rift map
		if(not(jsonData['queueId'] == srDraft or jsonData['queueId'] == srRankedSolo or jsonData['queueId'] == srBlindPick or jsonData['queueId'] == srRankedFlex)):
			print("It's not a Summoner's Rift game")
			return False
		
		break
		
	return jsonData

#A function to populate the database
def uniquePopulate(id):

	idProcess = id
	#To get the match values
	for i in range(0,1000):
		idProcess = id+i
		jsonData = verifyGame(idProcess)
		if(jsonData == False):
			print("The game we found was bad!")
		else:
			print("The game we found was OK!")
			break;

	#Getting the winside
	if( jsonData['teams'][0]['win'] == 'Win'):
		if(jsonData['teams'][0]['teamId'] == 100):
			#--!-- STILL NEED TO CHECK THAT
			winside = "blue"
		elif(jsonData['teams'][0]['teamId'] == 200):
			winside = "red"
	elif(jsonData['teams'][0]['win'] == 'Fail'):
		if(jsonData['teams'][0]['teamId'] == 100):
			#--!-- STILL NEED TO CHECK THAT
			winside = "red"
		elif(jsonData['teams'][0]['teamId'] == 200):
			winside = "blue"


	#We create the player dict
	players = list()

	#The structure we are looking for: summonerId:['char_id': int, 'side': string, "char_global_wr": long, "mastery_point" long, "elo": string]
	for player,info in zip(jsonData['participantIdentities'],jsonData['participants']):
		summonerId = player["player"]['summonerId']

		#--!-- NEED TO CHECK THIS! IDK IF 100 = BLUE OR RED
		if(info['teamId'] == 100):
			side = "blue"
		elif(info['teamId'] == 200):
			side = "red"
		element = {'summonerId': summonerId, 'char_id':info['championId'], 'side':side}
		players.append(element)
		#players[player["participantId"]] = {'summonerId': summonerId, 'char_id':info['championId'], 'side':side}


	#Now, we are gathering info for each player
	for player in players:
		while(True):
			#Mastery points
			call = (masteriesCharInfo[0]+str(player['summonerId'])+masteriesCharInfo[1]+str(player['char_id']))
			
			playerJsonData = fetchFromAPI(call, {'api_key': key})
			if(playerJsonData == False):
				print("This player returned error for mastery points: "+ str(player['summonerId'])+" with champion: "+str(player['char_id']))
				player['mastery_point'] = 0
			elif(playerJsonData == "429"):
				continue
			else:
				player['mastery_point'] = playerJsonData['championPoints']
			
			#If we arrived at the end, we can break the loop "retrying until call are allowed"
			break
		
		while(True):
			#League
			call = leaguePointsURL+str(player['summonerId'])
			playerJsonData = fetchFromAPI(call, {'api_key': key})
			
			if(playerJsonData == False):
				print("Error while processing League Rank for player: "+ str(player['summonerId']))
			elif(playerJsonData == "429"):
				continue
				

			#CHECK IF HE HAS A LEAGUE
			print(playerJsonData)
			if(playerJsonData == []):
				player['elo'] = 0
				winrate = fetchFromChampionGGApi(None, player['char_id'])
			else:
				#We need to do SOMETHING ELSE if the player has no rank yet!
				player['elo'] = leaguePointToElo(playerJsonData[0]['tier'],playerJsonData[0]['rank'],playerJsonData[0]['leaguePoints'])

				winrate = fetchFromChampionGGApi(playerJsonData[0]['tier'], player['char_id'])
				if(winrate == False):
					print("a problem in the champion.gg call happened")
			
			#We insert the winrate into the dict
			player['char_global_wr'] = winrate
		
			#If we arrived at the end, we can break the loop "retrying until call are allowed"
			break
		
	print(players)
	
	#NOW, WE NEED TO POPULATE THE DB
	if(insertIntoMatchesTable(idProcess, winside) == False):
		print('Problem while inserting data into "Matches" table')
	
	if(createMatchTable(idProcess) == False):
		print('Problem while creating the Match table')
	else:
		print('Correctly created the table')

	for player in players:
		print("trying")
		print(player)
		insertIntoMatchTable(idProcess, player)
	
	return idProcess


def multiplePopulate():
	
	#--!-- PROBLEM: ATM, IF NO RECENT MATCH IS SR, OUR SCRIPT DOESN'T WORK
	#THAT'S WHY I BYPASSED THIS PART AND PUT A FIXED ID 

	
	idRecentMatch = getRecentGame()
	if(idRecentMatch == False):
		print("Error fetching idRecentMatch")
		return False
	
	#To get a recent game

	#FOR TESTS
	#2759576982 = DO NOT EXIST

	#It seems like game AROUND (-1000) an highlighted match in HA are HA!
	#2759576981 = EXIST (Howling Abyss)
	#2759576980 = EXIST (Howling Abyss)
	
	#It seems like game AROUND (-1000) an highlighted match in SR are SR!
	#2760946266 = EXIST (Solo Ranked)
	#2760945266 = EXIST (Solo ranked)

	#--!-- WE BY-PASS THE "Random ID selection"
	#idRecentMatch = 2760945266


	idRecentMatch -= 5000

	#--!-- For test, we break the while
	#for x in range(0,100):
	print(idRecentMatch)
	for i in range(0,10):
		idRecentMatch = uniquePopulate(idRecentMatch)
		idRecentMatch +=1
	


if __name__ == "__main__":
    

	#Values definition

	#NEED TO FETCH THE CURRENT PATCH
	patch = 8.7


	key = 'RGAPI-c0f00d89-722e-4e6b-8342-3ae9bef81c73'
	championGGApiKey='8c07f22da47161cb742890f40ce828ee'

	featuredGamesURL = 'https://na1.api.riotgames.com//lol/spectator/v3/featured-games'
	matchInfoURL = 'https://na1.api.riotgames.com/lol/match/v3/matches'
	masteriesCharInfo = ['https://na1.api.riotgames.com/lol/champion-mastery/v3/champion-masteries/by-summoner/','/by-champion/']
	leaguePointsURL = "https://na1.api.riotgames.com/lol/league/v3/positions/by-summoner/"

	#match type IDs
	srDraft = 400
	srRankedSolo = 420
	srBlindPick = 430
	srRankedFlex = 440

	#db
	[c,conn] = configDb()
	#--!-- THE FIRST TIME, WE NEED TO CREATE THE GLOBAL MATCHES TABLE
	createMatchesTable(c)
	#createMatchTable(2760944266)
	#insertIntoMatchesTable(12, "red")
	#c.execute("INSERT INTO matches VALUES(?,?)",(int(12),str("blue")))
	#c.execute("INSERT INTO `{}` VALUES(?,?,?,?,?,?)".format(2760944266), (12,12,"blue",58,12,12))
	#c.execute("INSERT INTO `{}` VALUES(?,?,?,?,?,?)".format(id), (int(params["player_id"]),int(params["char_id"]),str(params["side"]),long(params["char_global_wr"]),long(params["mastery_point"]),long(params["elo"])))
	#insertIntoMatchTable(2760944266,{"player_id":13,"char_id":13, "side":"blue","char_global_wr":59,"mastery_point":12000,"elo":1455})

	#remplissage db

	multiplePopulate()

	#print(fetchFromDB(c, 'select * from `2760944266`').fetchone())

	#close DB
	print(closeDb(c,conn))
