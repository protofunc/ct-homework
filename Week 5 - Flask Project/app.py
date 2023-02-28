from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route("/")
def home():
    return render_template('home.html')

@app.route('/ergast', methods=['GET', 'POST'])
def ergast():
    print(request.method)
    if request.method == 'POST':
        name = request.form.get('poke_name')
        print(name) # Show name that was typed in the terminal
        url = f'https://pokeapi.co/api/v2/pokemon/{name}'
        response = requests.get(url)
        if response.ok:
            poke = response.json()
            poke_data = []
            poke_dict = { 
                'name': poke['forms'][0]['name'],
                'ability': poke['abilities'][0]['ability']['name'],
                'base_experience': poke['base_experience'],
                'sprite URL': poke['sprites']['front_shiny'],
                'attack base_stat': poke['stats'][1]['base_stat'],
                'hp base_stat': poke['stats'][0]['base_stat'],
                'defense base_stat': poke['stats'][3]['base_stat']
            }
            poke_data.append(poke_dict)
            return render_template('ergast.html', poke_data=poke_data)
        else:
            error = 'Incorrect name.'
            return render_template('ergast.html', error=error)
    return render_template('ergast.html')