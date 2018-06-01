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
#        print(player)
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
#        print(player)
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

if __name__ == '__main__':

    #Contain match ID and the outcome for every games
    gameList = getGamesFromDB()

    #print("test23")
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

    # First
    w1 = tf.Variable(tf.random_normal([50, 3])) # poids
    #chaque caracteristique aura 3 poids associés
    b1 = tf.Variable(tf.zeros([3])) # biais
    # Operations
    z1 = tf.matmul(tf_features, w1) + b1
    a1 = tf.nn.sigmoid(z1)

    # Output neuron
    w2 = tf.Variable(tf.random_normal([3, 1]))
    b2 = tf.Variable(tf.zeros([1]))
    # Operations
    z2 = tf.matmul(a1, w2) + b2
    py = tf.nn.sigmoid(z2)

    cost = tf.reduce_mean(tf.square(py - tf_targets))

    correct_prediction = tf.equal(tf.round(py), tf_targets)
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

    # on utilise un optimiser qui va effectuer l opération de la descente de gradient
    optimizer = tf.train.GradientDescentOptimizer(learning_rate=200000001)# on lui donne un learning rate les 
    train = optimizer.minimize(cost) # opération d entrainemenet utilisant l optimiser en vue de minimiser le cout

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
    })) #donnez la valeur de preactivation du neurone
    # on prend la premiere valeur de l array et on le mukltiplie par le poids associe et on lui ajoute lavaleur du biaius. 
    # donnant la valeur de lma preactivation, grace a la focntion matmul
    #dans l exemple on a des valeur qui sont assez greande il aurait ezte bien de les normaliser
    print('Probabilité avec la sigmoid', sess.run(a1, feed_dict={
        tf_features: features
    }))

    # calcul de l erreur
    #calculer l erreur ensortie du reseau de neurone

    print('cout de la fonction ', sess.run(cost, feed_dict={
        tf_features: features,
        tf_targets: targets
    }))
    # prediction - erreur au carée

    # ------------------------------------------------------------
    # une session d entrainemeent
    # expliquer la descente de gradient, l optimiser la fonction de reduction de cout. 
    """print("avant entrainement w1", sess.run(w1))
    print("avant  entrainement b1 = ", sess.run(b1))
    sess.run(train, feed_dict={
        tf_features: features,
        tf_targets: targets
    })
    print("apres entrainement w1", sess.run(w1))
    print("apres entrainement b1 = ", sess.run(b1))"""

    #--------------------------------------------------------------
    for e in range(100):

        sess.run(train, feed_dict={
            tf_features: features,
            tf_targets: targets
        })

        print("accuracy =", sess.run(accuracy, feed_dict={
            tf_features: features,
            tf_targets: targets
}))