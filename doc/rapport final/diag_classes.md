## Code PlantUML
@startuml

enum RoleUtilisateur {
  USER
  ADMIN
}

enum EtatStation {
  FONCTIONNELLE
  VIDE
  SATUREE
}

class Utilisateur {
  + id : int
  - email : str
  - mot_de_passe_hashé : str
  - role : RoleUtilisateur
  - stations_favorites : list[int]
  --
  + creer_compte()
  + se_connecter()
  + se_deco()
  + ajouter_favori(station_id : int)
  + retirer_favori(station_id : int)
}

class Station {
  + id : int
  + nom : str
  + localisation : int 
  + capacite : int
  + capacite_velos_electriques : int
  --
  + etat_actuel() : EtatStation
  + taux_remplissage() : float
}

class Recommandation {
  + station : Station
  + distance : float
  + score : float
  + rang : int
  --
  + calculer_score_rang() : float
}

Utilisateur-->Station
Station-->Recommandation

@enduml
