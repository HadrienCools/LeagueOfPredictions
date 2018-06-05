# LeagueOfPredictions


## Présentation du projet

Le projet a pour but de déterminer la victoire de l'équipe bleue ou l'équipe rouge du célèbre jeu "League Of Legends".
Pour cela il utilise un réseau de neurones établissant des prédictions sur base de features extraites de l'API LOL V3.

* Il faut garder en tête que le jeu contient beaucoup d'aléatoire et que le facteur humain est présent, il n'y a donc aucunes certitudes.

## Fichiers 

### Populate.py

Script appelant l'API, il s'occupe des appels et extrait les données importantes de chaques matchs et les informations relatives (Champions utilisés, expériance des joueurs, taux de victoire des joueurs).

### data.db

Base de données où sont stockés les données relatives aux différentes parties.

### Network.py

Fichier principal, il contient la mise en forme des données sous forme d'un vecteur devenant plus tard les features d'entrée du réseau de neurones.
Il contient le schéma du réseau de neurones, les opérations qu'il devra effectuer et  l'enchainement logique de ces opérations. 
Il contient une boucle permettant l'entrainement avec le dataset proposé en entrée.
Il est possible de rentrer un nombre d'itérations, correspondant au nombre de fois ou le réseau va être entrainé, après chaque entrainement le réseau est testé. 

## Utilisation 
* Avoir python > 3.5.
* Installer Tensorflow - matplotlib - numpy.
* Pour windows l'installation peut rencontrer des erreurs, [des solutions sont proposées dans ce thread.](https://github.com/tensorflow/tensorflow/issues/5949)
* Cloner dans le répo 'git clone https://github.com/HadrienCools/LeagueOfPredictions.git'
Deux opérations sont disponnibles
* Remplir la base de données avec des appels à l'API, il faut simplemnt inserer sa clée dans le code pour pouvoir effectuer les appels, la clé expire tous les 24H.
** S'inscrire et demander une clé [sur le site.](https://developer.riotgames.com/)
* Pour la génération du réseau de neurone et l'entrainement, utiliser le fichier network.py
  ** Utiliser la commande'python network.py' les résultats seront affichés en sortie.

## Améliorations 
* Softmax pour normaliser les données d'entrée, le réseau a du mal à s'entrainer.
* Relu, voir le comportement en utilisant une autre fonction non linéaire.
* Lambda variable, voir le comportement en fonction du facteur d'apprentissage.
* Feature selection, sélectionner mieux les données et plus de données pour avoir plus de features .
* Avoir un set d'entrainement et un set de test distincts.
* Augmenter la taille des sets.
* ...

### Sources
* [API League Of Legends](https://developer.riotgames.com/api-methods/)
* [Champion.GG API](http://api.champion.gg/)
* [Tutoriel Tensorflow](https://www.youtube.com/watch?v=O9yl9KKKoQI)
* [Projet similaire discutant des aspects utilisés](https://github.com/apovedamckay/LoL-neural-network)
* [Projet d'analyse de partie](https://github.com/vingtfranc/LoLAnalyzer)

### Auteurs

* Yannick Berckmans
* Cools Hadrien
