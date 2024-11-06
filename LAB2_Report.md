# Rapport de Laboratoire 2

## 1. Introduction

Ce deuxième laboratoire du cours LOG680 - Introduction à l'approche DevOps vise à approfondir notre maîtrise des pratiques DevOps en intégrant un pipeline d'intégration continue (CI) et la conteneurisation avec
Docker pour l'application Oxygène CS. Dans le cadre de ce projet, nous avons configuré un pipeline CI pour automatiser les tests et le déploiement, ainsi que des variables d'environnement pour rendre l'application
plus flexible et adaptable. De plus, l’ajout d’une base de données permet de sauvegarder les données critiques des capteurs et des événements HVAC, tandis que les métriques CI fournissent un suivi détaillé de la
performance et de la stabilité du pipeline. Ces actions renforcent notre compréhension de l’importance d’un environnement collaboratif et automatisé, essentiel pour un développement structuré et efficace.


## 2. Environnement GitHub (10 points)
- **Utilisation de Kanban et des outils de gestion** : Pour ce laboratoire, nous avons organisé nos tâches en utilisant un tableau Kanban sur GitHub, structuré en différentes colonnes : **Backlog**, **Ready**,
  **In Progress**, **In Review**, et **Done**. Cette organisation a permis une gestion claire des tâches, facilitant le suivi des éléments en cours et ceux déjà complétés (voir **Figure 1. Tableau Kanban pour le projet OxygenCS**).

  - **Backlog** : Les tâches initiales qui n'ont pas encore été démarrées, servant de réservoir pour les fonctionnalités à implémenter.
  - **Ready** : Les éléments prêts à être pris en charge par l'équipe, mais encore non assignés.
  - **In Progress** : Les tâches actuellement en cours d'exécution, incluant la mise en place du pipeline CI et la création de documentation pour le pipeline.
  - **In Review** : Les tâches terminées, mais en attente de validation, comme les tests d'intégration et unitaires pour l'application OxygenCS.
  - **Done** : Les tâches finalisées, comprenant des éléments tels que la création des Dockerfiles pour OxygenCS et Metrics, l'intégration des variables d'environnement, et la configuration du dépôt GitHub et de DockerHub pour l'équipe.

  Cette organisation du Kanban nous a permis de maintenir un flux de travail structuré, de prioriser efficacement les tâches, et de coordonner le travail entre les membres de l'équipe. Chaque tâche est marquée par un libellé descriptif
  (par exemple, `[Feature]`, `[Product Management]`) pour indiquer son type et faciliter le suivi des éléments de développement, de configuration, et de documentation.

<div align="center">
    <img src="https://github.com/user-attachments/assets/d0c2ec66-8066-4df6-9a2c-1bef2b5fde44" alt="Tableau Kanban pour le projet OxygenCS">
    <p><strong>Figure 1. Tableau Kanban pour le projet OxygenCS</strong></p>
</div>


## 3. Oxygen CS (20 points)

### 3.1 Modifications du code source
- **Variables d'environnement** (5 points) : Afin de rendre l'application **Oxygène CS** plus flexible et adaptable, nous avons introduit des variables d'environnement qui permettent de configurer dynamiquement certains paramètres
  sans modifier directement le code source. Ce fichier `.env` est essentiel pour isoler les configurations sensibles et faciliter le déploiement de l'application sur différents environnements. Voici le fichier `.env` utilisé dans ce projet :

  ```env
  HOST=http://159.203.50.162
  TOKEN=2a03e74e83693a665460
  T_MAX=20
  T_MIN=5
  DATABASE_URL=postgres://user01eq6:z0AMEq4PW3pAe5qc@157.230.69.113/db01eq6
  PYTHONPATH=.
  ```


