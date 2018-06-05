import matplotlib.pyplot as plt
import tensorflow as tf
import numpy as np

import sqlite3
import time

'''
-------------------------------------------
sqlite3 gesture
-------------------------------------------
'''
def connectDb():
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
	
# Gather information from DB	
def getGamesFromDB():
	[conn,c] = connectDb()
	gamesList = []
	
	try:
		games = c.execute("SELECT * FROM matches;")
	except:
		print("Error loading games")
	for game in games:
		#summonerId int, char_id int, side string, char_global_wr long, mastery_point long, elo long)'.format(id))
		gameInfo = {
			'match_id':game[0],
			'win_side':game[1]
		}
		
		gamesList.append(gameInfo)
	
	closeDb(conn,c)
	return gamesList
	
def getInfoFromGame(gameArray):
    [conn,c] = connectDb()
    players = []
    try:
        #print(gameArray['match_id'])
        games = c.execute("SELECT * FROM `{}`;".format(gameArray['match_id']))
    except:
        print("Error loading game info")
        return False
		
        
    for game in games:
        gameInfo = {
			'summonerId':game[0],
			'char_id':game[1],
			'side':game[2],
			'char_global_wr':game[3],
			'mastery_point':game[4],
			'elo':game[5],
		}

        #print(gameInfo)
        players.append(gameInfo)
    closeDb(conn,c)
    #print(players)
    #players = converToTuple(players)
    return convertToSimpleArray(players)
    #return players

# Pushing all element in an array for each
# order: (summonerId, char_id, side, char_global_wr, mastery_point, elo)*5
def convertToSimpleArray(players):
    myTupleBlue = []
    myTupleRed = []

    for player in players:
        playerTuple = []
        player['side'] = 0 if player['side'] == 'blue' else 1
        # print(player)
        for value in player:
            if(value == 'summonerId'):
                continue

            if(player['side'] == 0):
                myTupleBlue.append(player[value])
            elif(player['side'] == 1):
                myTupleRed.append(player[value])

    #myTuple = []
    #myTuple.append(myTupleBlue)
    #myTuple.append(myTupleRed)
    #print(myTuple)
        
    return [myTupleBlue,myTupleRed]

def converToTuple(players):
    myTupleBlue = []
    myTupleRed = []
    
    #print(players)
    for player in players:
        playerTuple = []
        player['side'] = 0 if player['side'] == 'blue' else 1
        # print(player)
        for value in player:
          playerTuple.append(player[value])
        if(player['side'] == 0):
            myTupleBlue.append(playerTuple)
        elif(player['side'] == 1):
            myTupleRed.append(playerTuple)

    myTuple = []
    myTuple.append(myTupleBlue)
    myTuple.append(myTupleRed)
    #print(myTuple)
        
    return myTuple

"""if __name__ == '__main__':
	gameList = getGamesFromDB()
	for game in gameList:
		gameInfo = getInfoFromGame(game)
		print(gameInfo)"""

def get_dataset(gameList):
    """
    --------------------------
        Génération du dataset
    """

    games = []
    outcomeMatches = []
    features1 = []
    features2 = []
    for game in gameList:
        #gameInfo = getInfoFromGame(game)
        [blueSide, redSide] = getInfoFromGame(game)
        features1.append(blueSide)
        features2.append(redSide)
        
        #print("GInfo",gameInfo)
        #games.append(gameInfo)
        outcomeMatches.append(game['win_side'])
    print('winned',outcomeMatches)

    winVector = []
    for win in outcomeMatches:
        if(win == "red"):
            winVector.append(0.0)
        elif(win == "blue"):    
            winVector.append(1.0)
    '''features1 = []
    features2 = []
    for game in games:
        features1.append(game[0])
        features2.append(game[1])
    #print(features1)
    #print( np.array(features1))
    #print( np.array(features2))
    '''
    """print('features1', features1)
    print('features2', features2)"""
    data_f1 = np.array(features1)
    data_f2 = np.array(features2)
    #print('dataf1',data_f1)
    #print(len(data_f1), len(data_f2))
    # Numbers of row per class
    row_per_class = 100
    # Generate rows
    sick = np.random.randn(row_per_class, 2) + np.array([-2, -2])
    #print('s', sick)
    #print(sick)
    sick_2 = np.random.randn(row_per_class, 2) + np.array([2, 2])
 
    healthy = np.random.randn(row_per_class, 2) + np.array([-2, 2])
    healthy_2 = np.random.randn(row_per_class, 2) + np.array([2, -2])

    features = np.vstack([data_f1, data_f2])
    #for ft in features :
        #print("ft",ft)
    features = np.concatenate((data_f1,data_f2), axis=1)
    for ft in features :
        print("ft",ft)
    #targets = np.concatenate(())
    #targets = np.concatenate((np.zeros(len(data_f1)), np.zeros(len(data_f2)) + 1))
    targets = np.array(winVector)
    #print("winvector",winVector)

    #print("tgst",type(targets))
    targets = targets.reshape(-1, 1)
    #print("tgst2",targets)

    return features, targets

