import requests

def obter_ultimos_concursos(qtd=25):
    url = "https://loteriascaixa-api.herokuapp.com/api/lotomania"
    concursos = []

    for i in range(qtd):
        response = requests.get(f"{url}/{i}")
        if response.status_code == 200:
            data = response.json()
            dezenas = data.get("dezenas", [])
            if dezenas:
                concursos.append([int(d) for d in dezenas])
    return concursos
