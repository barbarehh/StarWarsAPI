import json

import requests

film_url = "https://swapi.tech/api/films"
star_wars = "star_wars.json"
try:
    with open(star_wars, "r") as j:
        data = json.load(j)
except (FileNotFoundError, json.decoder.JSONDecodeError):
    data = []

while True:
    print("1 - A New Hope\n2 - The empire Strikes Back"
          "\n3 - Return of the Jedi"
          "\n4 - The Phantom Menace"
          "\n5 - Attack of the Clones"
          "\n6 - Revenge of the Sith")
    enter_id = input("Enter film ID to get information about it "
                     "(in case of any other symbol(s) the program will close) : ")

    if not enter_id.isdigit() or int(enter_id) not in range(1, 7):
        break

    for movie in data:
        if movie["Id"] == enter_id:
            print("Title:", movie["Title"])
            print("Episode ID:", movie["Episode ID"])
            print("Opening Crawl:", movie["Opening Crawl"])
            print("Director(s):", movie["Director(s)"])
            print("Producer(s):", movie["Producer(s)"])
            print("Release Date:", movie["Release Date"])
            print("Characters:")
            for item in movie["Characters"]:
                print("    ", "•", item)
            print("Planets:")
            for item in movie["Planets"]:
                print("    ", "•", item)

            print("Species:")
            for item in movie["Species"]:
                print("    ", "•", item)
            break

    else:
        response = requests.get(url=f"{film_url}/{enter_id}")
        if response.status_code == 200:

            resp = response.json()
            title = resp["result"]["properties"]["title"]
            ep_id = resp["result"]["properties"]["episode_id"]
            op_crawl = resp["result"]["properties"]["opening_crawl"]
            director = resp["result"]["properties"]["director"]
            producer = resp["result"]["properties"]["producer"]
            rel_date = resp["result"]["properties"]["release_date"]
            characters = resp["result"]["properties"]["characters"]
            species = resp["result"]["properties"]["species"]

            characters_list = []
            for character_url in characters:
                response = requests.get(character_url)
                if response.status_code == 200:
                    characters_data = response.json()
                    characters_list.append(characters_data["result"]["properties"]["name"])
                else:
                    print(f"Error {response.status_code}")
            planets = resp["result"]["properties"]["planets"]

            planets_list = []
            for planets_url in planets:
                response = requests.get(planets_url)
                if response.status_code == 200:
                    planets_data = response.json()
                    planets_list.append(planets_data["result"]["properties"]["name"])
                else:
                    print(f"Error {response.status_code}")

            species_list = []
            for species_url in species:
                response = requests.get(species_url)
                if response.status_code == 200:
                    species_data = response.json()
                    species_list.append(species_data["result"]["properties"]["name"])
                else:
                    print(f"Error {response.status_code}")

            new_data = {
                "Id": enter_id,
                "Title": title,
                "Episode ID": ep_id,
                "Opening Crawl": op_crawl,
                "Director(s)": director,
                "Producer(s)": producer,
                "Release Date": rel_date,
                "Characters": characters_list,
                "Planets": planets_list,
                "Species": species_list
            }

            data.append(new_data)

            with open("star_wars.json", "w") as f:
                json.dump(data, f, indent=4, separators=(", ", ": "))

            print("Title:", title,
                  "\nEpisode ID:", ep_id,
                  "\nOpening Crawl:", op_crawl,
                  "\nDirector(s):", director,
                  "\nProducer(s):", producer,
                  "\nRelease Date:", rel_date)

            print("Characters:")
            for item in characters_list:
                print("    ", "•", item)

            print("Planets:")
            for item in planets_list:
                print("    ", "•", item)

            print("Species:")
            for item in species_list:
                print("    ", "•", item)

        else:
            print("Error", response.status_code)
            break