- **Base de données** (5 points) : Trois nouvelles tables ont été créées pour enregistrer les données de température des capteurs, les actions du système HVAC, et les métriques d'intégration continue (CI).

  - **Table `sensor_events`** : Cette table stocke les enregistrements de température capturés par les capteurs avec un horodatage, permettant ainsi de suivre l'évolution de la température dans le système en temps réel
    (voir **Figure 2** ci-dessous).

  <div align="center">
      <img src="https://github.com/user-attachments/assets/f81b2e3e-f81b-49b7-8c82-1880aa485989", width="600">
      <p><strong>Figure 2. Table sensor_events avec les données de température</strong></p>
  </div>

  - **Table `hvac_actions`** : Cette table enregistre les actions du système HVAC, telles que l'activation du chauffage ou de la climatisation, avec des informations comme l'horodatage, le type d'action, la température, et des détails
    supplémentaires (voir **Figure 3** ci-dessous).

  <div align="center">
      <img src="https://github.com/user-attachments/assets/f2f85e00-a898-4e6f-ae13-081e92a29a56" alt="Table hvac_actions avec les enregistrements d'actions",width="600">
      <p><strong>Figure 3. Table hvac_actions avec les enregistrements d'actions</strong></p>
  </div>

  - **Table `ci_snapshot`** : Cette table enregistre les métriques CI, telles que le temps d'exécution des builds, le temps moyen des builds, le nombre de builds, et les builds échoués. Ces informations permettent d'analyser la performance des processus CI (voir **Figure 4** ci-dessous).

  <div align="center">
      <img src="path/to/ci_snapshot_image.png" alt="Table ci_snapshot avec les métriques CI" width="600">
      <p><strong>Figure 4. Table ci_snapshot avec les métriques CI</strong></p>
  </div>

- **Gestion des connexions** : Un curseur de base de données est utilisé pour exécuter les requêtes d'insertion de manière efficace. En cas d'erreur, un message d'erreur est affiché pour faciliter le débogage et maintenir l'intégrité des données.

  Ces tables permettent de capturer et de stocker les informations critiques liées aux capteurs de température, aux actions du système HVAC, et aux métriques d'intégration continue, facilitant l’analyse et le suivi des événements dans un environnement DevOps.


### 3.2 Tests
- **Tests unitaires** (5 points) : Décrire les tests unitaires écrits pour OxygenCS, les méthodes testées, et les résultats attendus.

- **Tests d'intégration** (5 points) : Les tests d'intégration pour **OxygenCS** vérifient l'insertion correcte des actions HVAC et des événements de capteur dans la base de données, assurant ainsi le bon fonctionnement global de l'application.

  - **Test d'insertion de données de capteur** : Ce test ajoute un événement de capteur avec une température spécifique dans la table `sensor_events` et vérifie l'insertion en recherchant l'horodatage et la température exacts dans la base de données (voir **Figure 5**).

    <div align="center">
        <img src="https://github.com/user-attachments/assets/6c1487a5-5953-45d4-928f-d732b8433c76" alt="Test d'insertion de données de capteur" width="600">
        <p><strong>Figure 5. Test d'insertion de données de capteur</strong></p>
    </div>

  - **Test d'insertion d'une action HVAC** : Ce test insère une action HVAC (par exemple, `TurnOnHeater`) dans la table `hvac_actions`, avec le champ `response_details` contenant la mention `"Integration Test"` pour l'identifier. Après l'insertion, une vérification confirme
    que l'action a été ajoutée avec succès (voir **Figure 6**).

    <div align="center">
        <img src="https://github.com/user-attachments/assets/ec966a25-c679-441f-a612-f078191b39d7" alt="Test d'insertion d'une action HVAC" width="800">
        <p><strong>Figure 6. Test d'insertion d'une action HVAC</strong></p>
    </div>



Ces tests garantissent que les enregistrements pour les actions HVAC et les événements de capteur sont correctement insérés, renforçant ainsi la fiabilité de l'application dans un cadre DevOps.

## 4. Intégration Continue (30 points)

