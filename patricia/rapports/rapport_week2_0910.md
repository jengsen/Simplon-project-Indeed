# Rapport week 2

## Scrapping + BDD
Nous avons terminé le scrapping. Hier Pierre nous a fait une présentation du code et il a repondu à nos questions.


Scrapping:
Dans les difficultés rencontrées:
1) Les contrats : Ils n'apparaissent pas au même endroit dans la page donc très peu des lignes ont le contrat (autours de 10%).
Solution possible : Recupérer toutes les infos du header d'un poste. 
2) Pour changer à la page suivante sur indeed les paths avaient le même nom de classe. Ils passaient à la page suivante et une fois scrappé la page suivante il passait à la page précédente.
Solution : les variables suivantes et précédentes ont été prise en compte. Si la classe NP ne compte qu'une seule variable (précédent) il quitte la page, sinon clicker sur l'élément suivant.
3) Il enregistrait la ville précédente (à cause des cookies), une fonction a été crée pour effacer l'historique . Ex: Nantes/ Paris (ils les collait côte à côte).


BDD
La base de donnée comporte autour de 10000 lignes et une dizaine de colonnes (id, titre du poste, entreprise, ville, salaire, type de contrat, descriptif du poste, date de publication).
Concernant la colonne type de contrat, nous devons réfléchir à l'utiliser ou pas pour faire des prédictions.



## Preprocessing
Ludovic a travaillé sur la colonne des salaires. Cette colonne est de type str et les salaires obtenus représentent 20% des données obtenues. Ils sont exprimés de manière différente:
Soit de l'heure, soit par jour, soit à la semaine, soit par mois ou bien par année (par tranches). Une fonction a été crée pour traiter les différents cas, à l'aide des regex pour avoir tous les salaires sur l'année. On obtient une nouvelle colonne avec la moyenne pour ceux dont il y avait une fourchette.

Pour la colonne ville, On essaye de séparer Paris de sa banlieu et on essaye de regrouper les autres villes avec leur banlieue.

Pour la colonne "descriptif du poste" nous pensons et testons plusieurs possibilités. Nous cherchons à trouver une variable exploitable pour prédire les salires. Nous avons pensé à extraire une liste de skills qui puissent permettre de prédire un salaire élevé ou pas. Par example: "Machine learning", "deep learning", "NLP", "intelligence artificielle ", etc.
Pour ceci, Pierre travaille sur les colonnes "titre du poste" et "descriptif du poste". Il compte l'apparition de chaque mot (un ou deux mots qui se suivent) avec un minimun d'occurence de  0.05(descriptif) ou 0.005 (titre). Ensuite, une matrise de correlation entre l'ocurrence des mots et le salaire, on obtient donc les mots qui ont le plus d'impact sur le salaire. On a gardé les 10 mots les plus négatifs et les 10 mots les plus positifs. On fera un modèle avec ces 20 nouvelles colonnes pour prédire le salaire. 

Objectif : proposer des modèles à la fin de la semaine.



## Flask
Nous avons tous suivi un tuto flask.



## Word embedding
Nous avons commencé à le regarder. Les notions sont comprises mais nous ne savons pas encore comment l'appliquer à notre problématique. 
Il est possible de l'utiliser pour faire des groupes des mots pour les colonnes "titre du poste" et "descriptif du poste".
Nous continuons d'approfondir sur le domaine.

