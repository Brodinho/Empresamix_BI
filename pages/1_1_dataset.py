import streamlit as st
from src.utils.menu import show_menu
from src.services.api_service import carregar_dados_faturamento
import pandas as pd
import math

# Configuração inicial da página
st.set_page_config(
    page_title="Dataset",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Menu lateral
with st.sidebar:
    show_menu()

# CSS para estilizar a tabela com cores alternadas
st.markdown("""
<style>
    /* Estilo para linhas alternadas da tabela */
    .dataframe tbody tr:nth-child(odd) {
        background-color: #1E1E1E;
    }
    .dataframe tbody tr:nth-child(even) {
        background-color: #2D2D2D;
    }
    
    /* Estilo para o cabeçalho da tabela */
    .dataframe thead th {
        background-color: #0E1117;
        color: white;
        text-align: left;
        padding: 10px;
    }
    
    /* Estilo para células da tabela */
    .dataframe tbody td {
        padding: 10px;
    }
    
    /* Remove bordas entre células */
    .dataframe {
        border: none;
    }
    .dataframe td, .dataframe th {
        border: none;
    }
</style>
""", unsafe_allow_html=True)

def show_dataset():
    st.title("Dataset Completo")
    
    try:
        # Carregar dados
        df = carregar_dados_faturamento()
        
        if df is None or df.empty:
            st.error("Não foi possível carregar os dados. Por favor, tente novamente.")
            return
        
        # Verificar se a coluna 'data' existe
        if 'data' not in df.columns:
            st.error("Coluna 'data' não encontrada no dataset.")
            return
        
        # Extrair anos únicos para o filtro
        anos_disponiveis = sorted(df['data'].dt.year.unique())
        
        # Layout em colunas para os filtros
        col1, col2 = st.columns([2, 2])
        
        with col1:
            # Filtro de anos - Multiselect
            anos_selecionados = st.multiselect(
                "Selecione os anos:",
                anos_disponiveis,
                default=anos_disponiveis,
                key="anos_dataset"
            )
        
        with col2:
            # Filtro de texto - Search box
            texto_busca = st.text_input(
                "Buscar em todas as colunas:",
                placeholder="Digite o texto para buscar...",
                key="busca_dataset"
            )
        
        # Aplicar filtros
        if anos_selecionados:
            df_filtrado = df[df['data'].dt.year.isin(anos_selecionados)]
        else:
            df_filtrado = df.copy()
        
        # Aplicar filtro de texto se houver
        if texto_busca:
            df_str = df_filtrado.astype(str)
            mask = df_str.apply(lambda x: x.str.contains(texto_busca, case=False, na=False)).any(axis=1)
            df_filtrado = df_filtrado[mask]
        
        # Configurações de paginação
        total_registros = len(df_filtrado)
        
        # Layout em colunas para controles de paginação
        col1, col2, col3, col4 = st.columns([1.5, 1, 1, 1])
        
        with col1:
            # Slider para registros por página
            registros_por_pagina = st.slider(
                "Registros por página:",
                min_value=1,
                max_value=100,
                value=10,
                key="registros_por_pagina"
            )
        
        # Calcular número total de páginas
        total_paginas = math.ceil(total_registros / registros_por_pagina)
        
        with col2:
            # Input para navegação direta de página
            pagina_atual = st.number_input(
                "Ir para página:",
                min_value=1,
                max_value=total_paginas,
                value=1,
                key="pagina_atual"
            )
        
        with col3:
            # Mostrar total de registros
            st.markdown(f"**Total de registros:** {total_registros}")
        
        with col4:
            # Mostrar total de páginas
            st.markdown(f"**Total de páginas:** {total_paginas}")
        
        # Calcular índices para paginação
        inicio = (pagina_atual - 1) * registros_por_pagina
        fim = inicio + registros_por_pagina
        
        # Aplicar paginação
        df_paginado = df_filtrado.iloc[inicio:fim]
        
        # Exibir dataframe com estilo
        st.dataframe(
            df_paginado,
            use_container_width=True,
            height=600
        )
        
        # Mostrar informação da página atual
        st.markdown(f"Mostrando registros {inicio + 1} até {min(fim, total_registros)} de {total_registros}")
    
    except Exception as e:
        st.error(f"Erro ao carregar os dados: {str(e)}")
        st.exception(e)

if __name__ == "__main__":
    show_dataset()
