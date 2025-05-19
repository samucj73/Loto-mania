import streamlit as st
from api_lotomania import obter_ultimos_resultados_lotomania
from estatisticas_lotomania import analisar_concursos
from gerador_cartoes import gerar_cartoes
from conferidor import conferir_cartoes, calcular_retorno
from probabilidade import calcular_probabilidades

st.set_page_config(page_title="Lotomania Inteligente", layout="wide")

st.markdown("<h1 style='text-align: center;'>🎯 Lotomania Inteligente</h1>", unsafe_allow_html=True)

with st.spinner("🔄 Carregando concursos..."):
    concursos_completos = obter_ultimos_resultados_lotomania()

if not concursos_completos:
    st.error("❌ Não foi possível carregar os concursos. Verifique sua conexão ou tente novamente mais tarde.")
    st.stop()

# Extrair apenas as dezenas
concursos = [sorted([int(d) for d in c['dezenas']]) for c in concursos_completos]
ultimo_concurso = concursos_completos[0]["concurso"]
data_ultimo = concursos_completos[0]["data"]

# Estatísticas
estatisticas = analisar_concursos(concursos)
probabilidades = calcular_probabilidades(estatisticas)

# Abas principais
abas = st.tabs(["📊 Estatísticas", "📈 Probabilidades", "🎲 Gerador de Cartões", "📋 Conferência"])

# ------------------ ABA ESTATÍSTICAS ------------------
with abas[0]:
    st.markdown(f"<h3 style='text-align: center;'>📊 Estatísticas dos Últimos 25 Concursos</h3>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align: center;'>Último concurso: <strong>{ultimo_concurso}</strong> ({data_ultimo})</p>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    col1.metric("Total de Concursos", estatisticas["total_concursos"])
    col2.metric("Média Pares", f'{estatisticas["pares_med"]:.2f}')
    col3.metric("Média Ímpares", f'{estatisticas["ímpares_med"]:.2f}')
    st.metric("Média Soma das Dezenas", f'{estatisticas["soma_media"]:.2f}')

    st.subheader("🔝 Dezenas Mais Frequentes")
    st.write(estatisticas["mais_frequentes"])

    st.subheader("🔻 Dezenas Menos Frequentes")
    st.write(estatisticas["menos_frequentes"])

    st.subheader("📊 Porcentagem de Aparição das Dezenas")
    st.bar_chart(estatisticas["porcentagem_aparicao"])

# ------------------ ABA PROBABILIDADES ------------------
with abas[1]:
    st.markdown("<h3 style='text-align: center;'>📈 Análise de Probabilidades</h3>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Média Soma", f'{probabilidades["media_soma"]:.2f}')
    col2.metric("Média Pares", f'{probabilidades["media_pares"]:.2f}')
    col3.metric("Média Repetidas", f'{probabilidades["media_repetidas"]:.2f}')
    
    st.metric("Média Sequências", f'{probabilidades["media_sequencias"]:.2f}')
    
    st.subheader("🔝 Dezenas Prováveis (Mais Frequentes)")
    st.write(probabilidades["mais_frequentes"])

    st.subheader("🔻 Dezenas Improváveis (Menos Frequentes)")
    st.write(probabilidades["menos_frequentes"])

# ------------------ ABA GERADOR ------------------
with abas[2]:
    st.markdown("<h3 style='text-align: center;'>🎲 Gerador de Cartões Inteligentes</h3>", unsafe_allow_html=True)

    qtd_cartoes = st.slider("Quantidade de cartões a gerar", 1, 50, 10)
    if st.button("🔁 Gerar Cartões"):
        cartoes = gerar_cartoes(estatisticas, qtd_cartoes)
        st.success("Cartões gerados com sucesso!")
        
        st.write("### Cartões Gerados:")
        for i, cartao in enumerate(cartoes, 1):
            st.write(f"Cartão {i}: {cartao}")
        
        # Exportar para .txt
        conteudo_txt = "\n".join([", ".join(f"{d:02}" for d in cartao) for cartao in cartoes])
        st.download_button("📥 Baixar Cartões (.txt)", conteudo_txt, file_name="cartoes_lotomania.txt")

# ------------------ ABA CONFERIDOR ------------------
with abas[3]:
    st.markdown("<h3 style='text-align: center;'>📋 Conferência de Cartões</h3>", unsafe_allow_html=True)
    
    if 'cartoes' in locals():
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
    else:
        st.warning("⚠️ Gere os cartões primeiro na aba anterior.")

# ------------------ RODAPÉ ------------------
st.markdown("""<hr style="margin-top: 40px;"/>
<div style='text-align: center; font-size: 14px; color: gray;'>
    SAMUCJ TECHNOLOGY &nbsp;&nbsp;|&nbsp;&nbsp; <span style="font-size:16px;">© 2025</span>
</div>""", unsafe_allow_html=True)
