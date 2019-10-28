# 1st Rapport week 1

## Scrapping (Ursula)
Le code est fonctionnel, il manque faire un peu de regex.

Objectif: Terminer aujourd'hui. Si cela fonctionne le lancer ce soir.
             Avoir la base de données ce weekend.
             
Problèmes rencontrés: 
- scrapper les bonnes infos
- la date : pour quelques uns ce n'était pas en page principale, il fallait clicker avant .
- type de contrat : il change de possition  par rapport au type de navigateur.
             
             
## Pierre

Création de la fonction pour la connexion à la BDD mongo
Création d'un Github repository
Faire des fonctions et des classes 'squelette' pour rendre fonctionnel le scrapping (Aider Ursula avec le scrapping). 


## Tester des modèles 
Preprocessing

Ludovic :
- Chercher un dataset
- Refléchir aux features qu'on va choisir (localisation, postes... entreprise)
- Application des méthodes ensemblistes (Arbres de decision et Random Forest) sur une base de données de 5000 lignes environ.

Patricia :
- Application des modèles Regression Logistique et Kernel RBF, petite base de données (200 lignes)

Problèmes rencontres :
Salaires:
On a trouvé des fourchettes, comment les traiter?
- Faire la moyenne -> si la fourchette est trop vaste  ce n'est pas forcement très bien.
- Faire un système de classification en fonction des diplômes ou années d'expériences. Réflechir à un coefficient. Si la personne a beaucoup des diplômes -> le rapprocher du maximun, etc...
Métiers:
- Les titres sont très diverses pour un même type de poste -> harmoniser les titres, comment? Créer fonction qui regroupe les postes par similarité.

