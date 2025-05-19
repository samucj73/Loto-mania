from collections import Counter
import math

def is_prime(n):
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    return all(n % i != 0 for i in range(3, int(n**0.5)+1, 2))

def is_fibonacci(n):
    x1 = 5 * n * n + 4
    x2 = 5 * n * n - 4
    return math.isqrt(x1)**2 == x1 or math.isqrt(x2)**2 == x2

def analisar_concursos(concursos):
    total_concursos = len(concursos)
    todas_dezenas = [d for c in concursos for d in c]

    pares_med = sum(sum(1 for d in c if d % 2 == 0) for c in concursos) / total_concursos
    impares_med = sum(sum(1 for d in c if d % 2 != 0) for c in concursos) / total_concursos
    soma_media = sum(sum(c) for c in concursos) / total_concursos

    contagem = Counter(todas_dezenas)
    mais_freq = contagem.most_common(10)
    menos_freq = contagem.most_common()[-10:]
    porcentagem = {k: (v / total_concursos) * 5 for k, v in contagem.items()}  # média de 5 aparições por concurso

    # Estatísticas adicionais
    quadrantes = [range(0, 25), range(25, 50), range(50, 75), range(75, 100)]
    quadrante_medias = [sum(sum(1 for d in c if d in q) for c in concursos) / total_concursos for q in quadrantes]

    linhas = [range(i, i+10) for i in range(0, 100, 10)]
    linhas_medias = [sum(sum(1 for d in c if d in l) for c in concursos) / total_concursos for l in linhas]

    colunas = [list(range(0 + i, 100, 10)) for i in range(10)]
    colunas_medias = [sum(sum(1 for d in c if d in col) for c in concursos) / total_concursos for col in colunas]

    primos_med = sum(sum(1 for d in c if is_prime(d)) for c in concursos) / total_concursos
    fibonacci_med = sum(sum(1 for d in c if is_fibonacci(d)) for c in concursos) / total_concursos
    quadrados_med = sum(sum(1 for d in c if int(math.sqrt(d))**2 == d) for c in concursos) / total_concursos

    multiplos_3_med = sum(sum(1 for d in c if d % 3 == 0) for c in concursos) / total_concursos
    multiplos_5_med = sum(sum(1 for d in c if d % 5 == 0) for c in concursos) / total_concursos
    multiplos_10_med = sum(sum(1 for d in c if d % 10 == 0) for c in concursos) / total_concursos

    faixa_baixa = range(0, 34)
    faixa_media = range(34, 67)
    faixa_alta = range(67, 100)
    faixa_baixa_med = sum(sum(1 for d in c if d in faixa_baixa) for c in concursos) / total_concursos
    faixa_media_med = sum(sum(1 for d in c if d in faixa_media) for c in concursos) / total_concursos
    faixa_alta_med = sum(sum(1 for d in c if d in faixa_alta) for c in concursos) / total_concursos

    finais_med = [sum(sum(1 for d in c if d % 10 == f) for c in concursos) / total_concursos for f in range(10)]

    altos_med = sum(sum(1 for d in c if d >= 50) for c in concursos) / total_concursos
    baixos_med = sum(sum(1 for d in c if d < 50) for c in concursos) / total_concursos

    return {
        "total_concursos": total_concursos,
        "pares_med": pares_med,
        "ímpares_med": impares_med,
        "soma_media": soma_media,
        "mais_frequentes": mais_freq,
        "menos_frequentes": menos_freq,
        "porcentagem_aparicao": porcentagem,
        "frequencia": contagem,

        # Estatísticas novas:
        "quadrante_medias": quadrante_medias,
        "linhas_medias": linhas_medias,
        "colunas_medias": colunas_medias,
        "primos_med": primos_med,
        "fibonacci_med": fibonacci_med,
        "quadrados_perfeitos_med": quadrados_med,
        "multiplos_3_med": multiplos_3_med,
        "multiplos_5_med": multiplos_5_med,
        "multiplos_10_med": multiplos_10_med,
        "faixa_baixa_med": faixa_baixa_med,
        "faixa_media_med": faixa_media_med,
        "faixa_alta_med": faixa_alta_med,
        "finais_med": finais_med,
        "altos_med": altos_med,
        "baixos_med": baixos_med,
    }
