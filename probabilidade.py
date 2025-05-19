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
        "frequencia": contagem
    }


def calcular_probabilidades(estatisticas):
    soma_media = estatisticas["soma_media"]
    pares_media = estatisticas["pares_med"]
    repetidas_media = estatisticas.get("repetidas_med", 0)
    sequencias_media = estatisticas.get("sequencias_med", 0)

    frequencia = estatisticas["frequencia"]
    todas_dezenas = list(frequencia.items())
    todas_dezenas.sort(key=lambda x: x[1], reverse=True)

    mais_frequentes = [d[0] for d in todas_dezenas[:30]]
    menos_frequentes = [d[0] for d in todas_dezenas[-30:]]

    altas = [d for d in frequencia if d > 50]
    media_altas = len(altas) / len(frequencia) if frequencia else 0

    return {
        "media_soma": soma_media,
        "media_pares": pares_media,
        "media_repetidas": repetidas_media,
        "media_sequencias": sequencias_media,
        "mais_frequentes": mais_frequentes,
        "menos_frequentes": menos_frequentes,
        "alta_baixa_balanceado": {"media_altas": media_altas}
    }
