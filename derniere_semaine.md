Salut,

Voici le compte rendu d'aujourd'hui, avec le travail à fournir individuellement + tout ce qu'il faut faire en commun (à la fin, section "à se répartir").
Concernant le rapport : ne rédiger pas directement dessus écrivez vos paragraphes ailleurs et ne pushez qu'après demande des autres membres du groupes. Attention : TOUTES LES FIGURES DU RAPPORT SONT ACTUELLEMENT FAUSSES, les diagrammes mis à jours ne sont que dans les fichiers .md qui contiennent le code draw.io.

Je souhaiterais que la rédaction de vos parties du rapport soient rédigés et pushez pour samedi soir.

Bon courage !


Alix et Méline
Frontend :
- rendre l'axe des abscisses des graphiques de disponibilité plus lisible
- faire tester l'ergonomie de l'application
- afficher le score de la station (demander dans cahier des charges)
Rapport :
- rédiger une synthèse sur le fonctionnement du frontend (section 3.1.a Frontend du rapport)

Samuel :
Rapport
- rédiger le paragraphe "Classes liées au traitement des données liées aux stations"
- partie now dans get availability à justifier vis à vis des bonnes pratiques de test

Eliot
Base de données :
- mettre en place une copie afin de pouvoir la fournir lors du rendu
- nettoyer le code SQL pour le rentre le plus "simple" possible en utilisant les méthodes du Template
Rapport :
- rédiger un paragraphe pour la section "Classes liées aux utilisateurs" sur l'implémentation gestion des administrateurs
- rédiger le paragraphe "Classes liées à la collecte de données liées aux stations" du rapport (+ créer le diagramme de classe en créant un nouveau fichier "diag_classes_collecte.md" et en respectant strictement le même template que ceux déjà créé)
- rédiger le paragraphe : "Gestion de la sécurité de l'application"
- Question : un admin peut supprimer un admin ?

Eddy :
Rapport
- revoir le rapport en entier
- ajouter une section "gestion des classes favorites"
- parler des bonnes pratiques (tests très rapprochés du code, test de la DAO sur fausse base de données avant la collecte pour vérifier les fonctionnalités, utilisation de l'IA)
- rajouter une partie sur les schéma/modèles
- revoir comment fonctionne les favoris : pourquoi body, etc.
- rajouter la justification du now de Samuel dans la partie test


À se répartir :
- Réécrire deux readME en anglais et proprement
- commenter toutes les classes et les méthodes, vérifier la cohérence (typage, présentation)
- revoir l'introduction du rapport
- écrire une conclusion au rapport
- faire les modifications demandées au rapport intermédiaire par retour de mail
- revoir les cas d'utilisation du rapport ainsi que le diagramme d'activité, à mettre à jour
- incorporer des images de l'appli ? peut-être en annexe ?
- revoir la description des endpoints, vérifier leur cohérence
- justifier dans le rapport : pourquoi id_user: int et id_station en str
- nettoyer le code (supprimer les bouts de code inutile, commenter les parties difficiles en anglais, écrire la documentation de chaque classe, vérifier la documentation des méthodes ainsi que le typage)
- vérifier si on a mis assez de code erreur HTTP sur les fonctionnalités "basiques"
- afficher des messages claires lorsqu'on a une error HTTP, sur la page, plutôt que le code


Questions en suspens :
Tests :
- tester la DAO ?
- vérifier si on a fait assez de tests
- utiliser mypy ?

Sécurité :
- on garde le fait que streamlit nous déconnecte, ou on essaie la sécurité optimale ? (de toute façon il faudra en parler dans le rapport : on est "presque" prêt au cas où streamlit change son comportement)
Dans tous les cas, il faudrait voir comment c'est fait dans le Template (TP5 ?)

Est-ce qu'on utilise ces méthodes ? sinon à supprimer ?
UserController :
update_my_profil ne sert à rien ? à voir si le frontend l'implémente
UserService :
update_own_profile


rédiger les fiches personnelles