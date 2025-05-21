import streamlit as st
st.set_page_config(page_title="Lotomania Inteligente", layout="wide")

from api_lotomania import obter_ultimos_resultados_lotomania
from estatisticas_lotomania import analisar_concursos
from probabilidade import calcular_probabilidades
from gerador_cartoes import gerar_cartoes
from conferidor import conferir_cartoes, calcular_retorno
from estatisticas_ocultas import analisar_estatisticas_ocultas, gerar_cartoes_ocultos_com_modo

import io

# Função para centralizar títulos com markdown + html
def titulo_centralizado(texto, nivel=1):
    st.markdown(f"<h{nivel} style='text-align: center;'>{texto}</h{nivel}>", unsafe_allow_html=True)

# Rodapé personalizado
def rodape():
    rodape_html = '''
    <div style="width:100%;text-align:center;color:gray;margin-top:50px;font-size:12px;">
        <p><b>SAMUCJ TECHNOLOGY</b> &nbsp;&nbsp;
        <img src="https://upload.wikimedia.org/wikipedia/commons/3/39/Corporate_Logo_2025.svg" alt="Corporate 2025" width="20" style="vertical-align: middle;"></p>
    </div>
    '''
    st.markdown(rodape_html, unsafe_allow_html=True)

# Título principal
titulo_centralizado("🎯 Lotomania Inteligente", nivel=1)

with st.spinner("🔄 Carregando concursos..."):
    concursos_completos = obter_ultimos_resultados_lotomania(25)

concursos = []
ultimo_concurso_num = None

for c in concursos_completos:
    if not isinstance(c, dict):
        st.warning(f"Item inesperado no resultado: {c} (não é dicionário)")
        continue

    dezenas = c.get('dezenas')
    if not dezenas or not isinstance(dezenas, list):
        st.warning(f"Concurso {c.get('concurso', '?')} está com dezenas inválidas: {dezenas}")
        continue

    try:
        dezenas_int = sorted(int(d) for d in dezenas)
        concursos.append(dezenas_int)
        if ultimo_concurso_num is None or c.get('concurso', 0) > ultimo_concurso_num:
            ultimo_concurso_num = c.get('concurso', 0)
    except Exception as e:
        st.error(f"Erro ao processar dezenas do concurso {c.get('concurso', '?')}: {e}")

if not concursos:
    st.error("❌ Não foi possível carregar concursos válidos.")
    rodape()
    st.stop()

titulo_centralizado(f"Último Concurso: {ultimo_concurso_num}", nivel=3)

# Exibir os 25 últimos concursos
with st.expander("📅 Ver os 25 últimos concursos"):
    for item in concursos_completos[:25]:
        numero = item['concurso']
        dezenas = ", ".join(str(d).zfill(2) for d in item['dezenas'])
        st.write(f"Concurso {numero}: {dezenas}")

estatisticas = analisar_concursos(concursos)
probabilidades = calcular_probabilidades(estatisticas)

if 'cartoes' not in st.session_state:
    st.session_state.cartoes = []

abas = st.tabs(["📊 Estatísticas", "📈 Probabilidades", "🎲 Gerador de Cartões", "📊 Estatísticas Ocultas", "🧾 Conferidor", "🗓️ Conferir Arquivo", "🌟 Cartões de Elite"])

# === ESTATÍSTICAS ===
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

    with st.expander("🔍 Análises Avançadas"):
        col1, col2, col3 = st.columns(3)
        col1.metric("Média de Primos", f"{estatisticas['media_primos']:.2f}")
        col2.metric("Média de Fibonacci", f"{estatisticas['media_fibonacci']:.2f}")
        col3.metric("Média de Quadrados", f"{estatisticas['media_quadrados']:.2f}")

        col4, col5, col6 = st.columns(3)
        col4.metric("Média de Altas (≥50)", f"{estatisticas['media_altas']:.2f}")
        col5.metric("Média de Baixas (<50)", f"{estatisticas['media_baixas']:.2f}")
        col6.metric("Média de Repetidas", f"{estatisticas['media_repetidas']:.2f}")

        col7, col8 = st.columns(2)
        col7.metric("Média Múltiplos de 5", f"{estatisticas['media_multiplos_5']:.2f}")
        col8.metric("Média Múltiplos de 10", f"{estatisticas['media_multiplos_10']:.2f}")

        st.metric("Média de Sequências Consecutivas", f"{estatisticas['media_sequencias']:.2f}")

    with st.expander("📦 Distribuição por Quadrantes e Volante"):
        st.write("#### Quadrantes (Q1–Q4)")
        st.bar_chart(estatisticas["quadrantes"])

        st.write("#### Linhas do Volante (0 a 9)")
        st.bar_chart(estatisticas["linhas"])

        st.write("#### Colunas do Volante (0 a 9)")
        st.bar_chart(estatisticas["colunas"])

    with st.expander("🔢 Frequência por Final (Terminação 0 a 9)"):
        finais_dict = {f"Final {k}": v for k, v in estatisticas["finais"].items()}
        st.bar_chart(finais_dict)

