from collections import Counter

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

    return {
        "total_concursos": total_concursos,
        "pares_med": pares_med,
        "ímpares_med": impares_med,
        "soma_media": soma_media,
        "mais_frequentes": mais_freq,
        "menos_frequentes": menos_freq,
        "porcentagem_aparicao": porcentagem,
        "frequencia": contagem  # ← ESSA LINHA FOI ADICIONADA
    }
