import requests
import streamlit as st

# Função para obter os últimos concursos
def obter_ultimos_resultados_lotomania(quantidade=50):
    url_ultimo = 'https://loteriascaixa-api.herokuapp.com/api/lotomania/latest'
    try:
        resposta = requests.get(url_ultimo)
        resposta.raise_for_status()
        ultimo_concurso = resposta.json()['concurso']
    except requests.exceptions.RequestException as e:
        st.error(f"Erro ao obter o último concurso: {e}")
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
                resultados.append({"concurso": numero, "dezenas": dezenas})
        except requests.exceptions.RequestException as e:
            st.warning(f"Erro ao obter o concurso {numero}: {e}")
            continue

    return resultados

# Carregar os concursos
concursos_completos = obter_ultimos_resultados_lotomania(50)

if concursos_completos:
    # Extraindo somente as dezenas para outras análises
    concursos = [c['dezenas'] for c in concursos_completos]

    # Concurso mais recente para mostrar na UI
    ultimo_concurso = concursos_completos[0]['concurso']

    st.title(f"Resultados Lotomania - Concurso {ultimo_concurso}")

    # Aqui você pode seguir usando concursos (listas de dezenas) normalmente
    # Exemplo: mostrar as dezenas do último concurso
    st.write(f"Dezenas do último concurso: {concursos[20]}")
else:
    st.error("❌ Não foi possível carregar concursos válidos. Verifique sua conexão ou tente novamente mais tarde.")
