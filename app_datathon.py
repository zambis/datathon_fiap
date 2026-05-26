import streamlit as st
import pandas as pd
from databricks import sql
import os

st.set_page_config(
    page_title="Passos Mágicos",
    layout="wide"
)

st.title("Passos Mágicos")

# Debug logs
import sys
st.write("🔧 Debug Mode ON")
st.write(f"Version Streamlit: {st.__version__}")

def get_databricks_connection():
    try:
        st.write("📍 Tentando conectar ao Databricks...")
        print("DEBUG: Iniciando conexão Databricks")

        conn = sql.connect(
            server_hostname=st.secrets["DATABRICKS_HOST"],
            http_path=st.secrets["DATABRICKS_HTTP_PATH"],
            personal_access_token=st.secrets["DATABRICKS_TOKEN"]
        )

        print("DEBUG: Conexão estabelecida!")
        st.write("✅ Conectado ao Databricks!")
        return conn
    except KeyError as e:
        msg = f"❌ Credencial faltando: {str(e)}"
        st.error(msg)
        print(f"DEBUG KeyError: {e}")
        return None
    except BaseException as e:
        import traceback
        tb = traceback.format_exc()
        msg = f"❌ Erro ao conectar: {type(e).__name__}: {str(e)}"
        st.error(msg)
        st.write(f"```\n{tb}\n```")
        print(f"DEBUG Exception: {tb}")
        return None

def load_data():
    conn = None
    try:
        print("DEBUG: Iniciando load_data")
        st.write("📍 Carregando dados...")

        conn = get_databricks_connection()
        if not conn:
            print("DEBUG: Conexão retornou None")
            return None

        print("DEBUG: Executando query SQL...")
        st.write("📍 Executando query SQL...")

        df = pd.read_sql("SELECT * FROM pos_fiap.datathon.modelo_passos_magicos", conn)

        print(f"DEBUG: Query executada com sucesso! {len(df)} linhas")
        st.write(f"✅ Dados carregados! ({len(df)} linhas)")
        return df
    except BaseException as e:
        import traceback
        tb = traceback.format_exc()
        print(f"DEBUG: Erro em load_data: {tb}")
        st.error(f"❌ Erro ao carregar dados: {type(e).__name__}")
        st.write(f"```\n{tb}\n```")
        return None
    finally:
        if conn:
            try:
                conn.close()
            except:
                pass

print("DEBUG: Iniciando app")

with st.spinner("⏳ Carregando dados..."):
    print("DEBUG: Dentro do spinner")
    df = load_data()

print(f"DEBUG: df recebido, tipo: {type(df)}")

if df is None:
    st.error("❌ Falhou ao carregar dados. Verifique os logs acima.")
    st.stop()

st.markdown("---")

col1, col2, col3, col4, col5, col6 = st.columns(6)

with col1:
    filtro_id = st.text_input("ID", placeholder="Digite o ID")

with col2:
    idade_min, idade_max = int(df['Idade'].min()), int(df['Idade'].max())
    if 'Idade' in df.columns:
        filtro_idade = st.slider("Idade", idade_min, idade_max, value=(idade_min, idade_max))
    else:
        filtro_idade = None

with col3:
    if 'Ano' in df.columns:
        ano_unique = sorted(df['Ano'].dropna().unique())
        filtro_ano = st.multiselect("Ano", options=ano_unique)

with col4:
    if 'Fase' in df.columns:
        fase_unique = sorted(df['Fase'].dropna().unique())
        filtro_fase = st.multiselect("Fase", options=fase_unique)

with col5:
    if 'Genero' in df.columns:
        genero_unique = sorted(df['Genero'].dropna().unique())
        filtro_genero = st.multiselect("Gênero", options=genero_unique)

with col6:
    if 'Pedra' in df.columns:
        pedra_unique = sorted(df['Pedra'].dropna().unique())
        filtro_pedra = st.multiselect("Pedra", options=pedra_unique)

col1, col2, col3, col4, col5, col6 = st.columns(6)

with col1:
    if 'Ian_defasagem' in df.columns:
        ian_unique = sorted(df['Ian_defasagem'].dropna().unique())
        filtro_ian = st.multiselect("IAN Defasagem", options=ian_unique)

with col2:
    if 'Defasagem' in df.columns:
        defasagem_unique = sorted(df['Defasagem'].dropna().unique())
        filtro_defasagem = st.multiselect("Defasagem", options=defasagem_unique)

with col3:
    if 'IDA' in df.columns:
        filtro_ida = st.slider("IDA", min_value=0.0, max_value=10.0, value=(0.0, 10.0))
    else:
        filtro_ida = None

with col4:
    if 'IPP' in df.columns:
        filtro_ipp = st.slider("IPP", min_value=0.0, max_value=10.0, value=(0.0, 10.0))
    else:
        filtro_ipp = None

