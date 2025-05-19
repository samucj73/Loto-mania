from collections import Counter

def eh_primo(n):
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

def analisar_concursos(concursos):
    total_concursos = len(concursos)
    todas_dezenas = [d for c in concursos for d in c]

    primos = {2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97}
    fibonacci = {0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89}
    quadrados = {i*i for i in range(10)}
    
    soma_total = 0
    pares_total = 0
    impares_total = 0
    primos_total = 0
    fibonacci_total = 0
    quadrados_total = 0
    altas_total = 0
    baixas_total = 0
    repetidas_total = 0
    sequencias_total = 0
    multiplos_5_total = 0
    multiplos_10_total = 0

    finais_count = Counter()
    linhas_count = [0] * 10
    colunas_count = [0] * 10
    quadrantes = [0] * 4

    for i, c in enumerate(concursos):
        soma_total += sum(c)
        pares_total += sum(1 for d in c if d % 2 == 0)
        impares_total += sum(1 for d in c if d % 2 != 0)
        primos_total += sum(1 for d in c if d in primos)
        fibonacci_total += sum(1 for d in c if d in fibonacci)
        quadrados_total += sum(1 for d in c if d in quadrados)
        altas_total += sum(1 for d in c if d > 49)
        baixas_total += sum(1 for d in c if d <= 49)
        multiplos_5_total += sum(1 for d in c if d % 5 == 0)
        multiplos_10_total += sum(1 for d in c if d % 10 == 0)

        if i > 0:
            repetidas_total += len(set(c) & set(concursos[i - 1]))

        c_sorted = sorted(c)
        seq_count = 0
        for j in range(len(c_sorted) - 1):
            if c_sorted[j] + 1 == c_sorted[j + 1]:
                seq_count += 1
        sequencias_total += seq_count

        for d in c:
            finais_count[str(d).zfill(2)[-1]] += 1
            linhas_count[d // 10] += 1
            colunas_count[d % 10] += 1
            if d <= 49 and d % 10 <= 4:
                quadrantes[0] += 1
            elif d <= 49:
                quadrantes[1] += 1
            elif d % 10 <= 4:
                quadrantes[2] += 1
            else:
                quadrantes[3] += 1

    contagem = Counter(todas_dezenas)
    mais_freq = contagem.most_common(10)
    menos_freq = contagem.most_common()[-10:]

    porcentagem = {k: (v / total_concursos) * 5 for k, v in contagem.items()}

    return {
        "total_concursos": total_concursos,
        "pares_med": pares_total / total_concursos,
        "ímpares_med": impares_total / total_concursos,
        "soma_media": soma_total / total_concursos,
        "media_primos": primos_total / total_concursos,
        "media_fibonacci": fibonacci_total / total_concursos,
        "media_quadrados": quadrados_total / total_concursos,
        "media_altas": altas_total / total_concursos,
        "media_baixas": baixas_total / total_concursos,
        "media_repetidas": repetidas_total / (total_concursos - 1) if total_concursos > 1 else 0,
        "media_sequencias": sequencias_total / total_concursos,
        "media_multiplos_5": multiplos_5_total / total_concursos,
        "media_multiplos_10": multiplos_10_total / total_concursos,
        "mais_frequentes": mais_freq,
        "menos_frequentes": menos_freq,
        "porcentagem_aparicao": porcentagem,
        "frequencia": contagem,
        "finais": dict(finais_count),
        "linhas": linhas_count,
        "colunas": colunas_count,
        "quadrantes": {
            "Q1 (00-49, col 0-4)": quadrantes[0],
            "Q2 (00-49, col 5-9)": quadrantes[1],
            "Q3 (50-99, col 0-4)": quadrantes[2],
            "Q4 (50-99, col 5-9)": quadrantes[3]
        }
    }
