import pandas as pd
import networkx as nx
from fuzzywuzzy import fuzz

def create_graph(df):
    G = nx.from_pandas_edgelist(df,
                            source="start_station", 
                            target="end_station",
                            edge_attr='duration', # weights
                            create_using=nx.DiGraph(oriented=True, data=True))
    return G

def preload_fastest_paths(G):
    """
    Example: access the shortest path and its weight from node A to node B
    path_from_A_to_B = weighted_paths['A']['B']['path']
    weight_from_A_to_B = weighted_paths['A']['B']['duration']
    """
    # Johnson's algorithm to find all pairs shortest paths
    shortest_paths_johnson = nx.johnson(G, weight="duration")
    # Create a dictionary to store the paths with their weights
    weighted_paths = {}
    for source, targets in shortest_paths_johnson.items():
        weighted_paths[source] = {}
        for target, path in targets.items():
            weight = sum(G[path[i]][path[i + 1]]['duration'] for i in range(len(path) - 1))
            weighted_paths[source][target] = {'path': path, 'duration': weight}
    return weighted_paths

# preload graph and fastest paths
timetables_df = pd.read_csv('./data/timetables.csv', delimiter=',', encoding='utf8')
G = create_graph(timetables_df)
shortest_paths = preload_fastest_paths(G)

# Get unique stations available
start_stations_unique = timetables_df['start_station'].unique()
end_stations_unique = timetables_df['end_station'].unique()
all_stations = list(start_stations_unique) + list(end_stations_unique)
unique_stations = pd.unique(all_stations)

def find_fastest_paths(start_stations, end_stations):
    best_path = None
    shortest_duration = float('inf')
    all_paths_info = []

    for start in start_stations:
        for end in end_stations:
            if start in shortest_paths and end in shortest_paths[start]:
                duration = shortest_paths[start][end]['duration']
                
                path_info = {
                    "start": start,
                    "end": end,
                    "duration": duration,
                    "path": shortest_paths[start][end]['path']
                }
                all_paths_info.append(path_info)
                
                if duration < shortest_duration:
                    shortest_duration = duration
                    best_path = (start, end, duration)
    return best_path, all_paths_info

def find_similar_stations(city, stations, threshold=90):
    """
    Find stations similar to the given city name.

    Parameters:
        city (str): The city name to search for.
        stations (list): List of station names.
        threshold (int): Similarity threshold for fuzzy string matching.

    Returns:
        list: List of stations similar to the city name.
    """
    # Convert city name to lowercase
    city_lower = city.lower()

    # Find stations similar to the city
    similar_stations = [station for station in stations if fuzz.partial_ratio(city_lower, station.lower()) >= threshold]

    return similar_stations[:4] # return maximum of 4 stations (paris has 4 stations)

def generate_city_combinations(b_cities, i_cities):
    """
    Generate all possible combinations of cities
    """
    
    city_combinations = [[b_city] + i_cities for b_city in b_cities]
    return city_combinations

def find_station_for_direction(predicted_cities: dict[str, list], direction='TO', threshold=90):
    """
    Find a similar station for a given direction based on predicted cities.

    Args:
    - predicted_cities (dict): Dictionary containing predicted cities categorized by label.
    - direction (str): Direction ('TO' or 'FROM').
    - threshold (int): Similarity threshold for finding similar stations.

    Returns:
    - str: The found similar station, or None if no similar station is found.
    """
    
    # Concatenate B-TO and I-TO cities if they exist
    if direction == 'TO':
        city_combinations =  generate_city_combinations(predicted_cities.get('B-TO', []), predicted_cities.get('I-TO', []))
    else:
        city_combinations =  generate_city_combinations(predicted_cities.get('B-FROM', []), predicted_cities.get('I-FROM', []))
    
    print(city_combinations)
    for city_words in city_combinations:
        # Try different lengths of city names starting from the full city name
        for i in range(len(city_words), 0, -1):
            # Concatenate the first i words of the city name
            partial_city = ' '.join(city_words[:i])
            similar_station = find_similar_stations(partial_city, threshold=threshold, stations=unique_stations)
            if similar_station:
                return similar_station