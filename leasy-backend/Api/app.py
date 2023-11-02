from flask import Flask, request, jsonify
import requests
import fuzzywuzzy.fuzz as fuzz
import os


app = Flask(__name__)

API_AUTH_TOKEN = os.environ.get('API_AUTH_TOKEN')

'''
Use and invoke this function to get the bearer token to use in the API.

headers = {
    "Accept": "application/json",
    "api-token": f'{API_AUTH_TOKEN}',
    "user-email": "everalso23@gmail.com"
  }

def get_auth_token(url, headers):
    token_auth_request= requests.get(url, headers=headers)
    print(token_auth_request.status_code)
    print(token_auth_request.json())
    with open ('token.txt', 'w') as f:
        f.write(token_auth_request.json()['auth_token'])
        print('token auth generated succesfully')'''


GET_AUTH_TOKEN_URL = os.environ.get('GET_AUTH_TOKEN_URL')

'''get_auth_token(GET_AUTH_TOKEN_URL, headers)'''

@app.route('/search_countries', methods=['GET'])
def buscar_paises():
    BEARER_TOKEN_OBTAINED = os.environ.get('BEARER_TOKEN_OBTAINED')
    API_URL = os.getenv('API_URL')
    HEADERS = {
        'Authorization': f'Bearer {BEARER_TOKEN_OBTAINED}',
         'Accept': "application/json"
    }
    print('--> URL API', API_URL)
    search_text = request.args.get('nombre_parcial')
    print('--> search_text', search_text)
    if not search_text:
        return jsonify({"error": "please enter a name for the country"}), 400

    try:
        # Consulta la API de Universal Tutorial para obtener la lista de países
        response = requests.get(f"{API_URL}/countries", headers=HEADERS)
        countries = response.json()

        matching_countries = []
        exact_match_regions = []

        for country in countries:
            similarity_ratio = fuzz.ratio(search_text.lower(), country['country_name'].lower())
            if similarity_ratio >= 80:
                matching_countries.append({
                    "nombre": country['country_name'],
                    "country_code": country['country_short_name'],
                    "phone_code": country['country_phone_code']
                })

            if search_text.lower() == country['country_name'].lower():
                # Si se encuentra una coincidencia exacta, busca las regiones de ese país
                response = requests.get(f"{API_URL}/states/{country['country_name']}", headers=HEADERS)
                regions = response.json()
                exact_match_regions = [{"region": region['state_name']} for region in regions]

        if matching_countries:
            return jsonify({"Countries": matching_countries})

        if exact_match_regions:
            return jsonify({"regions": exact_match_regions})

        return jsonify({"message": "No coincidence."}), 404

    except Exception as e:
        return jsonify({"error": f"Error looking countries and regions: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)