import requests

def obter_ultimos_concursos(qtd=25):
    url = "https://loteriascaixa-api.herokuapp.com/api/lotomania"
    concursos = []

    for i in range(qtd):
        try:
            response = requests.get(f"{url}/{i}")
            if response.status_code == 200:
                try:
                    data = response.json()
                    dezenas = data.get("dezenas", [])
                    if dezenas:
                        concursos.append([int(d) for d in dezenas])
                except ValueError:
                    print(f"[Erro JSON] Concurso {i} retornou conteúdo inválido.")
            else:
                print(f"[Erro HTTP] Concurso {i}: Status {response.status_code}")
        except requests.RequestException as e:
            print(f"[Erro de Conexão] Concurso {i}: {e}")
    
    return concursos
