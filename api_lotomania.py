import requests

def obter_ultimos_resultados_lotomania(quantidade=25):
    url_ultimo = 'https://loteriascaixa-api.herokuapp.com/api/lotomania/latest'
    try:
        resposta = requests.get(url_ultimo)
        resposta.raise_for_status()
        ultimo_concurso = resposta.json()['concurso']
    except requests.exceptions.RequestException as e:
        print(f"Erro ao obter o último concurso: {e}")
        return []

    resultados = []
    for numero in range(ultimo_concurso, ultimo_concurso - quantidade, -1):
        url = f'https://loteriascaixa-api.herokuapp.com/api/lotomania/{numero}'
        try:
            resposta = requests.get(url)
            resposta.raise_for_status()
            dados = resposta.json()
            dezenas = sorted([int(d) for d in dados.get("dezenas", [])])
            if len(dezenas) == 20:
                resultados.append(dezenas)
        except requests.exceptions.RequestException as e:
            print(f"Erro ao obter o concurso {numero}: {e}")
            continue

    return resultados
