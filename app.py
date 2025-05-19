import streamlit as st
from api_lotomania import obter_ultimos_resultados_lotomania
from estatisticas_lotomania import analisar_concursos
from gerador_cartoes import gerar_cartoes
from conferidor import conferir_cartoes, calcular_retorno

st.set_page_config(page_title="Lotomania Inteligente", layout="wide")
st.title("🎯 Lotomania Inteligente")

with st.spinner("🔄 Carregando concursos..."):
    concursos = obter_ultimos_resultados_lotomania()

if not concursos:
    st.error("❌ Não foi possível carregar os concursos. Verifique sua conexão ou tente novamente mais tarde.")
else:
    estatisticas = analisar_concursos(concursos)

    st.subheader("📊 Estatísticas dos Últimos 25 Concursos")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total de Concursos", estatisticas["total_concursos"])
    col2.metric("Média Pares", f'{estatisticas["pares_med"]:.2f}')
    col3.metric("Média Ímpares", f'{estatisticas["ímpares_med"]:.2f}')
    st.metric("Média Soma das Dezenas", f'{estatisticas["soma_media"]:.2f}')

    st.write("### 🔝 Dezenas Mais Frequentes")
    st.write(estatisticas["mais_frequentes"])

    st.write("### 🔻 Dezenas Menos Frequentes")
    st.write(estatisticas["menos_frequentes"])

    st.write("### 📈 Porcentagem de Aparição das Dezenas")
    st.bar_chart(estatisticas["porcentagem_aparicao"])

    st.subheader("🎲 Gerador de Cartões Inteligentes")
    qtd_cartoes = st.slider("Quantidade de cartões a gerar", 1, 50, 10)
    if st.button("🔁 Gerar Cartões"):
        cartoes = gerar_cartoes(estatisticas, qtd_cartoes)
        st.write("### Cartões Gerados")
        for i, cartao in enumerate(cartoes, 1):
            st.write(f"Cartão {i}: {cartao}")

        if st.button("📊 Conferir Desempenho nos Últimos 25 Concursos"):
            resultados = conferir_cartoes(cartoes, concursos)
            custo, retorno, saldo = calcular_retorno(cartoes, concursos)

            acertos_totais = [max(r) for r in resultados]
            st.write("### Faixas de Acerto por Cartão (Melhor Resultado entre os 25 concursos)")
            for i, acertos in enumerate(acertos_totais, 1):
                st.write(f"Cartão {i}: {acertos} acertos")

            st.success(f"💰 Custo Total: R$ {custo:.2f}")
            st.success(f"🏆 Retorno Total: R$ {retorno:.2f}")
            saldo_str = f"+R$ {saldo:.2f}" if saldo >= 0 else f"-R$ {abs(saldo):.2f}"
            st.metric("📈 Saldo Final", saldo_str)
