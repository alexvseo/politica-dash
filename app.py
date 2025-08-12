
# app.py
# -----------------------------------------------
# Dashboard de Desempenho de Anúncios (Sintético)
# Feito com Streamlit + Plotly. 
# Dados simulados para uma campanha política no Ceará.
# -----------------------------------------------
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime

# -----------------------------
# Configuração básica do app
# -----------------------------
st.set_page_config(
    page_title="Dashboard de Anúncios - CE",
    page_icon="📊",
    layout="wide"
)

@st.cache_data
def carregar_dados(caminho: str) -> pd.DataFrame:
    """Carrega os dados CSV e aplica tipos corretos.
    Obs.: cache para acelerar recarregamentos.
    """
    df = pd.read_csv(caminho)
    df['data'] = pd.to_datetime(df['data'])
    # Garantir tipos
    for col in ['impressoes', 'cliques', 'leads']:
        df[col] = df[col].astype(int)
    df['gastos'] = df['gastos'].astype(float)
    return df

df = carregar_dados('dados_sinteticos_anuncios.csv')

# -----------------------------
# Sidebar - Filtros
# -----------------------------
st.sidebar.header("Filtros")
min_date, max_date = df['data'].min(), df['data'].max()
data_inicio, data_fim = st.sidebar.date_input(
    "Período",
    value=(min_date, max_date),
    min_value=min_date, max_value=max_date
)

# Lista de cidades e objetivos
cidades = sorted(df['cidade'].unique().tolist())
objetivos = sorted(df['objetivo'].unique().tolist())
criativos = sorted(df['criativo'].unique().tolist())

cidades_sel = st.sidebar.multiselect("Cidades", cidades, default=cidades)
objetivos_sel = st.sidebar.multiselect("Objetivos", objetivos, default=objetivos)
criativos_sel = st.sidebar.multiselect("Criativos", criativos, default=criativos)

# -----------------------------
# Aplicar filtros
# -----------------------------
mask = (
    (df['data'].dt.date >= data_inicio) &
    (df['data'].dt.date <= data_fim) &
    (df['cidade'].isin(cidades_sel)) &
    (df['objetivo'].isin(objetivos_sel)) &
    (df['criativo'].isin(criativos_sel))
)
dff = df.loc[mask].copy()

# -----------------------------
# KPIs (Cards)
# -----------------------------
total_gastos = dff['gastos'].sum()
total_impress = int(dff['impressoes'].sum())
total_cliques = int(dff['cliques'].sum())
total_leads = int(dff['leads'].sum())
ctr = (total_cliques / total_impress) * 100 if total_impress else 0.0
cpc = (total_gastos / total_cliques) if total_cliques else 0.0
cpl = (total_gastos / total_leads) if total_leads else 0.0

col1, col2, col3, col4, col5, col6 = st.columns(6)
col1.metric("Gastos (R$)", f"{total_gastos:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
col2.metric("Impressões", f"{total_impress:,}".replace(",", "."))
col3.metric("Cliques", f"{total_cliques:,}".replace(",", "."))
col4.metric("CTR (%)", f"{ctr:.2f}")
col5.metric("CPC (R$)", f"{cpc:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
col6.metric("Leads", f"{total_leads:,}".replace(",", "."))

# -----------------------------
# Gráfico 1: Série temporal de gastos e cliques
# -----------------------------
serie = dff.groupby('data', as_index=False).agg({'gastos':'sum','cliques':'sum','impressoes':'sum'})
fig_line = px.line(serie, x='data', y=['gastos','cliques'], markers=True,
                   labels={'value':'Valor','variable':'Métrica','data':'Data'},
                   title='Série temporal: Gastos vs Cliques')
st.plotly_chart(fig_line, use_container_width=True)

# -----------------------------
# Gráfico 2: Barras por cidade (CPC e CTR)
# -----------------------------
por_cidade = dff.groupby('cidade', as_index=False).agg({'gastos':'sum','cliques':'sum','impressoes':'sum','leads':'sum'})
por_cidade['CTR (%)'] = (por_cidade['cliques'] / por_cidade['impressoes'] * 100).replace([np.inf, -np.inf], 0).fillna(0)
por_cidade['CPC (R$)'] = (por_cidade['gastos'] / por_cidade['cliques']).replace([np.inf, -np.inf], 0).fillna(0)
fig_bar = px.bar(por_cidade.sort_values('gastos', ascending=False),
                 x='cidade', y='gastos', hover_data=['CTR (%)','CPC (R$)','leads'],
                 title='Gastos por Cidade (hover: CTR, CPC e Leads)',
                 labels={'cidade':'Cidade','gastos':'Gastos (R$)'})
st.plotly_chart(fig_bar, use_container_width=True)

# -----------------------------
# Gráfico 3: Pizza por objetivo (gastos)
# -----------------------------
por_obj = dff.groupby('objetivo', as_index=False)['gastos'].sum()
fig_pie = px.pie(por_obj, names='objetivo', values='gastos', title='Distribuição de Gastos por Objetivo')
st.plotly_chart(fig_pie, use_container_width=True)

# -----------------------------
# Gráfico 4 (extra): Dispersão CPC x CTR por criativo
# -----------------------------
por_cr = dff.groupby('criativo', as_index=False).agg({'gastos':'sum','cliques':'sum','impressoes':'sum','leads':'sum'})
por_cr['CTR (%)'] = (por_cr['cliques'] / por_cr['impressoes'] * 100).replace([np.inf, -np.inf], 0).fillna(0)
por_cr['CPC (R$)'] = (por_cr['gastos'] / por_cr['cliques']).replace([np.inf, -np.inf], 0).fillna(0)
fig_scatter = px.scatter(por_cr, x='CTR (%)', y='CPC (R$)', size='gastos', color='criativo',
                         hover_data=['leads'], title='CPC vs CTR por Criativo (tamanho = Gastos)')
st.plotly_chart(fig_scatter, use_container_width=True)

# -----------------------------
# Tabela detalhada
# -----------------------------
with st.expander("Ver tabela detalhada filtrada"):
    st.dataframe(dff.sort_values(['data','cidade','objetivo','criativo']))

# -----------------------------
# Rodapé
# -----------------------------
st.markdown("""
**Sobre os dados**: Este conjunto é **sintético**, gerado para fins acadêmicos, simulando
uma campanha de anúncios digitais em cidades do Ceará. Ajuste rótulos/valores conforme necessário.
""")
