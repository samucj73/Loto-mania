import random
from collections import Counter

def analisar_estatisticas_ocultas(concursos):
    total_concursos = len(concursos)
    todos_numeros = [num for concurso in concursos for num in concurso]

    contagem = Counter(todos_numeros)
    mais_frequentes = [num for num, _ in contagem.most_common(60)]
    menos_frequentes = [num for num, _ in contagem.most_common()[-30:]]

    finais = Counter(num % 10 for num in todos_numeros)
    multiplos_5 = [num for num in todos_numeros if num % 5 == 0]
    multiplos_10 = [num for num in todos_numeros if num % 10 == 0]

    quadrantes = {"Q1": 0, "Q2": 0, "Q3": 0, "Q4": 0}
    for num in todos_numeros:
        if 0 <= num <= 24:
            quadrantes["Q1"] += 1
        elif 25 <= num <= 49:
            quadrantes["Q2"] += 1
        elif 50 <= num <= 74:
            quadrantes["Q3"] += 1
        elif 75 <= num <= 99:
            quadrantes["Q4"] += 1

    return {
        "total_concursos": total_concursos,
        "mais_frequentes": mais_frequentes,
        "menos_frequentes": menos_frequentes,
        "finais": dict(finais),
        "multiplos_5": list(set(multiplos_5)),
        "multiplos_10": list(set(multiplos_10)),
        "quadrantes": quadrantes,
        "contagem": dict(contagem)
    }

def gerar_cartoes_ocultos(analise, quantidade=10):
    todos_numeros = list(range(100))
    mais_freq = set(analise["mais_frequentes"])
    mult_5 = set(analise["multiplos_5"])
    mult_10 = set(analise["multiplos_10"])

    cartoes = []
    tentativas = 0
    while len(cartoes) < quantidade and tentativas < 1500:
        cartao = sorted(random.sample(todos_numeros, 50))
        score = (
            len(mais_freq.intersection(cartao)) +
            len(mult_5.intersection(cartao)) +
            len(mult_10.intersection(cartao))
        )
        if score >= 30:
            if cartao not in cartoes:
                cartoes.append(cartao)
        tentativas += 1
    return cartoes

def gerar_cartoes_zerar(analise, quantidade=10):
    todos_numeros = list(range(100))
    mais_freq = set(analise["mais_frequentes"])
    mult_5 = set(analise["multiplos_5"])
    mult_10 = set(analise["multiplos_10"])

    cartoes = []
    tentativas = 0
    while len(cartoes) < quantidade and tentativas < 9100000:
        cartao = sorted(random.sample(todos_numeros, 50))
        score = (
            len(mais_freq.intersection(cartao)) +
            len(mult_5.intersection(cartao)) +
            len(mult_10.intersection(cartao))
        )
        if score <= 10:  # quanto menor o score, mais "zerado" o cartão está
            if cartao not in cartoes:
                cartoes.append(cartao)
        tentativas += 1
    return cartoes 
def gerar_cartoes_ocultos_com_modo(analise, quantidade=10, modo="normal"):
    if modo == "zerar":
        return gerar_cartoes_zerar(analise, quantidade)
    else:
        return gerar_cartoes_ocultos(analise, quantidade)