- **Pre-commit Git Hook** (10 points) : Le hook pre-commit est configuré pour assurer la qualité du code en exécutant des outils de linting, de formatage, et de tests d'intégration avant chaque commit.

  - **Linting et formatage** : Le hook utilise `Pylint` pour l'analyse statique du code et `Black` pour le formatage, garantissant un code uniforme et sans erreurs. Ces outils sont exécutés localement avec `pre-commit`, configurés avec Python 3.11. `Pylint` inclut les dépendances nécessaires et utilise `PYTHONPATH` pour accéder aux modules locaux.

  - **Tests d'intégration** : Un hook `pre-commit` exécute également les tests d'intégration via `pytest` dans le dossier `tests/integration_tests`, garantissant que les modifications n'introduisent pas de régressions. Les résultats des hooks (voir **Figure 7** ci-dessous) montrent que tous les contrôles passent avant le commit.

  <div align="center">
      <img src="https://github.com/user-attachments/assets/57800dbd-34f9-49fd-8013-e3277130f1b7" alt="Exécution des hooks pre-commit" width="600">
      <p><strong>Figure 7. Exécution des hooks pre-commit</strong></p>
  </div>

  - **GitHub Actions** : Pour une intégration continue complète, un workflow GitHub Actions est configuré pour exécuter les tests, construire et publier l'image Docker sur Docker Hub. Ce workflow se déclenche automatiquement sur chaque `push` vers la branche `main` et peut également être déclenché manuellement.

    - **Étapes du workflow** :
      1. **Tests** : La première étape du workflow exécute les tests unitaires pour s'assurer de la stabilité du code.
      2. **Build et publication** : Si les tests réussissent, le workflow passe à l'étape de build et publication de l'image Docker. L'image est construite, taguée avec le dernier SHA du commit, et publiée sur Docker Hub avec les tags `latest` et `${{ github.sha }}`.

    Les étapes du workflow sont illustrées dans **Figure 9** ci-dessous.

    <div align="center">
        <img src="https://github.com/user-attachments/assets/10078a88-d184-455f-a974-c82f131a081d" alt="Workflow GitHub Actions pour le build et la publication" width="400">
        <p><strong>Figure 9. Workflow GitHub Actions pour le build et la publication</strong></p>
    </div>

Ce système de hooks et de workflows CI/CD renforce la qualité et la stabilité du code, en empêchant l'ajout de modifications non conformes ou de régressions.

- **Création d'images Docker** :
  - **Metrics** (5 points) : Expliquer le processus de création de l'image Docker pour l'application Metrics et sa mise en ligne sur DockerHub.
  - **HVAC (OxygenCS)** (5 points) : Décrire la création de l'image Docker pour OxygenCS et son déploiement.
- **Pipeline CI pour DockerHub** :
  - **Pipeline Metrics** (5 points) : Expliquer les étapes du pipeline CI pour Metrics (Build, Test, et déploiement sur DockerHub).
  - **Pipeline HVAC** (5 points) : Décrire les étapes du pipeline CI pour l'application HVAC (OxygenCS) de la même manière.

## 5. Métriques DevOps (10 points)
- **Métriques CI** : Décrire les quatre métriques sélectionnées pour le suivi de l'intégration continue, telles que le temps d'exécution des builds, le taux de réussite des tests, etc. Justifier le choix de chaque métrique et expliquer comment elles sont intégrées dans l'application Metrics.


## 7. Conclusion
Ce laboratoire nous a permis de mettre en œuvre des pratiques avancées de DevOps en automatisant le pipeline CI et en utilisant Docker pour standardiser les environnements, contribuant ainsi à la fiabilité et à l'efficacité
de l'application Oxygène CS. Les métriques CI offrent un suivi précis de la performance des builds et des tests, facilitant une identification rapide des problèmes et assurant la qualité du code. L’intégration de ces outils
et processus pose les bases pour une gestion de projet optimisée et ouvre la voie à de futures améliorations dans notre approche DevOps.
