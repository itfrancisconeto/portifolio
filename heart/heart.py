#importar bibliotecas
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
import seaborn as sns

#titulo
print ('Prever a propensão à doença cardiaca')
print()

#carregar dados para o dataframe
df_heart=pd.read_csv(r'datasets_33180_43520_heart.csv', sep=',')

#verificar os tipos de dados
df_heart.info()

#verificar o shape
print (df_heart.shape)
print()

#verificar quantidade  de instancias nulas por atributo
nans = df_heart.isna().sum()
print(nans[nans > 0])

#separar os atributos idade e frequencia  cardiaca maxima alcançada
df_heart_clean = df_heart[['age','thalach']].copy()

#verificar a correlação entre a idade e a frequencia cardiaca máxima alcançada
plt.figure(figsize=(6,5))
df_corr_ = df_heart_clean.corr()
ax_ = sns.heatmap(df_corr_, annot=True)
bottom, top = ax_.get_ylim()
ax_.set_ylim(bottom + 0.5, top - 0.5)
plt.show()
print()

# Separar os dados entre treino e teste')
X = df_heart.drop('target', axis=1)
Y = df_heart['target']
split_test_size = 0.3 #Definindo a taxa de split
X_treino, X_teste, Y_treino, Y_teste = train_test_split(X, Y, test_size = split_test_size)

#utilizar o modelo Regressão Logística
modelo = LogisticRegression(solver='lbfgs', max_iter=10000) #criar o modelo
modelo.fit(X_treino, Y_treino.ravel()) #treinar o modelo
lr_predict_test = modelo.predict(X_teste) #aplicar predição com os dados de teste

#medir a acuracia do modelo sobre os dados de teste
acuracia = accuracy_score(Y_teste, lr_predict_test)
print('Acurácia da RL: ',acuracia)
print()

#criar Confusion Matrix
print('Matriz de Confusão: ')
print(pd.crosstab(Y_teste,lr_predict_test,rownames=['Real'],colnames=['Predito'],margins=True))
print()

#exibir relatorio de classificação
print('Relatório de Classificação: ')
print(classification_report(Y_teste,lr_predict_test))



