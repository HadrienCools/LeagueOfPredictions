# LeagueOfPredictions


## Présentation du projet

Le projet a pour but de determiner la victoire de l'équipe bleue ou l'équipe rouge du célèbre jeu "League Of Legends".
Pour cela il utilise un réseau de neurones établissant des prédictions sur base de features extraites de l'API LOL V2.

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
Il est possible de rentrer un nombre d'itérations, correspondant au nombre de fois ou le réseau va être entrainé, apres chaque entrainement le réseau est testé. 


## Améliorations 
* Softmax pour normaliser les données d'entrée, le réseau a du mal à s'entrainer.
* Relu, voir le comportement en utilisant une autre fonction non linéaire.
* Lambda variable, voir le comportement en fonction du facteur d'apprentissage.
* Feature selection, sélectionner mieux les données et plus de données pour avoir plus de features .
* Avoir un set d'entrainement et un set de test distincts.
* Augmenter la taille des sets.
* ...

### Auteurs

* Yannick Berckmans
* Cools Hadrien
