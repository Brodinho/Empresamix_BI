# Dashboard EmpresaMix

Dashboard interativo desenvolvido com Streamlit para visualização de dados comerciais e financeiros.

## Requisitos do Sistema

- Python 3.8 ou superior
- Bibliotecas principais:
  - pandas
  - plotly
  - streamlit
  - python-dotenv
  - requests (para integração com API)

## Estrutura do Projeto

empresamixBI/
├── .streamlit/
│   └── config.toml
├── pages/
│   ├── 1_comercial.py
│   └── 2_financeiro.py
├── utils/
│   ├── api_connector.py
│   ├── data_processing.py
│   ├── layout.py
│   └── visualizations.py
├── .gitignore
├── .env
├── Home.py
└── README.md

## Instalação

1. Clone o repositório

bash
git clone https://github.com/Brodinho/empresamixBI.git
cd empresamixBI

2. Crie e ative o ambiente virtual

bash
python -m venv venv
Windows
venv\Scripts\activate
Linux/Mac
source venv/bin/activate

3. Instale as dependências

bash
pip install -r requirements.txt

4. Configure as variáveis de ambiente no arquivo .env

bash
API Comercial
API_URL=http://tecnolife.empresamix.info:8077/POWERBI/
API_CLIENT=TECNOLIFE
API_ID=XIOPMANA
API_VIEW=CUBO_FATURAMENTO
Configurações do Streamlit
STREAMLIT_THEME=dark
PAGE_TITLE=EmpresaMixBI
PAGE_ICON=📊


## Uso
Execute o aplicativo Streamlit:

bash
streamlit run Home.py


## Módulos

### Comercial
- Dashboard de vendedores
  - Análise de performance individual
  - Ranking de vendas
  - Número de pedidos
- Evolução mensal do faturamento
  - Comparativo anual
  - Tendências de vendas
- Distribuição geográfica das vendas
  - Mapa interativo
  - Análise por região

### Financeiro
- Análise de receitas e despesas
- Fluxo de caixa
- Indicadores financeiros

## Tecnologias Utilizadas
- Python 3.8+
- Streamlit (interface web)
- Pandas (análise de dados)
- Plotly (visualizações)
- Python-dotenv (variáveis de ambiente)
- Requests (integração API)

## Suporte e Contato
- Email: [help@empresamix.com.br]
- Issues: Utilize o sistema de issues do GitHub
- Wiki: Consulte a wiki do projeto para mais detalhes

## Contribuição
1. Fork o projeto
2. Crie sua Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m "Add some AmazingFeature"`)
4. Push para a Branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

