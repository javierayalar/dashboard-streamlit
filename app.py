import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title='Performance Dashboard',layout = 'wide')

header = st.beta_container()
dataset = st.beta_container()
interactive = st.beta_container()

st.markdown(
    """
    <style>
    .main{
        background-color: #F4F4F4;
    }
    </style>
    """,
    unsafe_allow_html=True
)

background_color = '#F4F4F4'
plot_bar_color = '#b73a3a'

#borde plots: #959595
#fondo barras: #b73a3a

@st.cache
def get_data(filename):
    derivador_data = pd.read_excel(open(filename, 'rb'), sheet_name='Registros') 
    return derivador_data

with header:
    #st.markdown("<h1 style='text-align: center; color: red;'>Some title</h1>", unsafe_allow_html=True)
    html_temp = """
    <div style="background-color:#F4F4F4;">
    <h1 style="color:#000000;text-align:center;">Performance of the ticket system in the CAC Larco</h1>
    </div><br>"""
    st.markdown(html_temp,unsafe_allow_html=True)

with dataset:
    df = get_data('data_derivador.xls')
    #st.dataframe(df.head())

    date_min = df["FECHA"].min()
    date_max = df["FECHA"].max()

with interactive:

    row1_col1, row1_col2= st.beta_columns(2)

    with row1_col1:

        try:
            date_ini, date_fin = st.date_input("Filter by Date", [pd.to_datetime(date_min), pd.to_datetime(date_max)])
        except (ValueError):
            date_ini, date_fin = date_min, date_max

        mask = (df['FECHA'] >= str(date_ini)) & (df['FECHA'] <= str(date_fin))

        total_tickets = len(df.loc[mask])

        html_kpi1 = """
        <div>
        <table style="border: 2px solid #959595;width:60%;">
        <tr><td style="color:#000000;text-align:center;">Total Tickets</td></tr>
        <tr><td style="color:#000000;text-align:center;font-weight:bold;">"""f'{total_tickets}'"""</td></tr>
        </table>
        </div><br>"""
        st.markdown(html_kpi1,unsafe_allow_html=True)

        tiempo_sesion = df.loc[mask]["T. SESION (seg.)"].mean().round(2)

        html_kpi2 = """
        <div>
        <table style="border: 2px solid #959595;width:60%;">
        <tr><td style="color:#000000;text-align:center;">Session Time (Avg sec.)</td></tr>
        <tr><td style="color:#000000;text-align:center;font-weight:bold;">"""f'{tiempo_sesion}'"""</td></tr>
        </table>
        </div><br>"""
        st.markdown(html_kpi2,unsafe_allow_html=True)
        
    with row1_col2:

        f_diasemana = px.histogram(df.loc[mask]["DIA SEMANA"], x="DIA SEMANA", nbins=15, 
        title="Total Tickets per day of the week", color_discrete_sequence=[plot_bar_color])
        f_diasemana.update_layout(
            width=600,height=380,
            font=dict(
            color="#000000",size=13
            ),
            paper_bgcolor=background_color,
            plot_bgcolor=background_color,    
        )
        f_diasemana.update_xaxes(title="Day of the week")
        f_diasemana.update_yaxes(title="Total Tickets")
        st.plotly_chart(f_diasemana)    

    row2_col1, row2_col2= st.beta_columns(2)

    with row2_col1:

        f_motivo = px.histogram(df.loc[mask]["MOTIVO"], x="MOTIVO", nbins=15, 
        title="Total Tickets by Reason", color_discrete_sequence=[plot_bar_color])
        f_motivo.update_layout(
            width=600,height=380,
            font=dict(
            color="#000000",size=13
            ),
            paper_bgcolor=background_color,
            plot_bgcolor=background_color,    
        )
        f_motivo.update_xaxes(title="Reason")
        f_motivo.update_yaxes(title="Total Tickets")
        st.plotly_chart(f_motivo)
    
    with row2_col2:

        f_llegada = px.histogram(df.loc[mask]["HORA LLEGADA"], x="HORA LLEGADA", nbins=15, 
        title="Total Tickets by Arrival Time", color_discrete_sequence=[plot_bar_color])
        f_llegada.update_layout(
            width=600,height=380,
            font=dict(
            color="#000000",size=13
            ),
            paper_bgcolor=background_color,
            plot_bgcolor=background_color,    
        )
        f_llegada.update_xaxes(title="Arrival Time")
        f_llegada.update_yaxes(title="Total Tickets")
        
        st.plotly_chart(f_llegada)