# === PROBABILIDADES ===
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

# === GERADOR DE CARTÕES ===
with abas[2]:
    titulo_centralizado("🎲 Gerador de Cartões Inteligentes", nivel=2)
    qtd_cartoes = st.slider("Quantidade de cartões a gerar", 1, 50, 10)
    gerar_btn = st.button("🔁 Gerar Cartões")
    if gerar_btn:
        st.session_state.cartoes = gerar_cartoes(estatisticas, qtd_cartoes)
        st.success(f"{len(st.session_state.cartoes)} cartões gerados com sucesso!")
    if st.session_state.cartoes:
        st.write(f"### {len(st.session_state.cartoes)} Cartões Gerados:")
        for i, cartao in enumerate(st.session_state.cartoes, 1):
            st.write(f"Cartão {i}: {cartao}")

        txt_buffer = io.StringIO()
        for i, cartao in enumerate(st.session_state.cartoes, 1):
            linha = f"Cartão {i}: " + ", ".join(str(d).zfill(2) for d in cartao)
            txt_buffer.write(linha + "\n")
        txt_data = txt_buffer.getvalue()
        st.download_button(
            label="📥 Download TXT dos Cartões",
            data=txt_data,
            file_name=f"cartoes_lotomania_{ultimo_concurso_num}.txt",
            mime="text/plain"
        )

# === ESTATÍSTICAS OCULTAS ===
# === ESTATÍSTICAS OCULTAS ===
with abas[3]:
    titulo_centralizado("📊 Estatísticas Ocultas e Geração de Cartões", nivel=2)

    estat_ocultas = analisar_estatisticas_ocultas(concursos)

    st.write("### 📈 Resultados das Estatísticas Ocultas")
    st.json(estat_ocultas)

    modo = st.selectbox("Modo de Geração", ["normal", "zerar"])

    qtd_cartoes_ocultos = st.slider("Quantidade de Cartões Ocultos a Gerar", 1, 20, 5)
    gerar_ocultos_btn = st.button("🧩 Gerar Cartões Ocultos")
    if gerar_ocultos_btn:
        cartoes_ocultos = gerar_cartoes_ocultos_com_modo(estat_ocultas, qtd_cartoes_ocultos, modo=modo)
        st.session_state.cartoes_ocultos = cartoes_ocultos
        st.success(f"{len(cartoes_ocultos)} cartões ocultos gerados com sucesso! (Modo: {modo})")

    if 'cartoes_ocultos' in st.session_state and st.session_state.cartoes_ocultos:
        st.write(f"### {len(st.session_state.cartoes_ocultos)} Cartões Ocultos Gerados (Modo: {modo}):")
        for i, cartao in enumerate(st.session_state.cartoes_ocultos, 1):
            st.write(f"Cartão Oculto {i}: {cartao}")

        txt_buffer = io.StringIO()
        for i, cartao in enumerate(st.session_state.cartoes_ocultos, 1):
            linha = f"Cartão Oculto {i}: " + ", ".join(str(d).zfill(2) for d in cartao)
            txt_buffer.write(linha + "\n")
        txt_data = txt_buffer.getvalue()
        st.download_button(
            label="📥 Download TXT dos Cartões Ocultos",
            data=txt_data,
            file_name=f"cartoes_ocultos_lotomania_{modo}_{ultimo_concurso_num}.txt",
            mime="text/plain"
        )
# === CONFERIDOR ===
with abas[4]:
    titulo_centralizado("🧾 Conferidor de Cartões", nivel=2)
    tem_cartoes_tradicionais = bool(st.session_state.get("cartoes"))
    tem_cartoes_ocultos = bool(st.session_state.get("cartoes_ocultos"))

    if not (tem_cartoes_tradicionais or tem_cartoes_ocultos):
        st.info("Primeiro gere os cartões em uma das abas disponíveis.")
    else:
        conferir_btn = st.button("📊 Conferir Desempenho nos Últimos 25 Concursos")
        if conferir_btn:
            if tem_cartoes_tradicionais:
                st.subheader("🎲 Cartões Tradicionais")
                resultados_t = conferir_cartoes(st.session_state.cartoes, concursos)
                custo_t, retorno_t, saldo_t = calcular_retorno(st.session_state.cartoes, concursos)

                acertos_totais_t = [max(r) for r in resultados_t]
                for i, acertos in enumerate(acertos_totais_t, 1):
                    st.write(f"Cartão {i}: {acertos} acertos")

                st.success(f"💰 Custo: R$ {custo_t:.2f}")
                st.success(f"🏆 Retorno: R$ {retorno_t:.2f}")
                st.metric("📈 Saldo", f"{retorno_t - custo_t:+.2f}".replace(".", ","))

            if tem_cartoes_ocultos:
                st.subheader("🔮 Cartões por Estatísticas Ocultas")
                resultados_o = conferir_cartoes(st.session_state.cartoes_ocultos, concursos)
                custo_o, retorno_o, saldo_o = calcular_retorno(st.session_state.cartoes_ocultos, concursos)

                acertos_totais_o = [max(r) for r in resultados_o]
                for i, acertos in enumerate(acertos_totais_o, 1):
                    st.write(f"Cartão {i}: {acertos} acertos")

                st.success(f"💰 Custo: R$ {custo_o:.2f}")
                st.success(f"🏆 Retorno: R$ {retorno_o:.2f}")
                st.metric("📈 Saldo", f"{retorno_o - custo_o:+.2f}".replace(".", ",")) 

 # Comferidor Arquivos
