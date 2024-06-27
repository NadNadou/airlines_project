**Projet de Suivi des Vols en Temps Réel
**
**Description**
Ce projet vise à suivre les vols en temps réel en utilisant les données fournies par l'API Lufthansa et les systèmes IoT des avions. L'architecture de l'application combine le traitement par lots et le traitement en streaming pour une gestion efficace et une visualisation interactive des données aéronautiques.

**Structure du Projet**
**Batch**
Ce dossier contient le code pour le traitement par lots des données provenant de l'API Lufthansa.

**airlines/ :** Contient les scripts spécifiques aux compagnies aériennes.
**test/ :** Contient les tests pour le traitement par lots.
**utils/ :** Contient des utilitaires utilisés dans le traitement par lots.
**app.py :** Script principal pour l'ingestion des données de l'API Lufthansa.
**dashboard.py :** Génère les tableaux de bord à partir des données ingérées.
**crontab :** Fichier de configuration pour automatiser l'exécution du traitement par lots.
**update_mongo.sh :** Script pour mettre à jour la base de données MongoDB avec les nouvelles données.
**Dockerfile :** Fichier pour créer une image Docker pour l'application batch.
**requirements.txt :** Liste des dépendances Python pour le traitement par lots.

**Streaming**
Ce dossier contient le code pour le traitement en streaming des données IoT des avions.

**Dash_app/ :** Contient le code pour l'application web Dash.
**Iot_Data_Producer/ :** Contient les scripts pour produire les données IoT des avions.
**kafka_consumer_to_mongodb/ :** Contient les scripts pour consommer les données IoT de Kafka et les stocker dans MongoDB.
**docker-compose.yml :** Fichier de configuration pour orchestrer les services Docker nécessaires au traitement en streaming.

**Prérequis**
Docker
Python 3.x
Kafka
MongoDB

**Installation**

Clonez le dépôt :
git clone <URL-du-dépôt>
cd <nom-du-dépôt>

Installez les dépendances pour le traitement par lots :
cd batch
pip install -r requirements.txt

Démarrez les services Docker pour le traitement en streaming :
cd ../streaming
docker-compose up

**Utilisation**

Traitement par lots : Exécutez le script d'ingestion des données :
cd batch
python app.py

Traitement en streaming : Démarrez les producteurs et consommateurs Kafka :
cd streaming/Iot_Data_Producer
python producer.py
cd ../kafka_consumer_to_mongodb
python consumer.py

Visualisation : Lancez l'application Dash :
cd streaming/Dash_app
python app.py

**Contribution**
Les contributions sont les bienvenues. Veuillez soumettre une pull request pour toute amélioration ou correction.

**Licence**
Ce projet est sous licence MIT. Veuillez consulter le fichier LICENSE pour plus de détails.
