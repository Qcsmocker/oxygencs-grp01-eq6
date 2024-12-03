# LOG-680 : Modèle pour Oxygen-CS

Cette application Python surveille en continu un hub de capteurs et gère les actions du système CVC (Chauffage, Ventilation et Climatisation) en fonction des données des capteurs reçues. Elle utilise `signalrcore` pour maintenir une connexion en temps réel avec le hub de capteurs et utilise `requests` pour envoyer des requêtes GET à un point de contrôle CVC distant. Cette application utilise `pipenv`, un outil qui vise à rassembler le meilleur de tous les mondes de la gestion de paquets dans l'univers Python.

Le déploiement de cette application est fait de manière automatique. En effet, nous avons automatisé le processus en déployant le projet sur un cluster Kurbenetes à chaque fois qu'un changement a été effectué dans le main. Nous expliquons ce processus en détail dans notre wiki au [lien suivant](https://github.com/Qcsmocker/oxygencs-grp01-eq6/wiki/Kubernetes#d%C3%A9ploiements-kubernetes).

## Exigences

- Python 3.8+
- pipenv
- Configuration des secrets sur GitHub: [lien vers notre wiki qui explique comment faire](https://github.com/Qcsmocker/oxygencs-grp01-eq6/wiki/Kubernetes#mise-en-place-des-configmaps-et-secrets-sur-kubernetes)

## Démarrage

Installez les dépendances du projet :

```bash
pipenv install
```

## Configuration

Vous devez configurer les variables suivantes dans la classe App :

- HOST : L'hôte du hub de capteurs et du système CVC.
- TOKEN : Le jeton pour l'authentification des requêtes.
- T_MAX : La température maximale autorisée.
- T_MIN : La température minimale autorisée.
- DB_USER : Le nom d'utilisateur de la base de données.
- DB_PASSWORD : Le mot de passe de notre utilisateur de la base de données.
- DB_HOST : L'adresse de notre base de données.
- DB_PORT : Le numéro de port de la connexion.
- DB_NAME : Le nom de notre espace sur la base de données.

## Exécution du Programme

Après la configuration, vous pouvez démarrer le programme avec la commande suivante :

```bash
docker build -t jfkfred/oxygencs . --progress=plain

docker run --rm -it --name oxygencs --env-file .env  jfkfred/oxygencs
```

## Journalisation

L'application enregistre des événements importants tels que l'ouverture/fermeture de la connexion et les événements d'erreur pour aider au dépannage.

## Licence

MIT

## Contact

Pour plus d'informations, n'hésitez pas à contacter le propriétaire du dépôt.
