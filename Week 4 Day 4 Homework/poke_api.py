import requests

def setPoke(poke_name):
    # Get url info
    url = f'https://pokeapi.co/api/v2/pokemon/{poke_name}'
    response = requests.get(url)
    if response.ok:
        poke = response.json()
        poke_data = { 
            'name': poke['forms'][0]['name'],
            'ability': poke['abilities'][0]['ability']['name'],
            'base_experience': poke['base_experience'],
            'sprite URL': poke['sprites']['front_shiny'],
            'attack base_stat': poke['stats'][1]['base_stat'],
            'hp base_stat': poke['stats'][0]['base_stat'],
            'defense base_stat': poke['stats'][3]['base_stat']
        }
    else:
        return 'Error.'
    return poke_data

def getPoke(a_dict):
    # Display pokemon 
    for k,v in a_dict.items():
        print(f'{k.title()}: {str(v).title()}')
    print()

# Test it bb
dict1 = setPoke('blastoise')
dict2 = setPoke('ditto')
dict3 = setPoke('charmander')
dict4 = setPoke('squirtle')
dict5 = setPoke('pikachu')
getPoke(dict1)
getPoke(dict2)
getPoke(dict3)
getPoke(dict4)
getPoke(dict5)