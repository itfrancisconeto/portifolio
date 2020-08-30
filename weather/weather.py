#importar bibliotecas
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

#titulo
print ('Prever a temperatura maxima dada a temperatura minima')
print()

#carregar dados para o dataframe
df_weather=pd.read_csv(r'Summary_of_Weather.csv', sep=',', low_memory=False)

#verificar os tipos de dados
#df_weather.info()

#verificar o shape
#print (df_weather.shape)
#print()

#separar os atributos relevantes para o modelo
df_weather_clean = df_weather[['MaxTemp','MinTemp']].copy()

#verificar quantidade  de instancias nulas por atributo
nans = df_weather_clean.isna().sum()
print(nans[nans > 0])

#verificar a correlação entre as temperaturas maxima e minima
plt.figure(figsize=(6,5))
df_corr_ = df_weather_clean.corr()
ax_ = sns.heatmap(df_corr_, annot=True)
bottom, top = ax_.get_ylim()
ax_.set_ylim(bottom + 0.5, top - 0.5)
plt.show()
print()

#realizar a análise de regressão
x=df_weather_clean['MinTemp'].values #variável independente 
Y=df_weather_clean['MaxTemp'].values #variável dependente

#construir modelo de regressão
reg= LinearRegression()
x_Reshaped=x.reshape((-1, 1)) #colocar os dados no formato 2D
regressao= reg.fit (x_Reshaped,Y) #encontrar os coeficientes (realiza a regressão)

#realizar a previsão
previsao=reg.predict(x_Reshaped)

#análisar a  qualidade do modelo
print('Y = {}X {}'.format(reg.coef_,reg.intercept_))
R_2 = r2_score(Y, previsao)  #realiza o cálculo do R2
print("Coeficiente de Determinação (R2):", R_2)
print ("Capacidade de explicação do modelo (%): ", R_2.round(4) * 100)

#realiza a plotagem dos dados
plt.figure(figsize=(4, 4), dpi=100)
plt.scatter(x, Y,  color='gray') #realiza o plot do gráfico de dispersão
plt.plot(x, previsao, color='red', linewidth=2) # realiza o plto da "linha"
plt.xlabel("MinTemp")
plt.ylabel("MaxTemp")
plt.show()



