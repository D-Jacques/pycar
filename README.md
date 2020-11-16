# pycar
python-project-car
DUCROUX Jacques / ABABSA Nessim

Ce projet simule la création d'une application web pour une concession automobile.

Dans cette application :
	- Il y'a une création d'utilisateurs, cette création d'utilisateurs est réservée aux 	adminstrateurs.
	- La base de données du projet peut-être initialisée avec la commande flask init-db, un 		utilisateur admin sera crée à l'initialisation avec comme mot de passe admin
	- Les utilisateurs ont un role attribué lors de leur inscription: Administrateur, 		Mécanicien et vendeur
	- L'adminitrateur à accès a tout le site, il peut aussi créer des utilisateurs.
	- Les mécaniciens peuvent créer et éditer des fiches techniques pour les véhicules
	- Les vendeurs peuvent créer les véhicules a mettre en vente, modifier les véhicules mis 
	en vente et il peut les retirer.
	-Chaque utilisateur peut modifier son adresse mail et son mot de passe.

règles: 
	-Les mots de passes et les nom d'utilisateurs doivent faire au moins 4 caractères de 	 long.
	-Les mails doivent faire 10 caractères de long.
	-Les fiches techniques et les informations sur les véhicules (ajout, modification) ne 	  peuvent pas être vides.
	-Chaque nom d'utilisateurs et adresse mail doit rester unique.
