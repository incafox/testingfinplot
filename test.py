import finplot as fplt
import numpy as np
import pandas as pd
import requests
import ta
import sys
from datetime import datetime
import time 
sys.setrecursionlimit(150000000)

def process(candles):
    marcadores = []
    #aux = []
    quote = []
    for index, row in candles.iterrows():
        quote.append(row)
        print (row['open'])
        if (len(quote)>4):
            pass


        #aux = row 
        #print(row['c1'], row['c2'])
    pass


def crosspoint_strategy(fast,slow):
        
    pass



# pull some data
symbol = 'USDT-BTC'
url = 'https://bittrex.com/Api/v2.0/pub/market/GetTicks?marketName=%s&tickInterval=fiveMin' % symbol
data = requests.get(url).json()

# format it in pandas
df = pd.DataFrame(data['result'])
#print (df)
df = pd.read_csv('EPM20-2Minutesx.csv')
df[' <Time>'] = (df['<Date>']+" "+df[' <Time>'])
#df = df[[' <Time>',' <Open>', ' <Close>', ' <High>', ' <Low>']]
print (df.head())
df = df.rename(columns={' <Time>':'time', ' <Open>':'open', ' <Close>':'close', ' <High>':'high', ' <Low>':'low', ' <Volume>':'volume'})
for e in range(len(df['time'])):
    df['time'][e] = datetime.strptime(df['time'][e], "%m/%d/%Y %H:%M:%S")

df = df.astype({'time':'datetime64[ns]'})
print(df)
# create three plots
ax,ax2,ax3 = fplt.create_plot(symbol, rows=3)

# plot candle sticks
candles = df[['time','open','close','high','low']]
fplt.candlestick_ochl(candles, ax=ax)

# put an MA in there
#fplt.plot(df['time'], df['close'].rolling(25).mean(), ax=ax, color='#00f', legend='ma-25')

# place some dumb markers
hi_wicks = df['high'] - df[['open','close']].T.max()
df.loc[(hi_wicks>hi_wicks.quantile(0.99)), 'marker'] = df['high']
#fplt.plot(df['time'], df['marker'], ax=ax, color='#f44', style='^', legend='dumb mark')


# draw some random crap on our second plot
fplt.plot(df['time'], np.random.normal(size=len(df)), ax=ax2, color='#927', legend='stuff')
fplt.set_y_range(ax2, -1.4, +1.7) # fix y-axis range

#process(candles)

#e = ta.add_all_ta_features(df, open="open", high="high", low="low", close="close", volume="volume")
ema_14 = ta.trend.EMAIndicator(df['close'],14,True).ema_indicator()
ema_32 = ta.trend.EMAIndicator(df['close'],32,True).ema_indicator()
# put an EMA in there
fplt.plot(df['time'], ema_14, ax=ax, color='#f00', legend='ema14')
fplt.plot(df['time'], ema_32, ax=ax, color='#0f0', legend='ema32')

portfolio = 10000
tick_price = 12.5
tick_size = 0.25
ema14 = []
ema32 = []
point = []
crossdown = [] 
# [(date1,y1,date2,y2)]
tuplas = []
inicio = (1,2) # tupla
fin = (1,2) #tupla
debe_entrar = False
debe_salir = False 
registro_portfolio = [portfolio] #para mostrar drowndowns
for e in range(len(ema_14)):
    ema14.append(ema14)
    ema32.append(ema32)
    if (e>40 ):
        promedio_anterior = df['close'].iloc[e-30:e]
        #print (promedio_anterior)
        accu = 0
        for h in promedio_anterior:
            accu += h
        promedio =accu/len(promedio_anterior)
        print (str(promedio) + " << "+ str(df['close'][e]))
        #print ( ema_14[e] > ema_32[e] , ema_14[e-1] < ema_32[e-1])
        #detecta subida
        if (ema_14[e] > ema_32[e] and ema_14[e-1] < ema_32[e-1] and promedio>df['close'][e] ):
            point.append(df['close'][e])
            inicio = (df['time'][e],df['close'][e])
            text = fplt.add_text((inicio[0], inicio[1]), str(portfolio), color='#bbff00')
            debe_salir = True
        #detecta bajada
        if (debe_salir and ema_14[e] < ema_32[e] and ema_14[e-1] > ema_32[e-1]):
            crossdown.append(df['close'][e])
            debe_salir = False 
            fin = (df['time'][e],df['close'][e])
            profit = (fin[1] - inicio[1])/tick_size 
            print ("===================================")
            #print (df['close'][e-4:e] )
            print ("inicio > " + str(inicio[1]))
            print ("fin    > " + str(fin[1]))
            print ("diference >> " + str(fin[1] - inicio[1]))
            print ("ticks >> " + str((fin[1] - inicio[1])/tick_size))
            profit = profit * tick_price 
            portfolio = portfolio + profit
            print ("profit > " + str(profit))
            #print (inicio[0],inicio[1],fin[0],fin[1])
            #print (type(inicio[0]))
            #line = fplt.add_line((inicio[0],inicio[1]),(fin[0],fin[1]),color='#555555',interactive=True)
            text = fplt.add_text((fin[0], fin[1]), str(portfolio), color='#bb4400')
            registro_portfolio.append(portfolio)
        else:
            point.append(np.NaN)
            crossdown.append(np.NaN)
    else:
        point.append(np.NaN)
        crossdown.append(np.NaN)

#for i in range(len(point)): 
#    print (i)
#fplt.plot(df['time'], point, ax=ax, color='#3f3', style='o', legend='crossover')
#fplt.plot(df['time'], crossdown, ax=ax, color='#33f', style='o', legend='crossover')
#fplt.add_line(df['time'],(dates[100].timestamp(),4.4),(dates[1100].timestamp(),4.6),color='#9900ff',interactive=False)
# finally a volume bar chart in our third plot

volumes = df[['time','open','close','volume']]
fplt.volume_ocv(volumes, ax=ax3)

print ("<<<<<<<<<<< resultado >>>>>>>>>>>>>>>>>")
print ("max : " + str(max( registro_portfolio) ))
print ("min :  " + str(min( registro_portfolio) ))
print ("numero de entradas: "+ str(len(registro_portfolio)))
print ("resultado final : " + str(portfolio) )

# we're done
fplt.show()
#print (df['marker'])

