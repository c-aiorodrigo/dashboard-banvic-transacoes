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
df['data_transacao'] = pd.to_datetime(df['data_transacao'])
df['apenas_data'] = df['data_transacao'].dt.date           #separando a data da hora

#criando o layout do dashboard
st.sidebar.header("✔️Filtros")

#filtro por mes
meses_disponiveis = sorted(df['mes'].unique())
meses_selecionados = st.sidebar.multiselect("Selecione o(s) Mes(es)", meses_disponiveis, default=meses_disponiveis)
df_filtrado = df[df['mes'].isin(meses_selecionados)]

#calculando numeros por mes
numero_total = df_filtrado['valor_transacao'].count()                                       #numero total dos meses selecionados

df_transacoes_mensais = df_filtrado.groupby(['mes', 'apenas_data']).count().reset_index()
df_transacoes_mensais.rename(columns={'valor_transacao': 'transacoes_mensais'}, inplace=True)
df_numero_medio_mes = df_transacoes_mensais.groupby('mes')['transacoes_mensais'].mean().reset_index(name='media_mes_transacoes')
if not df_numero_medio_mes.empty:
    if len(df_numero_medio_mes) > 1:
        numero_medio_mes = df_numero_medio_mes['media_mes_transacoes'].mean()
    else:
        numero_medio_mes = df_numero_medio_mes                                              #numero medio dos meses selecionados   

#calculando volume por mes
volume_total = df_filtrado['valor_transacao'].sum()                                         #volume total dos meses selecionados
volume_medio = df_filtrado['valor_transacao'].mean()                                        #volume medio dos meses selecionados

#criando as colunas para mostrar as metricas do mes
c1, c2= st.columns(2)                                                              
with c1:
    st.metric(label="Número Total de Transações", value=f"{numero_total:,}")                #para mostrar o numero total
with c2:
    st.metric(label="Número Médio de Transações", value=f"{numero_medio_mes:.2f}")          #para mostrar o numero medio    
c3, c4= st.columns(2)                                                              
with c3:
    st.metric(label="Volume Total de Transações", value=f"R$ {volume_total:,.2f}")          #para mostrar o valor total
with c4:
    st.metric(label="Volume Médio de Transações", value=f"R$ {volume_medio:,.2f}")          #para mostrar o valor medio
numero_total_mes = df_filtrado.groupby('mes')['valor_transacao'].count().reset_index()            #numero total por mes
numero_medio_mes = df_filtrado.groupby('mes')['valor_transacao'].mean().reset_index()             #numero medio por mes    
volume_total_mes = df_filtrado.groupby('mes')['valor_transacao'].sum().reset_index()              #volume por mes
volume_medio_mes = df_filtrado.groupby('mes')['valor_transacao'].mean().reset_index()             #media por mes

#criando os graficos do mes
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
df_filtrado_dia = df_filtrado[df_filtrado['dia_da_semana'].isin(dias_selecionados)]

#calculando numeros por dia da semana
numero_total_dia = df_filtrado_dia['valor_transacao'].count()                       #numero total por dia da semana

numero_total_dia = df_filtrado_dia['valor_transacao'].count()
df_transacoes_diarias = df_filtrado_dia.groupby(['dia_da_semana', 'apenas_data']).count().reset_index()
df_transacoes_diarias.rename(columns={'valor_transacao': 'transacoes_diarias_count'}, inplace=True)
df_numero_medio_dia = df_transacoes_diarias.groupby('dia_da_semana')['transacoes_diarias_count'].mean().reset_index(name='media_dia_transacoes')
if not df_numero_medio_dia.empty:
    if len(df_numero_medio_dia) > 1:
        numero_medio_dia = df_numero_medio_dia['media_dia_transacoes'].mean()
    else:
        numero_medio_dia = df_numero_medio_dia                                      #numero medio por dia da semana

#calculando volume por dia da semana
volume_total_dia = df_filtrado_dia['valor_transacao'].sum()                         #volume total por dia da semana

volume_medio_dia = df_filtrado_dia['valor_transacao'].mean()                        #volume medio por dia da semana


#criando as colunas para mostrar as metricas do dia da semana
c5, c6= st.columns(2)                                                           
with c5:
    st.metric(label="Número Total de Transações (Dia da Semana)", value=f"{numero_total_dia:,}")
with c6:
    st.metric(label="Número Médio de Transações (Dia da Semana)", value=f"{numero_medio_dia:.2f}")
c7, c8= st.columns(2)                                                           #criando colunas
with c7:
    st.metric(label="Volume Total de Transações (Dia da Semana)", value=f"R$ {volume_total_dia:,.2f}")
with c8:
    st.metric(label="Volume Médio de Transações (Dia da Semana)", value=f"R$ {volume_medio_dia:,.2f}")
numero_total_dia_semana = df_filtrado_dia.groupby('dia_da_semana')['valor_transacao'].count().reset_index() #numero total por dia da semana
numero_medio_dia_semana = df_filtrado_dia.groupby('dia_da_semana')['valor_transacao'].mean().reset_index()  #numero medio por dia da semana
volume_total_dia_semana = df_filtrado_dia.groupby('dia_da_semana')['valor_transacao'].sum().reset_index()   #volume total por dia da semana
volume_medio_dia_semana = df_filtrado_dia.groupby('dia_da_semana')['valor_transacao'].mean().reset_index()  #volume medio por dia da semana

#criando os graficos do dia da semana
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
    st.plotly_chart(fig_volume_medio_dia_semana, use_container_width=True) #para atualizar o commit