with abas[5]:
    titulo_centralizado("📂 Conferir Cartões do Arquivo (.txt)", nivel=2)

    arquivo = st.file_uploader("📤 Envie seu arquivo .TXT com os cartões (1 por linha, 50 dezenas separadas por vírgula):", type="txt")

    if arquivo is not None:
        linhas = arquivo.read().decode("utf-8").splitlines()
        cartoes_arquivo = []

        for linha in linhas:
            try:
                # Remove o prefixo tipo "Cartão 1:" se existir
                if ":" in linha:
                    linha = linha.split(":", 1)[1]
                dezenas = [int(x.strip()) for x in linha.split(",") if x.strip().isdigit()]
                if len(dezenas) == 50:
                    cartoes_arquivo.append(sorted(dezenas))
            except:
                continue

        if not cartoes_arquivo:
            st.error("❌ Nenhum cartão válido encontrado no arquivo.")
        else:
            st.success(f"✅ {len(cartoes_arquivo)} cartões lidos com sucesso.")

            ultimo_resultado = concursos[-1]  # Último concurso dos 25 carregados

            st.write(f"### 🗓️ Conferindo com o último concurso ({ultimo_concurso_num})")
            for i, cartao in enumerate(cartoes_arquivo, 1):
                acertos = len(set(cartao).intersection(set(ultimo_resultado)))
                st.write(f"Cartão {i}: {acertos} acertos")

            # Retorno financeiro com base no último concurso
            premios = {
                20: 500000,
                19: 25000,
                18: 1500,
                17: 200,
                16: 50,
                15: 10,
            }

            custo = len(cartoes_arquivo) * 3.0
            retorno = 0
            for cartao in cartoes_arquivo:
                acertos = len(set(cartao).intersection(set(ultimo_resultado)))
                retorno += premios.get(acertos, 0)

            saldo = retorno - custo
            st.success(f"💰 Custo Total: R$ {custo:.2f}")
            st.success(f"🏆 Retorno Total: R$ {retorno:.2f}")
            saldo_str = f"+R$ {saldo:.2f}" if saldo >= 0 else f"-R$ {abs(saldo):.2f}"
            st.metric("📈 Saldo Final", saldo_str)
            # === CARTÕES DE ELITE ===
with abas[6]:
    titulo_centralizado("🌟 Cartões de Elite - Análise e Seleção Avançada", nivel=2)

    qtd_simulacoes = st.slider("Quantidade de Simulações", 100, 5000, 1000, step=100)
    filtro_min = st.number_input("Mínimo de Acertos (Filtro)", min_value=15, max_value=20, value=18)
    filtro_max = st.number_input("Máximo de Acertos (Filtro)", min_value=15, max_value=20, value=20)

    gerar_elite_btn = st.button("🚀 Gerar Cartões de Elite")
    if gerar_elite_btn:
        with st.spinner("🔍 Processando simulações e aplicando filtros..."):
            from cartoes_elite import gerar_cartoes_elite

            cartoes_elite = gerar_cartoes_elite(
                concursos=concursos,
                estatisticas=estatisticas,
                n_simulacoes=qtd_simulacoes,
                filtro_min=filtro_min,
                filtro_max=filtro_max
            )
            st.session_state.cartoes_elite = cartoes_elite
            st.success(f"{len(cartoes_elite)} cartões de elite gerados!")

    if 'cartoes_elite' in st.session_state and st.session_state.cartoes_elite:
        st.write(f"### {len(st.session_state.cartoes_elite)} Cartões de Elite Selecionados:")
        for i, cartao in enumerate(st.session_state.cartoes_elite, 1):
            st.write(f"Cartão Elite {i}: {cartao}")

        txt_buffer = io.StringIO()
        for i, cartao in enumerate(st.session_state.cartoes_elite, 1):
            linha = f"Cartão Elite {i}: " + ", ".join(str(d).zfill(2) for d in cartao)
            txt_buffer.write(linha + "\n")
        txt_data = txt_buffer.getvalue()

        st.download_button(
            label="📥 Download TXT dos Cartões de Elite",
            data=txt_data,
            file_name=f"cartoes_elite_lotomania_{ultimo_concurso_num}.txt",
            mime="text/plain"
        )
# Rodapé
rodape()
