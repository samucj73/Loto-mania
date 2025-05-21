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

def cartao_valido(cartao, frequentes, soma_ideal=(850, 1250), quadrante_alvo=range(10, 16), repetidos=set()):
    try:
        frequentes_set = set(frequentes)
    except TypeError:
        print("Rejeitado: frequentes não iterável")
        return False

    if len(set(cartao) & frequentes_set) < 25:
        print("Rejeitado por frequência insuficiente:", len(set(cartao) & frequentes_set))
        return False

    soma = sum(cartao)
    if not soma_ideal[0] <= soma <= soma_ideal[1]:
        print("Rejeitado por soma fora do ideal:", soma)
        return False

    q = calcular_quadrantes(cartao)
    if any(qv not in quadrante_alvo for qv in q.values()):
        print("Rejeitado por quadrantes desequilibrados:", q)
        return False

    repetidas = len(set(cartao) & repetidos)
    if repetidas >= 30:
        print("Rejeitado por repetições:", repetidas)
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
        repetidas_recentes.update(c)  # últimas 5 para evitar repetições

    for i in range(n_simulacoes):
        cartao = sorted(random.sample(range(100), 50))
        if not cartao_valido(cartao, dezenas_frequentes, repetidos=repetidas_recentes):
            continue

        acertos = conferir_acertos(cartao, concursos)
        if any(filtro_min <= a <= filtro_max for a in acertos):
            print(f"Cartão {i+1} aprovado com acertos: {acertos}")
            elite.append(cartao)

    print(f"Total de cartões de elite gerados: {len(elite)}")
    return elite
