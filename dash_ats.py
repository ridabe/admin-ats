from pymongo import MongoClient
import pandas as pd
from bson import ObjectId
import streamlit as st
import matplotlib.pyplot as plt

client = MongoClient(
    'mongodb+srv://recrud:recrud2023bne@recrudprd.b82su.mongodb.net/recrud?retryWrites=true&w=majority')

db = client['recrud']
collection_job_integration_candidate = db['job_integration_candidate']

job_integration = collection_job_integration_candidate.find({})

st.set_page_config(page_title='Dash ATS')
st.set_option('deprecation.showPyplotGlobalUse', False)

with st.container():
    st.sidebar.markdown("# Dash")
    st.markdown("# Dash")
    st.subheader('Dash para monitoramento do ATS')

with st.container():
    st.write('---')
    st.write('Resultado das integrações com LUGARH')
    df = pd.DataFrame(list(job_integration))
    df.drop(columns=['_id', 'uuid_integration', 'integration_name'], inplace=True)
    st.dataframe(df)
    num_rows = df.shape[0]
    # Exiba o número de linhas e o DataFrame no Streamlit
    st.write(f"Número de linhas retornadas: {num_rows}")
    st.write('---')

with st.container():
    tab1, tab2 = st.tabs(["Status Integração", "Tipos de Erros"])
    with tab1:
        # Conte o número de linhas com valores nulos e não nulos na coluna 'error_integration'
        null_count = df['error_integration'].isnull().sum()
        not_null_count = df['error_integration'].notnull().sum()

        # Crie um gráfico de pizza

        labels = ['Não Integrados', 'Integrados']
        sizes = [not_null_count, null_count]
        colors = ['lightcoral', 'lightblue']
        explode = (0.1, 0)  # explode 1st slice
        plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=140)
        plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        plt.title('Distribuição de Valores Integrados e Não Integrados')
        st.pyplot()
        st.write(f"Quantidade integrado: {null_count}")
        st.write(f"Quantidade nao integrado: {not_null_count}")

    with tab2:
        # Obter as categorias únicas do campo 'error_integration'
        categories = df['error_integration'].unique()

        # Definir cores para cada categoria única
        colors = plt.cm.tab10.colors[:len(categories)]  # Use uma paleta de cores padrão do Matplotlib

        # Mapear as categorias únicas para as cores correspondentes
        color_map = dict(zip(categories, colors))

        # Agrupar os dados pela coluna 'error_integration' e contar as ocorrências em cada grupo
        grouped = df['error_integration'].value_counts()

        # Criar um gráfico de barras
        ax = grouped.plot(kind='bar', color=[color_map.get(x, 'gray') for x in grouped.index])

        # Ajustar tamanho da fonte
        plt.title('Quantidade de ocorrências por tipo de erro')
        plt.xlabel('Erro de Integração')
        plt.ylabel('Quantidade de Ocorrências')

        # Exibir legenda das cores
        legend_labels = [plt.Rectangle((0, 0), 1, 1, color=color_map[label]) for label in color_map]
        plt.legend(legend_labels, color_map.keys(), loc='best')

        # Adicionar o texto com a quantidade acima de cada barra
        for i, v in enumerate(grouped):
            plt.text(i, v + 0.2, str(v), ha='center')
        # Remover ticks do eixo x
        plt.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)

        # Exibir o gráfico no Streamlit
        st.pyplot()
