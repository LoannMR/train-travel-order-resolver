from find_cities_model import make_prediction, extract_predicted_cities
from spell_checker import spell_check
from speech_recognition import start_voice_recognition
from tgv_stations_finder import find_fastest_paths, find_station_for_direction

if __name__ == '__main__':
    user_input = None
    while user_input == None:
        print("Welcome to trouver votre trajet le plus rapide.")

        while user_input not in ["1", "2"]:
            user_input = input("1: text, 2: speech Recognition \n")

        if user_input == "1":
            Sentence = input("Entree une phrase d'une ville A a une ville B: \n")

        if user_input == "2":
            Sentence = start_voice_recognition()
        
        print("Phrase entrée:", Sentence)

        corrected_sentence = spell_check(Sentence)
        print("Phrase corrigée: ", corrected_sentence)

        labels = make_prediction(corrected_sentence)
        print("Classification de chaque mot: ", labels)

        predicted_cities = extract_predicted_cities(corrected_sentence, labels)
        print("Villes trouvée(s):", predicted_cities)

        stations_from = find_station_for_direction(predicted_cities, direction='FROM', threshold=90)
        stations_to = find_station_for_direction(predicted_cities, direction='TO', threshold=90)
        print("Stations de départs trouvées: ", stations_from)
        print("Stations d'arrivées trouvées: ", stations_to)

        print("Meilleurs chemins trouvées:")
        try:
            for station_from in stations_from:
                for station_to in stations_to:
                    best_path, all_paths = find_fastest_paths([station_from], [station_to])
                    print(best_path)
        except:
            pass

        user_input = input("Voulez-vous effectuez une autre recherche ? 1: oui, 2: non / ")
        if user_input == "1":
            user_input = None