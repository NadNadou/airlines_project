import pytest
from utils.lufthansa import all_countries ,all_airports

def test_all_countries():


    # Appelez la fonction à tester
    result = all_countries()

    # Vérifiez que le résultat est une liste
    assert isinstance(result, list)

    # Vérifiez que chaque élément de la liste est un dictionnaire
    for country in result:
        assert isinstance(country, dict)

        # Vérifiez que chaque dictionnaire contient les clés 'country_code' et 'names'
        assert 'country_code' in country
        assert 'names' in country


def test_all_airports():

    # Appelez la fonction à tester
    result = all_airports()

    # Vérifiez que le résultat est une liste
    assert isinstance(result, list)

    # Vérifiez que chaque élément de la liste est un dictionnaire
    for airport in result:
        assert isinstance(airport, dict)

        # Vérifiez que chaque dictionnaire contient les clés nécessaires
        assert 'airport_name' in airport
        assert 'airport_code' in airport
        assert 'position' in airport
        assert 'city_code' in airport
        assert 'country_code' in airport
        assert 'location_type' in airport
        assert 'utc_offset' in airport
        assert 'time_zone_id' in airport

def test_all_cities():
    # Appel de la fonction à tester
    result = all_cities()

    # Vérification que le résultat est une liste
    assert isinstance(result, list)

    # Vérification que chaque élément de la liste est un dictionnaire
    for city in result:
        assert isinstance(city, dict)

        # Vérification que chaque dictionnaire contient les clés nécessaires
        assert 'city_code' in city
        assert 'country_code' in city
        assert 'name' in city

def test_all_airlines():
    # Appel de la fonction à tester
    result = all_airlines()

    # Vérification que le résultat est une liste
    assert isinstance(result, list)

    # Vérification que chaque élément de la liste est un dictionnaire
    for airline in result:
        assert isinstance(airline, dict)

        # Vérification que chaque dictionnaire contient les clés nécessaires
        assert 'airline_name' in airline
        assert 'airline_id' in airline
        assert 'airline_id_icao' in airline

def test_all_schedules():
    # Définir les paramètres pour la fonction à tester
    origin = 'FRA'
    destination = 'JFK'
    date = '2024-03-08'

    # Appel de la fonction à tester
    result = all_schedules(origin, destination, date)

    # Vérification que le résultat est une liste
    assert isinstance(result, list)

    # Vérification que chaque élément de la liste est un dictionnaire
    for schedule in result:
        assert isinstance(schedule, dict)

        # Vérification que chaque dictionnaire contient les clés nécessaires
        assert 'Departure' in schedule
        assert 'Arrival' in schedule
        assert 'FlightNumber' in schedule
       


# Exécutez les tests avec pytest
if __name__ == '__main__':
    pytest.main()