with col5:
    if 'INDE' in df.columns:
        filtro_inde = st.slider("INDE", min_value=0.0, max_value=10.0, value=(0.0, 10.0))
    else:
        filtro_inde = None

with col6:
    if 'Probabilidade_Defasagem' in df.columns:
        filtro_prob = st.slider("Probabilidade Defasagem", min_value=0.0, max_value=1.0, value=(0.0, 1.0))
    else:
        filtro_prob = None

df_filtrado = df.copy()

if filtro_id:
    df_filtrado = df_filtrado[df_filtrado['ID'].astype(str) == filtro_id]

if filtro_idade and 'Idade' in df_filtrado.columns:
    df_filtrado = df_filtrado[
        (df_filtrado['Idade'] >= filtro_idade[0]) &
        (df_filtrado['Idade'] <= filtro_idade[1])
    ]

if filtro_ano and 'Ano' in df_filtrado.columns:
    df_filtrado = df_filtrado[df_filtrado['Ano'].isin(filtro_ano)]

if filtro_fase and 'Fase' in df_filtrado.columns:
    df_filtrado = df_filtrado[df_filtrado['Fase'].isin(filtro_fase)]

if filtro_genero and 'Genero' in df_filtrado.columns:
    df_filtrado = df_filtrado[df_filtrado['Genero'].isin(filtro_genero)]

if filtro_pedra and 'Pedra' in df_filtrado.columns:
    df_filtrado = df_filtrado[df_filtrado['Pedra'].isin(filtro_pedra)]

if filtro_defasagem and 'Defasagem' in df_filtrado.columns:
    df_filtrado = df_filtrado[df_filtrado['Defasagem'].isin(filtro_defasagem)]

if filtro_ida and filtro_ida != (0.0, 10.0) and 'IDA' in df_filtrado.columns:
    df_filtrado = df_filtrado[
        (df_filtrado['IDA'] >= filtro_ida[0]) &
        (df_filtrado['IDA'] <= filtro_ida[1])
    ]

if filtro_ipp and filtro_ipp != (0.0, 10.0) and 'IPP' in df_filtrado.columns:
    df_filtrado = df_filtrado[
        (df_filtrado['IPP'] >= filtro_ipp[0]) &
        (df_filtrado['IPP'] <= filtro_ipp[1])
    ]

if filtro_inde and filtro_inde != (0.0, 10.0) and 'INDE' in df_filtrado.columns:
    df_filtrado = df_filtrado[
        (df_filtrado['INDE'] >= filtro_inde[0]) &
        (df_filtrado['INDE'] <= filtro_inde[1])
    ]

if filtro_ian and 'Ian_defasagem' in df_filtrado.columns:
    df_filtrado = df_filtrado[df_filtrado['Ian_defasagem'].isin(filtro_ian)]

if filtro_prob and filtro_prob != (0.0, 1.0) and 'Probabilidade_Defasagem' in df_filtrado.columns:
    df_filtrado = df_filtrado[
        (df_filtrado['Probabilidade_Defasagem'] >= filtro_prob[0]) &
        (df_filtrado['Probabilidade_Defasagem'] <= filtro_prob[1])
    ]

if 'ID' in df_filtrado.columns:
    df_filtrado = df_filtrado.sort_values('ID').reset_index(drop=True)

st.markdown("---")

st.subheader(f"📋 Resultados ({len(df_filtrado)} registros)")

st.dataframe(df_filtrado, use_container_width=True, height=400)

st.markdown("---")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric("Total", len(df_filtrado))

with col2:
    if 'Idade' in df_filtrado.columns:
        idade_media = df_filtrado['Idade'].mean()
        st.metric("Idade Média", f"{idade_media:.1f}")
    else:
        st.metric("Idade Média", "N/A")

with col3:
    if 'IDA' in df_filtrado.columns:
        ida_media = df_filtrado['IDA'].mean()
        st.metric("IDA Médio", f"{ida_media:.2f}")
    else:
        st.metric("IDA Médio", "N/A")

with col4:
    if 'INDE' in df_filtrado.columns:
        inde_media = df_filtrado['INDE'].mean()
        st.metric("INDE Médio", f"{inde_media:.2f}")
    else:
        st.metric("INDE Médio", "N/A")

with col5:
    if 'Probabilidade_Defasagem' in df_filtrado.columns:
        prob_media = df_filtrado['Probabilidade_Defasagem'].mean()
        st.metric("Prob. Média", f"{prob_media:.1%}")
    else:
        st.metric("Prob. Média", "N/A")

st.markdown("---")

csv = df_filtrado.to_csv(index=False)
st.download_button(
    label="📥 Baixar como CSV",
    data=csv,
    file_name="dados.csv",
    mime="text/csv"
)