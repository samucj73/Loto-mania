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

def calcular_faixa_soma_ideal(concursos):
    somas = [sum(concurso) for concurso in concursos]
    media = sum(somas) / len(somas)
    desvio = (sum((x - media) ** 2 for x in somas) / len(somas)) ** 0.5
    faixa_min = int(media - desvio)
    faixa_max = int(media + desvio)
    return (faixa_min, faixa_max)

def cartao_valido(cartao, frequentes, soma_ideal=(850, 1250), quadrante_alvo=range(10, 16), repetidos=set()):
    # Garante que 'frequentes' é iterável e converte para set
    try:
        frequentes_set = set(frequentes)
    except TypeError:
        return False

    if len(set(cartao) & frequentes_set) < 25:
        return False
    if not soma_ideal[0] <= sum(cartao) <= soma_ideal[1]:
        return False
    q = calcular_quadrantes(cartao)
    if any(qv not in quadrante_alvo for qv in q.values()):
        return False
    if len(set(cartao) & repetidos) >= 30:
        return False
    return True

def conferir_acertos(cartao, concursos):
    resultados = []
    for concurso in concursos:
        acertos = len(set(cartao) & set(concurso))
        resultados.append(acertos)
    return resultados

def gerar_cartoes_elite(concursos, estatisticas, n_simulacoes=1000, filtro_min=16, filtro_max=20):
    elite = []
    dezenas_frequentes = estatisticas['frequencia'][:60]  # Top 60 mais frequentes
    repetidas_recentes = set()
    for c in concursos[-5:]:
        repetidas_recentes.update(c)

    soma_ideal = calcular_faixa_soma_ideal(concursos)

    for _ in range(n_simulacoes):
        cartao = sorted(random.sample(range(100), 50))
        if not cartao_valido(cartao, dezenas_frequentes, soma_ideal=soma_ideal, repetidos=repetidas_recentes):
            continue

        acertos = conferir_acertos(cartao, concursos)
        if any(filtro_min <= a <= filtro_max for a in acertos):
            elite.append(cartao)

    return elite
