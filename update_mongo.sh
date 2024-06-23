#!/bin/bash

curl -X POST http://localhost:8000/references


# Liste des noms des aéroports
airports=("BIO" "PAR" "JFK" "LHR" "FRA" "AMS")

# Fonction pour générer une date de deux mois à partir d'aujourd'hui
generate_date() {
  date -d "+1 days" "+%Y-%m-%d"
}

# Générer et envoyer 5 requêtes POST avec des paires de villes aléatoires
for i in {1..5}; do
  # Sélectionner deux aéroports aléatoires
  origin=$(shuf -e "${airports[@]}" -n 1)
  destination=$(shuf -e "${airports[@]}" -n 1)

  # S'assurer que l'origine et la destination sont différentes
  while [ "$origin" == "$destination" ]; do
    destination=$(shuf -e "${airports[@]}" -n 1)
  done

  # Générer la date
  date=$(generate_date)

  # Envoyer la requête POST
  curl -X  POST "http://localhost:8000/schedule?origin=${origin}&destination=${destination}&date=${date}"
 
 done