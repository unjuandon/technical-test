from flask import Flask, request, jsonify
import requests
import fuzzywuzzy.fuzz as fuzz

app = Flask(__name__)

# URL de la API de Universal Tutorial
# API_URL = "https://www.universal-tutorial.com/api"
# HEADERS = {
#     "Authorization": "Bearer Your-API-Token-Here",  # Reemplaza con tu token de API
#     "Accept": "application/json"
# }

# API_AUTH_TOKEN="mEcC78R7ujOPMZ2dpyVy9C_esbdu6VUVFvAwVC2QQ2n3CC1el-EHyR1f7xnst8G3f3g"



# headers = {
#     "Accept": "application/json",
#     "api-token": f'{API_AUTH_TOKEN}',
#     "user-email": "everalso23@gmail.com"
#   }

# def get_auth_token(url, headers):
#     token_auth_request= requests.get(url, headers=headers)
#     print(token_auth_request.status_code)
#     print(token_auth_request.json())
#     with open ('token.txt', 'w') as f:
#         f.write(token_auth_request.json()['auth_token'])
#         print('token auth generated succesfully')

# get_auth_token('https://www.universal-tutorial.com/api/getaccesstoken', headers)

@app.route('/buscar_paises', methods=['GET'])
def buscar_paises():
    API_URL = "https://www.universal-tutorial.com/api"
    HEADERS = {
        'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjp7InVzZXJfZW1haWwiOiJldmVyYWxzbzIzQGdtYWlsLmNvbSIsImFwaV90b2tlbiI6Im1FY0M3OFI3dWpPUE1aMmRweVZ5OUNfZXNiZHU2VlVWRnZBd1ZDMlFRMm4zQ0MxZWwtRUh5UjFmN3huc3Q4RzNmM2cifSwiZXhwIjoxNjk5MDQyODQ4fQ.d3h7FjgDjnFFfduCXNQ8aHllf0wcMQcSuKjAVtOa2rg',
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
                    "codigo_pais": country['country_short_name'],
                    "codigo_telefonico": country['country_phone_code']
                })

            if search_text.lower() == country['country_name'].lower():
                # Si se encuentra una coincidencia exacta, busca las regiones de ese país
                response = requests.get(f"{API_URL}/states/{country['country_name']}", headers=HEADERS)
                regions = response.json()
                exact_match_regions = [{"region": region['state_name']} for region in regions]

        if matching_countries:
            return jsonify({"paises": matching_countries})

        if exact_match_regions:
            return jsonify({"regiones": exact_match_regions})

        return jsonify({"message": "No se encontraron coincidencias."}), 404

    except Exception as e:
        return jsonify({"error": f"Error al buscar países y regiones: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)