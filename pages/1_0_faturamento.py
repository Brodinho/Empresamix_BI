import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from src.services.api_service import carregar_dados_faturamento
from src.utils.theme_config import COLORS

def show_faturamento():
    st.title("Dashboard de Faturamento")
    
    # Carrega dados
    df = carregar_dados_faturamento()
    
    if df is not None:
        # Distribuição Geográfica
        st.subheader("Distribuição Geográfica do Faturamento")
        try:
            geo_data = df.groupby('estado')['valor'].sum().reset_index()
            fig_geo = px.choropleth(
                geo_data,
                locations='estado',
                locationmode='country names',
                color='valor',
                scope='south america',
                color_continuous_scale='Viridis',
                title='Faturamento por Estado'
            )
            st.plotly_chart(fig_geo, use_container_width=True)
            
        except Exception as e:
            st.error(f"Erro ao criar mapa: {str(e)}")
            
        # Evolução Mensal    
        st.subheader("Evolução Mensal do Faturamento")
        try:
            df['mes_ano'] = df['data'].dt.strftime('%Y-%m')
            monthly_data = df.groupby('mes_ano')['valor'].sum().reset_index()
            fig_line = px.line(
                monthly_data,
                x='mes_ano',
                y='valor',
                title='Evolução do Faturamento Mensal'
            )
            fig_line.update_layout(
                xaxis_title='Mês/Ano',
                yaxis_title='Valor Faturado (R$)',
                yaxis_tickformat=',.2f'
            )
            st.plotly_chart(fig_line, use_container_width=True)
            
        except Exception as e:
            st.error(f"Erro ao criar gráfico mensal: {str(e)}")
            
        # Gráficos em colunas
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Faturamento por Grupo")
            try:
                grupo_data = df.groupby('grupo')['valor'].sum().reset_index()
                fig_grupo = px.bar(
                    grupo_data.sort_values('valor', ascending=True).tail(10),
                    x='valor',
                    y='grupo',
                    orientation='h',
                    title='Top 10 Grupos'
                )
                fig_grupo.update_layout(
                    xaxis_title='Valor Faturado (R$)',
                    yaxis_title='Grupo',
                    xaxis_tickformat=',.2f'
                )
                st.plotly_chart(fig_grupo, use_container_width=True)
            except Exception as e:
                st.error(f"Erro ao criar gráfico de grupos: {str(e)}")
            
        with col2:
            st.subheader("Faturamento por Categoria")
            try:
                cat_data = df.groupby('categoria')['valor'].sum().reset_index()
                fig_cat = px.bar(
                    cat_data.sort_values('valor', ascending=True).tail(10),
                    x='valor',
                    y='categoria',
                    orientation='h',
                    title='Top 10 Categorias'
                )
                fig_cat.update_layout(
                    xaxis_title='Valor Faturado (R$)',
                    yaxis_title='Categoria',
                    xaxis_tickformat=',.2f'
                )
                st.plotly_chart(fig_cat, use_container_width=True)
            except Exception as e:
                st.error(f"Erro ao criar gráfico de categorias: {str(e)}")
        
        # Faturamento por Estado
        st.subheader("Top Estados por Faturamento")
        try:
            estado_data = df.groupby('estado')['valor'].sum().reset_index()
            fig_estado = px.bar(
                estado_data.sort_values('valor', ascending=True).tail(10),
                x='valor',
                y='estado',
                orientation='h',
                title='Top 10 Estados'
            )
            fig_estado.update_layout(
                xaxis_title='Valor Faturado (R$)',
                yaxis_title='Estado',
                xaxis_tickformat=',.2f'
            )
            st.plotly_chart(fig_estado, use_container_width=True)
        except Exception as e:
            st.error(f"Erro ao criar gráfico de estados: {str(e)}")
            
    else:
        st.error("Não foi possível carregar os dados da API")

# Executar o dashboard
show_faturamento()
