import requests

def obter_ultimos_concursos(qtd=25):
    url_base = "https://loteriascaixa-api.herokuapp.com/api/lotomania/"
    concursos = []

    ultimo_concurso = obter_ultimo_numero_concurso()
    if not ultimo_concurso:
        return concursos

    for numero in range(ultimo_concurso, ultimo_concurso - qtd, -1):
        try:
            response = requests.get(f"{url_base}{numero}")
            if response.status_code == 200:
                data = response.json()
                dezenas = data.get("dezenas", [])
                if dezenas and len(dezenas) == 20:
                    dezenas_formatadas = sorted([int(d.zfill(2)) for d in dezenas])
                    concursos.append(dezenas_formatadas)
            else:
                print(f"[HTTP {response.status_code}] Erro ao acessar concurso {numero}")
        except Exception as e:
            print(f"[Erro] Concurso {numero}: {e}")
    return concursos

def obter_ultimo_numero_concurso():
    try:
        response = requests.get("https://loteriascaixa-api.herokuapp.com/api/lotomania")
        if response.status_code == 200:
            data = response.json()
            return int(data.get("concurso", 0))
    except Exception as e:
        print(f"[Erro ao obter último concurso] {e}")
    return None
