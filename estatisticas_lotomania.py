from collections import Counter

def analisar_concursos(concursos):
    todas_dezenas = [d for c in concursos for d in c]
    frequencia = Counter(todas_dezenas)

    pares_med = sum([sum(1 for d in c if d % 2 == 0) for c in concursos]) / len(concursos)
    somas = [sum(c) for c in concursos]
    repetidas = []
    sequencias = []

    for i in range(1, len(concursos)):
        anteriores = set(concursos[i-1])
        atuais = set(concursos[i])
        repetidas.append(len(atuais & anteriores))

        max_seq = 1
        seq = 1
        ordenado = sorted(atuais)
        for j in range(1, len(ordenado)):
            if ordenado[j] == ordenado[j-1] + 1:
                seq += 1
                max_seq = max(max_seq, seq)
            else:
                seq = 1
        sequencias.append(max_seq)

    return {
        "frequencia": frequencia,
        "pares_med": pares_med,
        "somas": somas,
        "repetidas": repetidas,
        "sequencias": sequencias
    }
