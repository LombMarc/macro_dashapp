import datetime
from dash import Dash, dcc, html, dash_table
import plotly.graph_objects as go
from core.core import *

def create_app():


    year = str(datetime.datetime.today().year)
    app = Dash(__name__,meta_tags=[
            {"name": "viewport", "content": "width=device-width, initial-scale=1"}
        ])
    server = app.server


    colors = {
        'background': '#111111',
        'text': '#7FDBFF'
    }
    stock_indices = ['^GSPC', '^IXIC', '^DJI', '^FTSE', '^GDAXI', '^N225', 'FTSEMIB.MI']
    currency_pairs = ['EUR=X', 'GBP=X', 'JPY=X', 'CHF=X', 'CAD=X', 'AUD=X']

    # retrive data
    web = True
    if web:
        calend = economic_calendar()
        gy = yield_rate("germany")
        uy = yield_rate("united-kingdom")
        iy = yield_rate("italy")
        usy = yield_rate("united-states")
        ii = get_inflation("italy-inflation-rate")
        ei = get_inflation("euro-area-historical-inflation-rate")
        usi = get_inflation("usa-inflation-rate")
        euribor = Euribor()
        GDP = GDP_g20().iloc[:11]

    pd_st = []
    for i in stock_indices:
        f = yf.Ticker(i)
        df = f.history(period='1y')
        df['EMA20'] = df['Close'].ewm(span=20).mean()
        df['EMA50'] = df['Close'].ewm(span=50).mean()
        sign = ['']
        for i in range(1, len(df)):
            if df['EMA20'].iloc[i] > df['EMA50'].iloc[i] and df['EMA20'].iloc[i - 1] <= df['EMA50'].iloc[i - 1]:
                sign.append("^")
            elif df['EMA20'].iloc[i] < df['EMA50'].iloc[i] and df['EMA20'].iloc[i - 1] >= df['EMA50'].iloc[i - 1]:
                sign.append("v")
            else:
                sign.append("")
        df['sign'] = sign
        pd_st.append(df[-31:-1])

    pd_cp = []
    for i in currency_pairs:
        f = yf.Ticker(i)
        df = f.history(period='1y')
        df['EMA20'] = df['Close'].ewm(span=20).mean()
        df['EMA50'] = df['Close'].ewm(span=50).mean()
        sign = ['']
        for i in range(1, len(df)):
            if df['EMA20'].iloc[i] > df['EMA50'].iloc[i] and df['EMA20'].iloc[i - 1] <= df['EMA50'].iloc[i - 1]:
                sign.append("^")
            elif df['EMA20'].iloc[i] < df['EMA50'].iloc[i] and df['EMA20'].iloc[i - 1] >= df['EMA50'].iloc[i - 1]:
                sign.append("v")
            else:
                sign.append("")
        df['sign'] = sign
        pd_cp.append(df.iloc[-41:-1])

    #build graph object
    #stock index
    sp = go.Figure()
    sp.add_candlestick(close=pd_st[0]['Close'],high=pd_st[0]['High'],open=pd_st[0]['Open'],low=pd_st[0]['Low'],x=pd_st[0].index.tolist(),name='candle')
    sp.add_scatter(x = pd_st[0].index.tolist(),y = pd_st[0]['EMA20'],mode ='lines',name='EMA20',line= dict(color='orange'))
    sp.add_scatter(x = pd_st[0].index.tolist(),y = pd_st[0]['EMA50'],mode ='lines',name='EMA50',line=dict(color='blue'))
    sp.add_scatter(x= pd_st[0][pd_st[0]['sign']=='^'].index.tolist(),y=pd_st[0][pd_st[0]['sign']=='^']['EMA50']*.98,mode='markers',marker=dict(symbol='triangle-up',color='green'),name='up signal' )
    sp.add_scatter(x= pd_st[0][pd_st[0]['sign']=='v'].index.tolist(),y=pd_st[0][pd_st[0]['sign']=='v']['EMA20']*1.02,mode='markers',marker=dict(symbol='triangle-down',color='red'),name='down signal' )
    sp.update_layout(title="S&P500",xaxis_rangeslider_visible=False)

    nq = go.Figure()
    nq.add_candlestick(close=pd_st[1]['Close'],high=pd_st[1]['High'],open=pd_st[1]['Open'],low=pd_st[1]['Low'],x=pd_st[1].index.tolist(),name='candle')
    nq.add_scatter(x = pd_st[1].index.tolist(),y = pd_st[1]['EMA20'],mode ='lines',name='EMA20',line= dict(color='orange'))
    nq.add_scatter(x = pd_st[1].index.tolist(),y = pd_st[1]['EMA50'],mode ='lines',name='EMA50',line=dict(color='blue'))
    nq.add_scatter(x= pd_st[1][pd_st[1]['sign']=='^'].index.tolist(),y=pd_st[1][pd_st[1]['sign']=='^']['EMA50']*.98,mode='markers',marker=dict(symbol='triangle-up',color='green'),name='up signal' )
    nq.add_scatter(x= pd_st[1][pd_st[1]['sign']=='v'].index.tolist(),y=pd_st[1][pd_st[1]['sign']=='v']['EMA20']*1.02,mode='markers',marker=dict(symbol='triangle-down',color='red'),name='down signal' )
    nq.update_layout(title="NASDAQ",xaxis_rangeslider_visible=False)

    dj = go.Figure()
    dj.add_candlestick(close=pd_st[2]['Close'],high=pd_st[2]['High'],open=pd_st[2]['Open'],low=pd_st[2]['Low'],x=pd_st[2].index.tolist(),name='candle')
    dj.add_scatter(x = pd_st[2].index.tolist(),y = pd_st[2]['EMA20'],mode ='lines',name='EMA20',line= dict(color='orange'))
    dj.add_scatter(x = pd_st[2].index.tolist(),y = pd_st[2]['EMA50'],mode ='lines',name='EMA50',line=dict(color='blue'))
    dj.add_scatter(x= pd_st[2][pd_st[2]['sign']=='^'].index.tolist(),y=pd_st[2][pd_st[2]['sign']=='^']['EMA50']*.98,mode='markers',marker=dict(symbol='triangle-up',color='green'),name='up signal' )
    dj.add_scatter(x= pd_st[2][pd_st[2]['sign']=='v'].index.tolist(),y=pd_st[2][pd_st[2]['sign']=='v']['EMA20']*1.02,mode='markers',marker=dict(symbol='triangle-down',color='red'),name='down signal' )
    dj.update_layout(title="DOWJONES",xaxis_rangeslider_visible=False)

    uk = go.Figure()
    uk.add_candlestick(close=pd_st[3]['Close'], high=pd_st[3]['High'], open=pd_st[3]['Open'], low=pd_st[3]['Low'], x=pd_st[3].index.tolist(),name='candle')
    uk.add_scatter(x = pd_st[3].index.tolist(),y = pd_st[3]['EMA20'],mode ='lines',name='EMA20',line= dict(color='orange'))
    uk.add_scatter(x = pd_st[3].index.tolist(),y = pd_st[3]['EMA50'],mode ='lines',name='EMA50',line=dict(color='blue'))
    uk.add_scatter(x= pd_st[3][pd_st[3]['sign']=='^'].index.tolist(),y=pd_st[3][pd_st[3]['sign']=='^']['EMA50']*.98,mode='markers',marker=dict(symbol='triangle-up',color='green'),name='up signal' )
    uk.add_scatter(x= pd_st[3][pd_st[3]['sign']=='v'].index.tolist(),y=pd_st[3][pd_st[3]['sign']=='v']['EMA20']*1.02,mode='markers',marker=dict(symbol='triangle-down',color='red'),name='down signal' )
    uk.update_layout(title="FTSE100", xaxis_rangeslider_visible=False)

    dx = go.Figure()
    dx.add_candlestick(close=pd_st[4]['Close'], high=pd_st[4]['High'], open=pd_st[4]['Open'], low=pd_st[4]['Low'], x=pd_st[4].index.tolist(),name='candle')
    dx.add_scatter(x = pd_st[4].index.tolist(),y = pd_st[4]['EMA20'],mode ='lines',name='EMA20',line= dict(color='orange'))
    dx.add_scatter(x = pd_st[4].index.tolist(),y = pd_st[4]['EMA50'],mode ='lines',name='EMA50',line=dict(color='blue'))
    dx.add_scatter(x= pd_st[4][pd_st[4]['sign']=='^'].index.tolist(),y=pd_st[4][pd_st[4]['sign']=='^']['EMA50']*.98,mode='markers',marker=dict(symbol='triangle-up',color='green'),name='up signal' )
    dx.add_scatter(x= pd_st[4][pd_st[4]['sign']=='v'].index.tolist(),y=pd_st[4][pd_st[4]['sign']=='v']['EMA20']*1.02,mode='markers',marker=dict(symbol='triangle-down',color='red'),name='down signal' )
    dx.update_layout(title="DAX", xaxis_rangeslider_visible=False)

    jp = go.Figure()
    jp.add_candlestick(close=pd_st[5]['Close'], high=pd_st[5]['High'], open=pd_st[5]['Open'], low=pd_st[5]['Low'], x=pd_st[5].index.tolist(),name='candle')
    jp.add_scatter(x = pd_st[5].index.tolist(),y = pd_st[5]['EMA20'],mode ='lines',name='EMA20',line= dict(color='orange'))
    jp.add_scatter(x = pd_st[5].index.tolist(),y = pd_st[5]['EMA50'],mode ='lines',name='EMA50',line=dict(color='blue'))
    jp.add_scatter(x= pd_st[5][pd_st[5]['sign']=='^'].index.tolist(),y=pd_st[5][pd_st[5]['sign']=='^']['EMA50']*.98,mode='markers',marker=dict(symbol='triangle-up',color='green'),name='up signal' )
    jp.add_scatter(x= pd_st[5][pd_st[5]['sign']=='v'].index.tolist(),y=pd_st[5][pd_st[5]['sign']=='v']['EMA20']*1.02,mode='markers',marker=dict(symbol='triangle-down',color='red'),name='down signal' )
    jp.update_layout(title="NIKKEI", xaxis_rangeslider_visible=False)

    mi = go.Figure()
    mi.add_candlestick(close=pd_st[6]['Close'], high=pd_st[6]['High'], open=pd_st[6]['Open'], low=pd_st[6]['Low'], x=pd_st[6].index.tolist(),name='candle')
    mi.add_scatter(x = pd_st[6].index.tolist(),y = pd_st[6]['EMA20'],mode ='lines',name='EMA20',line= dict(color='orange'))
    mi.add_scatter(x = pd_st[6].index.tolist(),y = pd_st[6]['EMA50'],mode ='lines',name='EMA50',line=dict(color='blue'))
    mi.add_scatter(x= pd_st[6][pd_st[6]['sign']=='^'].index.tolist(),y=pd_st[6][pd_st[6]['sign']=='^']['EMA50']*.98,mode='markers',marker=dict(symbol='triangle-up',color='green'),name='up signal' )
    mi.add_scatter(x= pd_st[6][pd_st[6]['sign']=='v'].index.tolist(),y=pd_st[6][pd_st[6]['sign']=='v']['EMA20']*1.02,mode='markers',marker=dict(symbol='triangle-down',color='red'),name='down signal' )
    mi.update_layout(title="MIB", xaxis_rangeslider_visible=False)

    #currency pairs
    ed = go.Figure()
    ed.add_candlestick(close=pd_cp[0]['Close'],high=pd_cp[0]['High'],open=pd_cp[0]['Open'],low=pd_cp[0]['Low'],x=pd_cp[0].index.tolist(),name='candle')
    ed.add_scatter(x = pd_cp[0].index.tolist(),y = pd_cp[0]['EMA20'],mode ='lines',name='EMA20',line= dict(color='orange'))
    ed.add_scatter(x = pd_cp[0].index.tolist(),y = pd_cp[0]['EMA50'],mode ='lines',name='EMA50',line=dict(color='blue'))
    ed.add_scatter(x= pd_cp[0][pd_cp[0]['sign']=='^'].index.tolist(),y=pd_cp[0][pd_cp[0]['sign']=='^']['EMA50']*.98,mode='markers',marker=dict(symbol='triangle-up',color='green'),name='up signal' )
    ed.add_scatter(x= pd_cp[0][pd_cp[0]['sign']=='v'].index.tolist(),y=pd_cp[0][pd_cp[0]['sign']=='v']['EMA20']*1.02,mode='markers',marker=dict(symbol='triangle-down',color='red'),name='down signal' )
    ed.update_layout(title="USD/EUR",xaxis_rangeslider_visible=False)

    gd = go.Figure()
    gd.add_candlestick(close=pd_cp[1]['Close'],high=pd_cp[1]['High'],open=pd_cp[1]['Open'],low=pd_cp[1]['Low'],x=pd_cp[1].index.tolist(),name='candle')
    gd.add_scatter(x = pd_cp[1].index.tolist(),y = pd_cp[1]['EMA20'],mode ='lines',name='EMA20',line= dict(color='orange'))
    gd.add_scatter(x = pd_cp[1].index.tolist(),y = pd_cp[1]['EMA50'],mode ='lines',name='EMA50',line=dict(color='blue'))
    gd.add_scatter(x= pd_cp[1][pd_cp[1]['sign']=='^'].index.tolist(),y=pd_cp[1][pd_cp[1]['sign']=='^']['EMA50']*.98,mode='markers',marker=dict(symbol='triangle-up',color='green'),name='up signal' )
    gd.add_scatter(x= pd_cp[1][pd_cp[1]['sign']=='v'].index.tolist(),y=pd_cp[1][pd_cp[1]['sign']=='v']['EMA20']*1.02,mode='markers',marker=dict(symbol='triangle-down',color='red'),name='down signal' )

    gd.update_layout(title="USD/GBP",xaxis_rangeslider_visible=False)

    yd = go.Figure()
    yd.add_candlestick(close=pd_cp[2]['Close'],high=pd_cp[2]['High'],open=pd_cp[2]['Open'],low=pd_cp[2]['Low'],x=pd_cp[2].index.tolist(),name='candle')
    yd.add_scatter(x = pd_cp[2].index.tolist(),y = pd_cp[2]['EMA20'],mode ='lines',name='EMA20',line= dict(color='orange'))
    yd.add_scatter(x = pd_cp[2].index.tolist(),y = pd_cp[2]['EMA50'],mode ='lines',name='EMA50',line=dict(color='blue'))
    yd.add_scatter(x= pd_cp[2][pd_cp[2]['sign']=='^'].index.tolist(),y=pd_cp[2][pd_cp[2]['sign']=='^']['EMA50']*.98,mode='markers',marker=dict(symbol='triangle-up',color='green'),name='up signal' )
    yd.add_scatter(x= pd_cp[2][pd_cp[2]['sign']=='v'].index.tolist(),y=pd_cp[2][pd_cp[2]['sign']=='v']['EMA20']*1.02,mode='markers',marker=dict(symbol='triangle-down',color='red'),name='down signal' )

    yd.update_layout(title="USD/JPY",xaxis_rangeslider_visible=False)

    sd = go.Figure()
    sd.add_candlestick(close=pd_cp[3]['Close'],high=pd_cp[3]['High'],open=pd_cp[3]['Open'],low=pd_cp[3]['Low'],x=pd_cp[3].index.tolist(),name='candle')
    sd.add_scatter(x = pd_cp[3].index.tolist(),y = pd_cp[3]['EMA20'],mode ='lines',name='EMA20',line= dict(color='orange'))
    sd.add_scatter(x = pd_cp[3].index.tolist(),y = pd_cp[3]['EMA50'],mode ='lines',name='EMA50',line=dict(color='blue'))
    sd.add_scatter(x= pd_cp[3][pd_cp[3]['sign']=='^'].index.tolist(),y=pd_cp[3][pd_cp[3]['sign']=='^']['EMA50']*.98,mode='markers',marker=dict(symbol='triangle-up',color='green'),name='up signal' )
    sd.add_scatter(x= pd_cp[3][pd_cp[3]['sign']=='v'].index.tolist(),y=pd_cp[3][pd_cp[3]['sign']=='v']['EMA20']*1.02,mode='markers',marker=dict(symbol='triangle-down',color='red'),name='down signal' )

    sd.update_layout(title="USD/CHF",xaxis_rangeslider_visible=False)

    cd = go.Figure()
    cd.add_candlestick(close=pd_cp[4]['Close'],high=pd_cp[4]['High'],open=pd_cp[4]['Open'],low=pd_cp[4]['Low'],x=pd_cp[4].index.tolist(),name='candle')
    cd.add_scatter(x = pd_cp[4].index.tolist(),y = pd_cp[4]['EMA20'],mode ='lines',name='EMA20',line= dict(color='orange'))
    cd.add_scatter(x = pd_cp[4].index.tolist(),y = pd_cp[4]['EMA50'],mode ='lines',name='EMA50',line=dict(color='blue'))
    cd.add_scatter(x= pd_cp[4][pd_cp[4]['sign']=='^'].index.tolist(),y=pd_cp[4][pd_cp[4]['sign']=='^']['EMA50']*.98,mode='markers',marker=dict(symbol='triangle-up',color='green'),name='up signal' )
    cd.add_scatter(x= pd_cp[4][pd_cp[4]['sign']=='v'].index.tolist(),y=pd_cp[4][pd_cp[4]['sign']=='v']['EMA20']*1.02,mode='markers',marker=dict(symbol='triangle-down',color='red'),name='down signal' )

    cd.update_layout(title="USD/CAD",xaxis_rangeslider_visible=False)

    ad = go.Figure()
    ad.add_candlestick(close=pd_cp[5]['Close'],high=pd_cp[5]['High'],open=pd_cp[5]['Open'],low=pd_cp[5]['Low'],x=pd_cp[5].index.tolist(),name='candle')
    ad.add_scatter(x = pd_cp[5].index.tolist(),y = pd_cp[5]['EMA20'],mode ='lines',name='EMA20',line= dict(color='orange'))
    ad.add_scatter(x = pd_cp[5].index.tolist(),y = pd_cp[5]['EMA50'],mode ='lines',name='EMA50',line=dict(color='blue'))
    ad.add_scatter(x= pd_cp[5][pd_cp[5]['sign']=='^'].index.tolist(),y=pd_cp[5][pd_cp[5]['sign']=='^']['EMA50']*.98,mode='markers',marker=dict(symbol='triangle-up',color='green'),name='up signal' )
    ad.add_scatter(x= pd_cp[5][pd_cp[5]['sign']=='v'].index.tolist(),y=pd_cp[5][pd_cp[5]['sign']=='v']['EMA20']*1.02,mode='markers',marker=dict(symbol='triangle-down',color='red'),name='down signal' )

    ad.update_layout(title="USD/AUD",xaxis_rangeslider_visible=False)

    #macroeconomic data
    fig = go.Figure()
    fig.add_scatter(x=gy['Maturity'], y=gy["Yield"], mode ="lines+markers", name="Germany yields")
    fig.add_scatter(x=uy['Maturity'], y=uy["Yield"], mode ="lines+markers", name="United Kingdom yields")
    fig.add_scatter(x=iy['Maturity'],y=iy["Yield"],mode='lines+markers',name="Italian yields")
    fig.add_scatter(x=usy['Maturity'],y=usy["Yield"],mode='lines+markers',name="US yields")
    fig.update_layout(
        title="Euro, US and Italy yields curves",
        plot_bgcolor=colors['background'],
        paper_bgcolor=colors['background'],
        font_color=colors['text'],
        hovermode="x"
    )



    inf = go.Figure()
    inf.add_scatter(x=ei.columns[1:-1],y=ei[ei.columns[1:-1]].iloc[0],mode="markers+lines",name="Euro")
    inf.add_scatter(x=ii.columns[1:-1],y=ii[ii.columns[1:-1]].iloc[0],mode="markers+lines",name="Italy")
    inf.add_scatter(x=usi.columns[1:-1],y=usi[usi.columns[1:-1]].iloc[0],mode="markers+lines",name="US")
    inf.update_layout(
        title=f"Inflation {year} ",
        plot_bgcolor=colors['background'],
        paper_bgcolor=colors['background'],
        font_color=colors['text'],
        hovermode="x"
    )


    inf_it = go.Figure()
    inf_it.add_scatter(x=ei.columns[1:-1],y=ei[ei.columns[1:-1]].iloc[1],mode="markers+lines",name="EUro")
    inf_it.add_scatter(x=ii.columns[1:-1],y=ii[ii.columns[1:-1]].iloc[1],mode="markers+lines",name="Italy")
    inf_it.add_scatter(x=usi.columns[1:-1],y=usi[usi.columns[1:-1]].iloc[1],mode="markers+lines",name="US")
    inf_it.update_layout(
        title="Inflation 2022",
        plot_bgcolor=colors['background'],
        paper_bgcolor=colors['background'],
        font_color=colors['text'],
        hovermode="x"
    )

    inf_us = go.Figure()
    inf_us.add_scatter(x=usi.columns[1:-1],y=usi[usi.columns[1:-1]].iloc[1],mode="markers+lines",name="Inflation US 2022")
    inf_us.add_scatter(x=usi.columns[1:-1],y=usi[usi.columns[1:-1]].iloc[0],mode="markers+lines",name="Inflation US 2023")
    inf_us.update_layout(
        title="Inflation in USA 2023 vs 2022",
        plot_bgcolor=colors['background'],
        paper_bgcolor=colors['background'],
        font_color=colors['text'],
        hovermode="x"
    )


    rat = go.Figure()
    rat.add_scatter(x=euribor['Maturity'],y=euribor['Rate'],mode="markers+lines",name="Last EURIBOR")
    rat.update_layout(
        title="EURIBOR",
        plot_bgcolor=colors['background'],
        paper_bgcolor=colors['background'],
        font_color=colors['text'],
        hovermode="x"
    )

    gdp_fg = go.Figure()
    gdp_fg.add_bar(x=GDP['Country'].iloc[1:-1],y=GDP['GDP 2022 (Billions $)'].iloc[1:-1],name='GDP 2022')
    gdp_fg.add_bar(x=GDP['Country'].iloc[1:-1],y=GDP['GDP 2023 (Billions $)'].iloc[1:-1],name='GDP 2023')
    gdp_fg.update_layout(
        title="GDP",
        plot_bgcolor=colors['background'],
        paper_bgcolor=colors['background'],
        font_color=colors['text'],
        hovermode="x"
    )


    inflation = pd.DataFrame()
    inflation['Year']= ii['Year']
    inflation['Annual_IT (%)'] = round(ii[ii.columns[1:-1]].mean(axis=1,skipna=True)*100,4)
    inflation['Annual_US (%)'] = round(usi[usi.columns[1:-1]].mean(axis=1,skipna=True)*100,4)
    inflation['Annual_EU (%)'] = round(ei[ei.columns[1:-1]].mean(axis=1,skipna=True)*100,4)


    #page layout for mobile
    mob = html.Div(
        children=[
            html.Div(children=[html.H1(children="Dashboard for stock market"),html.H1(children=str(datetime.date.today()),style={'margin':'auto'})]),
            html.Div(children=dcc.Graph(id="SP500",figure=sp),style={'width':'80%'}),
            html.Div(children=dcc.Graph(id="dow",figure=dj),style={'width':'80%'}),
            html.Div(children=dcc.Graph(id="nsdq", figure=nq), style={'width': '80%'}),
            html.Div(children=dcc.Graph(id="uk", figure=uk), style={'width': '80%'}),
            html.Div(children=dcc.Graph(id="dax", figure=dx), style={'width': '80%'}),
            html.Div(children=dcc.Graph(id="jap", figure=jp), style={'width': '80%'}),
            html.Div(children=dcc.Graph(id="it", figure=mi), style={'width': '80%'}),
            html.H2(children="Currency pairs"),
            html.Div(children=dcc.Graph(id="de", figure=ed), style={'width': '80%'}),
            html.Div(children=dcc.Graph(id="dp", figure=gd), style={'width': '80%'}),
            html.Div(children=dcc.Graph(id="dy", figure=yd), style={'width': '80%'}),
            html.Div(children=dcc.Graph(id="ds", figure=sd), style={'width': '80%'}),
            html.Div(children=dcc.Graph(id="dc", figure=cd), style={'width': '80%'}),
            html.Div(children=dcc.Graph(id="da", figure=ad), style={'width': '80%'}),
            html.H1(children="Yield curves"),
            html.Div(children=[dcc.Graph(id='Yield_curve',figure=fig)],style={'padding':'20px','margin-bottom':'30px','width':'80%'}),
            html.Div(children=[html.H2(children="Inflation"), html.H4(children="The value for the last year available is the avarage inflation in the last months")]),
            html.Div( children=[dash_table.DataTable(inflation.iloc[0:7].to_dict('records'), [{"name": i, "id": i} for i in inflation.columns],style_cell={'text-align':'center'})],style={'padding-left':'30px','padding-right':'30px'}),
            html.Div( children =[dcc.Graph(id="Inflaiton",figure=inf)],style={'padding':'20px','margin-bottom':'30px','width':'80%'}),
            html.Div(children=[html.H2(children="Euribor")]),
            html.Div( children =[dcc.Graph(id="eurib",figure=rat)],style={'padding':'20px','margin-bottom':'30px','width':'80%'}),
            html.Div(children=[html.H2(children="Inflation 2021")]),
            html.Div( children =[dcc.Graph(id="infl21",figure=inf_it)],style={'padding':'20px','margin-bottom':'30px','width':'80%'}),
            html.Div(children=[html.H2(children="GDP")]),
            html.Div( children=[dash_table.DataTable(GDP.iloc[0:11].to_dict('records'), [{"name": i, "id": i} for i in GDP.columns],style_cell={'text-align':'center'})],style={'padding':'20px','margin-bottom':'30px','width':'80%'}),
            html.Div( children =[dcc.Graph(id="gdp",figure=gdp_fg)],style={'padding':'20px','margin-bottom':'30px','width':'80%'}),
            html.Div(children=[
            html.H2(children="Economic calendar: "+str(datetime.date.today()),style={'padding-top':'50px'}),
            html.Div(children=[dash_table.DataTable(calend.to_dict('records'), [{"name": i, "id": i} for i in calend.columns],style_cell={'text-align':'center'},style_header={
            'backgroundColor': 'white',
            'fontWeight': 'bold'
        })],style={"margin-left":"25%",'margin-right':'25%','padding-top':'50px'})])
        ]
    )


    #page layout
    desk = html.Div(children=[html.Div(children=[html.H1(children="Dashboard for stock market"),html.H1(children=str(datetime.date.today()),style={'margin-left':'85%'})]),
        #html.Div(children=[html.Button('Mobile view', id='submit-val', n_clicks=0)]),
        html.Div(children=[html.H2(children="American market")]),
        html.Div(children=[html.Table( children=[

            html.Tr(children=[
                html.Td(children=html.Div(children=dcc.Graph(id="SP500",figure=sp)),style={'width':'30%'}),
                html.Td(html.Div(children=[dcc.Graph(id="dow",figure=dj)]),style={'width':'30%'}),
                html.Td(html.Div(children=dcc.Graph(id="nsdq",figure=nq)),style={'width':'30%'})
                ]),
            ],style={'width':'100%'}) #america market
        ]),
        html.Div(children=[html.Table( children=[

            html.Tr(children=[
                html.Td(children=html.Div(children=dcc.Graph(id="uk",figure=uk)),style={'width':'30%'}),
                html.Td(html.Div(children=[dcc.Graph(id="dax",figure=dx)]),style={'width':'30%'}),
                html.Td(html.Div(children=dcc.Graph(id="jap",figure=jp)),style={'width':'30%'})
                ]),
            ],style={'width':'100%'}) #other market
        ]),
        html.Div(children=dcc.Graph(id='it',figure=mi),style={'margin':'auto'}), #italian market
        html.Div(children=[html.H2(children="Currency pairs")]),
        html.Div(children=[html.Table( children=[

            html.Tr(children=[
                html.Td(children=html.Div(children=dcc.Graph(id="d/e",figure=ed)),style={'width':'30%'}),
                html.Td(html.Div(children=[dcc.Graph(id="d/p",figure=gd)]),style={'width':'30%'}),
                html.Td(html.Div(children=dcc.Graph(id="d/y",figure=yd)),style={'width':'30%'})
                ]),
            ],style={'width':'100%'}) #first 3 currency pairs
        ]),
        html.Div(children=[html.Table( children=[

            html.Tr(children=[
                html.Td(children=html.Div(children=dcc.Graph(id="d/s",figure=sd)),style={'width':'30%'}),
                html.Td(html.Div(children=[dcc.Graph(id="d/c",figure=cd)]),style={'width':'30%'}),
                html.Td(html.Div(children=dcc.Graph(id="d/a",figure=ad)),style={'width':'30%'})
                ]),
            ],style={'width':'100%'}) #last 3 currency pair
        ]),html.Div(children=html.H1(children="Yield curve")),html.Div(children=[
            dcc.Graph(id='Yield_curve',figure=fig)
        ],style={'width':'80%','margin':'auto'}),
        #second div with table and plot of inflation
        html.Div(children=[html.H2(children="Inflation in 2023"), html.H4(children="The value for the last year available is the avarage inflation in the last months"),
            html.Div(children=[
            html.Div( children=[dash_table.DataTable(inflation.iloc[0:7].to_dict('records'), [{"name": i, "id": i} for i in inflation.columns],style_cell={'text-align':'center'})],style={'padding-left':'30px','padding-right':'30px','margin':'auto','flex':'1'}),
            html.Div( children =[dcc.Graph(id="Inflaiton",figure=inf)],style={'padding':'20px','margin-bottom':'30px','width':'45%'})],style={'display':'flex','width':'100%'})]

        ),
        #third div with table and plot of inflation
        html.Div(children=[html.H2(children="EURIBOR and Inflation in 2022")]),
        html.Div(children=[
            html.Div( children=[dcc.Graph(id='Euribor',figure=rat)],style={'width':'48%','padding':'20px','flex':'1'}),
            html.Div( children =[dcc.Graph(id="Inflaiton_it",figure=inf_it)],style={'width':'48%', 'float':'left','padding':'20px'})],style={'display':'flex'}
        ),
        #7th div with GDP data
        html.Div(children=[
            html.H2(children="GROSS DOMESTIC PRODUCT"),
            html.Div(children =[
            html.Div( children=[dash_table.DataTable(GDP.iloc[0:11].to_dict('records'), [{"name": i, "id": i} for i in GDP.columns],style_cell={'text-align':'center'})],style={'float':'left','margin-left':'5%','margin-top':'2.5%','flex':'1'}),
            html.Div( children =[dcc.Graph(id="gdp_word",figure=gdp_fg)],style={'float':'left','margin-left':'5%','margin-right':'5%','width':'45%'})],style={'display':'flex'})]

        ),
    #6th div with economic calendar
        html.Div(children=[
            html.H2(children="Economic calendar: "+str(datetime.date.today()),style={'padding-top':'50px'}),
            html.Div(children=[dash_table.DataTable(calend.to_dict('records'), [{"name": i, "id": i} for i in calend.columns],style_cell={'text-align':'center'},style_header={
            'backgroundColor': 'white',
            'fontWeight': 'bold'
        })],style={"margin-left":"25%",'margin-right':'25%','padding-top':'50px'})


        ])
    ]
    )

    #page layout for mobile
    mob = html.Div(
        children=[
            html.Div(children=[html.H1(children="Dashboard for stock market"),html.H1(children=str(datetime.date.today()),style={'margin':'auto'})]),
            html.Div(children=dcc.Graph(id="SP500",figure=sp),style={'width':'80%'}),
            html.Div(children=dcc.Graph(id="dow",figure=dj),style={'width':'80%'}),
            html.Div(children=dcc.Graph(id="nsdq", figure=nq), style={'width': '80%'}),
            html.Div(children=dcc.Graph(id="uk", figure=uk), style={'width': '80%'}),
            html.Div(children=dcc.Graph(id="dax", figure=dx), style={'width': '80%'}),
            html.Div(children=dcc.Graph(id="jap", figure=jp), style={'width': '80%'}),
            html.Div(children=dcc.Graph(id="it", figure=mi), style={'width': '80%'}),
            html.H2(children="Currency pairs"),
            html.Div(children=dcc.Graph(id="de", figure=ed), style={'width': '80%'}),
            html.Div(children=dcc.Graph(id="dp", figure=gd), style={'width': '80%'}),
            html.Div(children=dcc.Graph(id="dy", figure=yd), style={'width': '80%'}),
            html.Div(children=dcc.Graph(id="ds", figure=sd), style={'width': '80%'}),
            html.Div(children=dcc.Graph(id="dc", figure=cd), style={'width': '80%'}),
            html.Div(children=dcc.Graph(id="da", figure=ad), style={'width': '80%'}),
            html.H1(children="Yield curves"),
            html.Div(children=[dcc.Graph(id='Yield_curve',figure=fig)],style={'padding':'20px','margin-bottom':'30px','width':'80%'}),
            html.Div(children=[html.H2(children="Inflation"), html.H4(children="The value for the last year available is the avarage inflation in the last months")]),
            html.Div( children=[dash_table.DataTable(inflation.iloc[0:7].to_dict('records'), [{"name": i, "id": i} for i in inflation.columns],style_cell={'text-align':'center'})],style={'padding-left':'30px','padding-right':'30px'}),
            html.Div( children =[dcc.Graph(id="Inflaiton",figure=inf)],style={'padding':'20px','margin-bottom':'30px','width':'80%'}),
            html.Div(children=[html.H2(children="Euribor")]),
            html.Div( children =[dcc.Graph(id="eurib",figure=rat)],style={'padding':'20px','margin-bottom':'30px','width':'80%'}),
            html.Div(children=[html.H2(children="Inflation 2021")]),
            html.Div( children =[dcc.Graph(id="infl21",figure=inf_it)],style={'padding':'20px','margin-bottom':'30px','width':'80%'}),
            html.Div(children=[html.H2(children="GDP")]),
            html.Div( children=[dash_table.DataTable(GDP.iloc[0:11].to_dict('records'), [{"name": i, "id": i} for i in GDP.columns],style_cell={'text-align':'center'})],style={'padding':'20px','margin-bottom':'30px','width':'80%'}),
            html.Div( children =[dcc.Graph(id="gdp",figure=gdp_fg)],style={'padding':'20px','margin-bottom':'30px','width':'80%'}),
            html.Div(children=[
            html.H2(children="Economic calendar: "+str(datetime.date.today()),style={'padding-top':'50px'}),
            html.Div(children=[dash_table.DataTable(calend.to_dict('records'), [{"name": i, "id": i} for i in calend.columns],style_cell={'text-align':'center'},style_header={
            'backgroundColor': 'white',
            'fontWeight': 'bold'
        })],style={"margin-left":"25%",'margin-right':'25%','padding-top':'50px'})])
        ]
    )

    app.layout = desk
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=False)

