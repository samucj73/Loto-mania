import requests
import streamlit as st

# Função para obter os últimos concursos
def obter_ultimos_resultados_lotomania(quantidade=25):
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
concursos_completos = obter_ultimos_resultados_lotomania(25)

if concursos_completos:
    # Extraindo somente as dezenas para outras análises
    concursos = [c['dezenas'] for c in concursos_completos]

    # Concurso mais recente
    ultimo_concurso = concursos_completos[0]['concurso']
    st.title(f"Resultados Lotomania - Concurso {ultimo_concurso}")

    # Mostrar dezenas do último concurso
    dezenas_ultimo = ", ".join(str(d).zfill(2) for d in concursos[0])
    st.write(f"🔹 **Dezenas do último concurso**: {dezenas_ultimo}")

    # Mostrar os 10 últimos concursos
    st.subheader("📅 Últimos 10 Concursos")
    for c in concursos_completos[:10]:
        numero = c['concurso']
        dezenas = ", ".join(str(d).zfill(2) for d in c['dezenas'])
        st.write(f"Concurso {numero}: {dezenas}")

else:
    st.error("❌ Não foi possível carregar concursos válidos. Verifique sua conexão ou tente novamente mais tarde.")
