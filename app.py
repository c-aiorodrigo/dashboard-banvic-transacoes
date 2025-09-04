import pandas as pd
import streamlit as st
import plotly.express as px

#criando uma pagina com os dados
st.set_page_config(
    page_title="Dashboard Análise de Transações", 
    page_icon="📊",
    layout="wide")

#carregando os dados
df = pd.read_csv("df_transacoes_merge.csv")

#Criando o layout do dashboard
st.sidebar.header("✔️Filtros")

#Filtro por mês
meses_disponiveis = sorted(df['mes'].unique())
meses_selecionados = st.sidebar.multiselect("Selecione o(s) Mes(es)", meses_disponiveis, default=meses_disponiveis)
df_filtrado = df[df['mes'].isin(meses_selecionados)]

#Calculando métricas principais
volume_total = df_filtrado['valor_transacao'].sum()                                    #volume total dos meses selecionados
volume_medio = df_filtrado['valor_transacao'].mean()                                    #volume médio dos meses selecionados
st.metric(label="Volume Total de Transações", value=f"R$ {volume_total:,.2f}")         #para mostrar o valor total
st.metric(label="Volume Médio de Transações", value=f"R$ {volume_medio:,.2f}")         #para mostrar o valor médio
volume_total_mes = df_filtrado.groupby('mes')['valor_transacao'].sum().reset_index()         #volume por mês
volume_medio_mes = df_filtrado.groupby('mes')['valor_transacao'].mean().reset_index()         #média por mês

fig_volume_mes = px.bar(volume_total_mes, x='mes', y='valor_transacao',                             
                        labels={"mes": "Mês", "valor_transacao": "Volume de Transações (R$)"})      #criando o grafico em barras
fig_volume_medio_mes = px.line(volume_medio_mes, x='mes', y='valor_transacao',                      
                                labels={"mes": "Mês", "valor_transacao": "Média de Transações (R$)"}) #criando o grafico em linha]

#criando duas colunas para os graficos
col1, col2 = st.columns(2)                                                                          
with col1:
    st.subheader("📈 Volume de Transações por Mês")
    st.plotly_chart(fig_volume_mes, use_container_width=True)
with col2:
    st.subheader("📉 Média de Transações por Mês")
    st.plotly_chart(fig_volume_medio_mes, use_container_width=True)

#Filtros por Dia da Semana
ordem_semana = ['Domingo', 'Segunda-feira', 'Terça-feira', 'Quarta-feira', 'Quinta-feira', 'Sexta-feira', 'Sábado']
df['dia_da_semana']= pd.Categorical(df['dia_da_semana'], categories=ordem_semana, ordered=True)
dias_disponiveis = df['dia_da_semana'].unique()
dias_selecionados = st.sidebar.multiselect("Selecione o(s) Dia(s) da Semana", dias_disponiveis, default=dias_disponiveis)
df_filtrado = df_filtrado[df_filtrado['dia_da_semana'].isin(dias_selecionados)]

#Calculando métricas principais por dia da semana
volume_total_dia = df_filtrado['valor_transacao'].sum()                    #volume total por dia da semana
volume_medio_dia = df_filtrado['valor_transacao'].mean()                   #volume medio por dia da semana
st.metric(label="Volume Total de Transações (Dia da Semana)", value=f"R$ {volume_total_dia:,.2f}")
st.metric(label="Volume Médio de Transações (Dia da Semana)", value=f"R$ {volume_medio_dia:,.2f}")
volume_total_dia_semana = df_filtrado.groupby('dia_da_semana')['valor_transacao'].sum().reset_index()   #volume total por dia da semana
volume_medio_dia_semana = df_filtrado.groupby('dia_da_semana')['valor_transacao'].mean().reset_index()  #volume medio por dia da semana

fig_volume_dia_semana = px.bar(volume_total_dia_semana, x='dia_da_semana', y='valor_transacao',
                               labels={"dia_da_semana": "Dia da Semana", "valor_transacao": "Volume de Transações (R$)"})
fig_volume_medio_dia_semana = px.line(volume_medio_dia_semana, x='dia_da_semana', y='valor_transacao',
                                      labels={"dia_da_semana": "Dia da Semana", "valor_transacao": "Média de Transações (R$)"})

#criando duas colunas para os graficos da semana
col3, col4 = st.columns(2)
with col3:
    st.subheader("📊 Volume de Transações por Dia da Semana")
    st.plotly_chart(fig_volume_dia_semana, use_container_width=True)
with col4:
    st.subheader("📉 Média de Transações por Dia da Semana")
    st.plotly_chart(fig_volume_medio_dia_semana, use_container_width=True)