#------------------------------------
# Main function
#------------------------------------

if __name__ == '__main__':

    #Contain match ID and the outcome for every games
    gameList = getGamesFromDB()

    print('gameslist',gameList)

    features, targets = get_dataset(gameList)
    print("features: ",features[1])
    #print("targets: ", targets)
    # Plot points
    #plt.scatter(features[:, 0], features[:, 1], s=40, c=targets, cmap=plt.cm.Spectral)
    #plt.show()

    #print(len(features[1]), 'lenfeat')
    tf_features = tf.placeholder(tf.float32, shape=[None, 50])
    tf_targets = tf.placeholder(tf.float32, shape=[None, 1])

    #------------
    # NN build
    #------------

    # First
    w1 = tf.Variable(tf.random_normal([50, 10])) # weight
    b1 = tf.Variable(tf.zeros([10])) # biais
    # Operations
    z1 = tf.matmul(tf_features, w1) + b1
    a1 = tf.nn.sigmoid(z1)

    # second layer
    w2 = tf.Variable(tf.random_normal([10, 2])) # weight
    # 
    b2 = tf.Variable(tf.zeros([2])) # biais
    # Operations
    z2 = tf.matmul(a1, w2) + b2
    a2 = tf.nn.sigmoid(z2)

    # Output neuron
    w3 = tf.Variable(tf.random_normal([2, 1]))
    b3 = tf.Variable(tf.zeros([1]))
    # Operations
    z3 = tf.matmul(a2, w3) + b3
    py = tf.nn.sigmoid(z3)

    cost = tf.reduce_mean(tf.square(py - tf_targets))

    correct_prediction = tf.equal(tf.round(py), tf_targets)
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

    # Optimiser based on gradient descend algorithm
    optimizer = tf.train.GradientDescentOptimizer(learning_rate=0.125)# learning rate
    train = optimizer.minimize(cost) # execution of optimization operation based on previons operations

    sess = tf.Session()
    sess.run(tf.global_variables_initializer()) 
    # Initialize all variables bellow the given shape for session and graph usecase

    #----------
    # exemples
    #----------
    print("feacture 0 = ", features[0])

    print("w1", sess.run(w1))
    print("b1 = ", sess.run(b1))
    print("z1 = ", sess.run(z1, feed_dict={
        tf_features: features
    })) # pre activation of neuron
    # first value of vector times weight plus biais
    # 'donnant la valeur de la preactivation, grace a la fonction matmul'
    # SoftMax would be usefull cause values are in high range
    print('Probabilité avec la sigmoid', sess.run(a1, feed_dict={
        tf_features: features
    }))

    # error calcul on output
    print('cout de la fonction ', sess.run(cost, feed_dict={
        tf_features: features,
        tf_targets: targets
    }))
    # prediction - root square of the error
    # ------------------------------------------------------------
    # trainning session
    # during this session itteration we ll adjust weight based on optimization function
    """print("avant entrainement w1", sess.run(w1))
    print("avant  entrainement b1 = ", sess.run(b1))
    sess.run(train, feed_dict={
        tf_features: features,
        tf_targets: targets
    })
    print("apres entrainement w1", sess.run(w1))
    print("apres entrainement b1 = ", sess.run(b1))"""

    #--------------------------------------------------------------
    # Execution of the graph, trainning and accuracy measurement
    # Number of iteration for trainning (10 000) for exemple
    # -------------------------------------------------------------

    for e in range(10000):

        # training step based on gradient descend method 
        sess.run(train, feed_dict={
            tf_features: features,
            tf_targets: targets
        })
        # !!!!!! HERE we have to generate a testing dataset, because we are testing our accuracy on same dataset (we test on trainning dataset ->> very bad)
        # If we dont have a lot of values we can une leave one value cross validation (we just ll keep on data for test from trainning set each iteration)
        # Accuracy value is not relevent cause of overfitting actually
        print("accuracy !! =", sess.run(accuracy, feed_dict={
            tf_features: features,
            tf_targets: targets
        }))
        # take pre activation value before decision ( 0 or 1 -> red team or blue team win) to get percentage of win for each match
        print("certitude de victoire pour chaque match de l'équipe bleue =", 1-sess.run(py, feed_dict={
            tf_features: features,
            tf_targets: targets
        }))
        
