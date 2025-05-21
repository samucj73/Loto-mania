import random

def calcular_quadrantes(dezenas):
    quadrantes = {
        'Q1': set(range(0, 25)),
        'Q2': set(range(25, 50)),
        'Q3': set(range(50, 75)),
        'Q4': set(range(75, 100))
    }
    distrib = {'Q1': 0, 'Q2': 0, 'Q3': 0, 'Q4': 0}
    for d in dezenas:
        for q in quadrantes:
            if d in quadrantes[q]:
                distrib[q] += 1
    return distrib

def cartao_valido(cartao, frequentes, soma_ideal=(850, 1250), quadrante_alvo=range(8, 18), repetidos=set()):
    try:
        frequentes_set = set(frequentes)
    except TypeError:
        return False

    # Frequência mínima mais flexível
    if len(set(cartao) & frequentes_set) < 15:
        return False
    # Soma ideal
    if not soma_ideal[0] <= sum(cartao) <= soma_ideal[1]:
        return False
    # Quadrantes mais amplos
    q = calcular_quadrantes(cartao)
    if any(qv not in quadrante_alvo for qv in q.values()):
        return False
    # Tolerância maior para repetição
    if len(set(cartao) & repetidos) >= 35:
        return False

    return True

def conferir_acertos(cartao, concursos):
    resultados = []
    for concurso in concursos:
        acertos = len(set(cartao) & set(concurso))
        resultados.append(acertos)
    return resultados

def gerar_cartoes_elite(concursos, estatisticas, n_simulacoes=1000, filtro_min=18, filtro_max=20):
    elite = []
    dezenas_frequentes = estatisticas['frequencia'][:60]  # Top 60 mais frequentes
    repetidas_recentes = set()
    for c in concursos[-5:]:
        repetidas_recentes.update(c)

    for _ in range(n_simulacoes):
        cartao = sorted(random.sample(range(100), 50))
        if not cartao_valido(cartao, dezenas_frequentes, repetidos=repetidas_recentes):
            continue

        acertos = conferir_acertos(cartao, concursos)
        if any(filtro_min <= a <= filtro_max for a in acertos):
            elite.append(cartao)

    return elite
