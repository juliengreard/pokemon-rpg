Projet Pokemon RPG
==================

- Initialiser la base de données: docker compose run backend python app/init_db.py
- Pour lancer le backend: ./prod.sh
- Pour lancer le frontend: cd frontend/pokemon-ui && npm run dev

TODO
====

1- Features
-----------

- Finir status (frozen, paralized, etc)
- Charger équipe via yaml/json
- Permettre de changer le niveau d'un joueur
- Gérer l'action "location" (backend à mettre en place + API + front + database à peupler (pokeapi?) )
- Sauvegarde des équipes chargées
- Level-up des pokemons
- Gérer la notion de capture (taux de réussite)

2- Bugs
-------

- Images HS pour certains pokemons
- Certains pokemons ont pas le bon nom
- Description des attaques en anglais => voir si traduction existe, ou intégration LLM ?
- Type d'attaque Electrick sans icone

3- Refacto
----------

- DRY pokeapi
- DRY moves
- DRY initdb
- Gérer les accents

4- CPL
-------

- tests API
- tests front (Selenium ou autre)
- couverture de tests
- doc
- front dans un docker spécifique
- déployer en AWS
- mettre en place plan de migration de la base (à voir comment c'est fait dans SQLAlchemy)
- gestion des logs