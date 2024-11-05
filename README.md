# LOG-680 : Modèle pour Oxygen-CS

Cette application Python surveille en continu un hub de capteurs et gère les actions du système CVC (Chauffage, Ventilation et Climatisation) en fonction des données des capteurs reçues.

Elle utilise `signalrcore` pour maintenir une connexion en temps réel avec le hub de capteurs et utilise `requests` pour envoyer des requêtes GET à un point de contrôle CVC distant.

Cette application utilise `pipenv`, un outil qui vise à rassembler le meilleur de tous les mondes de la gestion de paquets dans l'univers Python.

## Exigences

- Python 3.8+
- pipenv

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
- DATABASE_URL : L'URL de connexion à la base de données.

## Exécution du Programme

Après la configuration, vous pouvez démarrer le programme avec la commande suivante :

```bash
pipenv run start
```

## Journalisation

L'application enregistre des événements importants tels que l'ouverture/fermeture de la connexion et les événements d'erreur pour aider au dépannage.

## À Mettre en Œuvre

Il y a des espaces réservés dans le code pour envoyer des événements à une base de données et gérer les exceptions de requêtes. Ces sections doivent être complétées selon les exigences de votre application spécifique.

## Licence

MIT

## Contact

Pour plus d'informations, n'hésitez pas à contacter le propriétaire du dépôt.
