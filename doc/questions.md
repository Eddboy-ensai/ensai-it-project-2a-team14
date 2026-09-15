## Concernant la base de données  

1) Comment construire la base de données ?  

Récupérer en permanence les données via l'API et les rajouter à une table de données  

2) Comment organiser le modèle de données ?  

À étudier selon les trois formes normales ?  

**Table de données des stations**  

attributs : id station, nom de la station, localisation géographique, nombre de vélos disponibles, nombre de places libres, date, état de la station  

**Table de données des utilisateurs**  

attributs : id utilisateur, pseudo, mot de passe hashé, mail, liste de stations favorites  

3) Comment gérer le portage d'une ville à l'autre ?  

4) Comment gérer les enregistrements en termes d'objets ? Créer des objets "enregistrement" ou comme attribut de la classe Station, ou autre ?

## Séance du 04/09  

### Résumé  

Création du diagramme d'activité  
Concernant le rapport : ajout des sections à compléter, réflexion sur les classes, les services

### Travail à faire  

Rédiger les sections et tracer les diagrammes suivants :
Diagramme de Gantt + réflexion sur la formule du score de fiabilité (Alix)
Structure de l'API (frontend, backend, etc.) + arborescence du projet (Eddy)
Création base de données + questions du stockage sur le long terme (Eliot)
Diagramme d'activité (Samuel)  
Réfléchir au score de fiabilité (Méline)  



Réfléchir aux calculs (pour voir comment organiser la classe station_service)



### Endpoints

Proposition :

#### Comptes et authentification

| Chemin | Méthode | Entrée | Sortie (succès) | Habilitation | Description |
| :---- | :---- | :---- | :---- | :---- | :---- |
| `/create_user` | POST | corps : `username`, `password` | `201` + `User` | public | Crée un compte |
| `/login` | POST | corps : `username`, `password` | `200` + jeton d'accès | public | Authentifie et renvoie un jeton |
| `/users` | GET | `?limit=&offset=` | `200` + `liste[User]` | admin | Liste les comptes |
| `/users/{id_user}` | PATCH | corps : `username` et/ou `password` | `200` + `User` | admin | Modifie un compte |
| `/users/{id_user}` | DELETE | - | `204` | admin | Supprime un compte |

#### Stations

| Chemin | Méthode | Entrée | Sortie (succès) | Habilitation | Description |
| :---- | :---- | :---- | :---- | :---- | :---- |
| `/stations` | GET | - | `200` + `liste[Station]` | connecté | Liste les stations |
| `/stations/{id_station}` | GET | - | `200` + `Station` | connecté | État actuel d'une station + indicateurs + score |
| `/stations/{id_station}/history` | GET | `?periode=24h\|7j\|30j` | `200` + `liste[Releve]` | connecté | Évolution de la disponibilité (F3) |
| `/suggestions` | GET | `?lat=&lon=&limit=` | `200` + `liste[Station]` | connecté | Classement multicritère (F5) |

#### Gestion des stations favorites

| Chemin | Méthode | Entrée | Sortie (succès) | Habilitation | Description |
| :---- | :---- | :---- | :---- | :---- | :---- |
| `/favorites` | GET | - | `200` + `liste[Station]` | connecté | Favoris de l'utilisateur courant |
| `/favorites/{station_id}` | PUT | - | `204` | connecté | Ajoute une station aux favoris |
| `/favorites/{station_id}` | DELETE | - | `204` | connecté | Retire une station des favoris |
