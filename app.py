import streamlit as st
from api_lotomania import obter_ultimos_resultados_lotomania
from estatisticas_lotomania import analisar_concursos
from probabilidade import calcular_probabilidades
from gerador_cartoes import gerar_cartoes
from conferidor import conferir_cartoes, calcular_retorno
import io

st.set_page_config(page_title="Lotomania Inteligente", layout="wide")

# Função para centralizar títulos com markdown + html
def titulo_centralizado(texto, nivel=1):
    st.markdown(f"<h{nivel} style='text-align: center;'>{texto}</h{nivel}>", unsafe_allow_html=True)

# Rodapé personalizado
def rodape():
    rodape_html = """
    <div style="width:100%;text-align:center;color:gray;margin-top:50px;font-size:12px;">
        <p><b>SAMUCJ TECHNOLOGY</b> &nbsp;&nbsp;
        <img src="https://upload.wikimedia.org/wikipedia/commons/3/39/Corporate_Logo_2025.svg" alt="Corporate 2025" width="20" style="vertical-align: middle;"></p>
    </div>
    """
    st.markdown(rodape_html, unsafe_allow_html=True)

# Título principal
titulo_centralizado("🎯 Lotomania Inteligente", nivel=1)

with st.spinner("🔄 Carregando concursos..."):
    concursos_completos = obter_ultimos_resultados_lotomania(25)

# Verificação e limpeza dos dados
concursos = []
ultimo_concurso_num = None

if not concursos_completos:
    st.markdown(
        "<div style='text-align:center; color:red; font-size:18px;'>❌ Não foi possível obter os resultados dos concursos. Verifique sua conexão ou tente mais tarde.</div>",
        unsafe_allow_html=True
    )
    rodape()
    st.stop()

for i, c in enumerate(concursos_completos):
    if isinstance(c, list):
        try:
            dezenas_int = sorted(int(d) for d in c)
            concursos.append(dezenas_int)
        except Exception as e:
            st.warning(f"Erro ao processar item {i+1}: {e}")
    elif isinstance(c, dict) and "dezenas" in c:
        try:
            dezenas_int = sorted(int(d) for d in c["dezenas"])
            concursos.append(dezenas_int)
            if ultimo_concurso_num is None or c.get('concurso', 0) > ultimo_concurso_num:
                ultimo_concurso_num = c.get('concurso', 0)
        except Exception as e:
            st.warning(f"Erro ao processar concurso {c.get('concurso', '?')}: {e}")
    else:
        st.warning(f"Formato inesperado nos dados do concurso {i+1}: {c}")

if not concursos:
    st.markdown(
        "<div style='text-align:center; color:red; font-size:18px;'>⚠️ Nenhum concurso válido foi carregado. Verifique a API ou tente novamente mais tarde.</div>",
        unsafe_allow_html=True
    )
    rodape()
    st.stop()

# Exibe número do último concurso
titulo_centralizado(f"Último Concurso: {ultimo_concurso_num}", nivel=3)

# Estatísticas e probabilidades
estatisticas = analisar_concursos(concursos)
probabilidades = calcular_probabilidades(estatisticas)

# Abas principais
abas = st.tabs(["Estatísticas", "Probabilidades", "Gerador de Cartões", "Conferidor"])

with abas[0]:
    titulo_centralizado("📊 Estatísticas dos Últimos 25 Concursos", nivel=2)
    cols = st.columns(4)
    cols[0].metric("Total de Concursos", estatisticas["total_concursos"])
    cols[1].metric("Média de Pares", f'{estatisticas["pares_med"]:.2f}')
    cols[2].metric("Média de Ímpares", f'{estatisticas["ímpares_med"]:.2f}')
    cols[3].metric("Média Soma das Dezenas", f'{estatisticas["soma_media"]:.2f}')

    st.write("### 🔝 Dezenas Mais Frequentes")
    st.write(estatisticas["mais_frequentes"])

    st.write("### 🔻 Dezenas Menos Frequentes")
    st.write(estatisticas["menos_frequentes"])

    st.write("### 📈 Porcentagem de Aparição das Dezenas")
    st.bar_chart(estatisticas["porcentagem_aparicao"])

with abas[1]:
    titulo_centralizado("📈 Probabilidades Baseadas nas Estatísticas", nivel=2)
    st.write(f"Média Soma: **{probabilidades['media_soma']:.2f}**")
    st.write(f"Média Pares: **{probabilidades['media_pares']:.2f}**")
    st.write(f"Média de Repetidas: **{probabilidades['media_repetidas']:.2f}**")
    st.write(f"Média de Sequências: **{probabilidades['media_sequencias']:.2f}**")

    st.write("### 🔝 Mais Frequentes")
    st.write(probabilidades["mais_frequentes"])

    st.write("### 🔻 Menos Frequentes")
    st.write(probabilidades["menos_frequentes"])

    st.write("### 🔄 Balanceamento Altas/Baixas")
    st.write(f"Proporção de dezenas acima de 50: **{probabilidades['alta_baixa_balanceado']['media_altas']:.2f}**")

with abas[2]:
    titulo_centralizado("🎲 Gerador de Cartões Inteligentes", nivel=2)
    qtd_cartoes = st.slider("Quantidade de cartões a gerar", 1, 50, 10)
    gerar_btn = st.button("🔁 Gerar Cartões")
    if gerar_btn:
        cartoes = gerar_cartoes(estatisticas, qtd_cartoes)
        st.write(f"### {len(cartoes)} Cartões Gerados:")
        for i, cartao in enumerate(cartoes, 1):
            st.write(f"Cartão {i}: {cartao}")

        # Preparar download do TXT
        txt_buffer = io.StringIO()
        for i, cartao in enumerate(cartoes, 1):
            linha = f"Cartão {i}: " + ", ".join(str(d).zfill(2) for d in cartao)
            txt_buffer.write(linha + "\n")
        txt_data = txt_buffer.getvalue()
        st.download_button(
            label="📥 Download TXT dos Cartões",
            data=txt_data,
            file_name=f"cartoes_lotomania_{ultimo_concurso_num}.txt",
            mime="text/plain"
        )

with abas[3]:
    titulo_centralizado("🧾 Conferidor de Cartões", nivel=2)
    if 'cartoes' not in locals():
        st.info("Primeiro gere os cartões na aba 'Gerador de Cartões' para conferir o desempenho.")
    else:
        conferir_btn = st.button("📊 Conferir Desempenho nos Últimos 25 Concursos")
        if conferir_btn:
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

rodape()
