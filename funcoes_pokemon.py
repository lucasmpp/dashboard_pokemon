from re import template
import pandas as pd   
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px

from plotly import tools
import plotly.graph_objs as go
import plotly.figure_factory as ff


#plt.style.use('bmh')
#plt.rcParams['figure.dpi'] = 100


def grafico_radar_comparacao(dados, tipos):
    cores_tipos = {
        'normal': '#A8A77A',
        'fire': '#EE8130',
        'water': '#6390F0',
        'electric': '#F7D02C',
        'grass': '#7AC74C',
        'ice': '#96D9D6',
        'fighting': '#C22E28',
        'poison': '#A33EA1',
        'ground': '#E2BF65',
        'flying': '#A98FF3',
        'psychic': '#F95587',
        'bug': '#A6B91A',
        'rock': '#B6A136',
        'ghost': '#735797',
        'dragon': '#6F35FC',
        'dark': '#705746',
        'steel': '#B7B7CE',
        'fairy': '#D685AD',
    }
    maximo_grafico = 0

    def layer_do_tipo(tipo):
        nonlocal maximo_grafico

        filtrado = dados.query('(type1 == @tipo) or (type2 == @tipo)')
        dict_medidas_resumo = (
            filtrado
            .loc[:, ['attack','defense','sp_attack','sp_defense','speed','hp']]
            .mean()
            .to_dict()
        )

        maximo_grafico = max(maximo_grafico, *dict_medidas_resumo.values())
        return go.Scatterpolar(
            name=tipo.capitalize(),
            r = [
                dict_medidas_resumo['hp'],
                dict_medidas_resumo['attack'],
                dict_medidas_resumo['defense'],
                dict_medidas_resumo['sp_attack'],
                dict_medidas_resumo['sp_defense'],
                dict_medidas_resumo['speed'],
                dict_medidas_resumo["hp"]
            ],
            theta = ['HP','Ataque','Defesa','Ataque Especial','Defesa Especial','Velocidade','HP'],
            fill = 'toself',
            line =  dict(
                color = cores_tipos[tipo]
            )
        )

    dados = [layer_do_tipo(tipo) for tipo in tipos]
    
    layout = go.Layout(
    polar = dict(
        radialaxis = dict(
        visible = True,
        range = [10, maximo_grafico*1.2]
        )
    ),
    showlegend = True,
    )

    fig = go.Figure(data=dados, layout=layout)
    return fig

def chart_catch_x_tot(df,tipos):
    cores_tipos = {
        'normal': '#A8A77A',
        'fire': '#EE8130',
        'water': '#6390F0',
        'electric': '#F7D02C',
        'grass': '#7AC74C',
        'ice': '#96D9D6',
        'fighting': '#C22E28',
        'poison': '#A33EA1',
        'ground': '#E2BF65',
        'flying': '#A98FF3',
        'psychic': '#F95587',
        'bug': '#A6B91A',
        'rock': '#B6A136',
        'ghost': '#735797',
        'dragon': '#6F35FC',
        'dark': '#705746',
        'steel': '#B7B7CE',
        'fairy': '#D685AD',
    }

    def parse_dados(df, tipo):
        df = df.query('type1 == @tipo | type2 == @tipo')
        df = df.loc[:, ['name', 'capture_rate', 'base_total']]
        

        return df

    #dfs = [parse_dados(df, tipo) for tipo in tipos]


    fig = go.Figure()
    for tipo in tipos:
        df1 = parse_dados(df,tipo)
        fig.add_trace(go.Scatter(
            x=df1.capture_rate,
            y=df1.base_total,
            hovertext=df1.name,
            name=tipo,
            marker_color=cores_tipos[tipo]
        ))
    fig.update_traces(mode = 'markers')
    return fig



# def chart_catch_x_tot(df):
#     a = list(df.capture_rate)
#     a[773]=0
#     x = list(map(int, a))
#     x[773]=np.nan
#     y=df.base_total
#     fig = px.scatter(df, x=x, y=y,hover_name=df.name,template='none')
#     fig.update_xaxes(title_text='Facilidade de captura')
#     fig.update_yaxes(title_text='Atributos totais')
#     return fig    

def chart_egg_x_tot(df):
    x = df.base_egg_steps
    y = df.base_total
    fig = px.box(df, x=x, y=y, hover_name=df.name,template='none', category_orders={"base_egg_steps":["1280","2560","3840","5120","6400",
                                                                                           "7680","8960","10240","20480","30720"]})
    fig.update_xaxes(title_text='Número de passos para chocar o ovo')
    fig.update_yaxes(title_text='Atributos totais')
    fig.update_xaxes(type='category')
    return fig

def chart_egg_x_catch(df):
    a = list(df.capture_rate)
    a[773]=0
    y = list(map(int, a))
    y[773]=np.nan
    x = df.base_egg_steps
    fig = px.box(df, x=x, y=y, hover_name=df.name,template='none', category_orders={"base_egg_steps":["1280","2560","3840","5120","6400",
                                                                                           "7680","8960","10240","20480","30720"]})
    fig.update_xaxes(title_text='Número de passos para chocar o ovo')
    fig.update_yaxes(title_text='Facilidade de captura')
    fig.update_xaxes(type='category')
    return fig    