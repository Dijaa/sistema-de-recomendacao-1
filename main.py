import json
import random
from scipy.spatial.distance import euclidean
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics import mean_squared_error

import numpy as np

# Carregar o dataset a partir de um arquivo JSON
data = json.load(open("avaliacoes.json"))


# Função para dividir o dataset em treinamento e teste
def dividir_treino_teste(data, proporcao_teste=0.2):
    usuarios = list(data.keys())
    random.shuffle(usuarios)

    indice_divisao = int(len(usuarios) * (1 - proporcao_teste))
    usuarios_treino = usuarios[:indice_divisao]
    usuarios_teste = usuarios[indice_divisao:]

    dados_treino = {usuario: data[usuario] for usuario in usuarios_treino}
    dados_teste = {usuario: data[usuario] for usuario in usuarios_teste}

    return dados_treino, dados_teste


dados_treino, dados_teste = dividir_treino_teste(data, proporcao_teste=0.2)


# Funções para calcular a similaridade cosseno e a distância euclidiana
def obter_itens_comuns(usuario1, usuario2):
    return {
        item: (usuario1[item], usuario2[item]) for item in usuario1 if item in usuario2
    }


def similaridade_cosseno(usuario1, usuario2):
    comuns = obter_itens_comuns(usuario1, usuario2)
    if not comuns:
        return 0
    avaliacoes1, avaliacoes2 = zip(*comuns.values())
    return cosine_similarity([avaliacoes1], [avaliacoes2])[0][0]


def distancia_euclidiana(usuario1, usuario2):
    comuns = obter_itens_comuns(usuario1, usuario2)
    if not comuns:
        return 0
    avaliacoes1, avaliacoes2 = zip(*comuns.values())
    return 1 / (1 + euclidean(avaliacoes1, avaliacoes2))


# Função para prever a avaliação de um item
def prever_avaliacao(data, usuario_id, item_id, metodo="cosine"):
    soma_similaridade = 0
    soma_ponderada = 0
    usuario_alvo = data[usuario_id]

    for outro_usuario in data:
        if outro_usuario == usuario_id or item_id not in data[outro_usuario]:
            continue
        if metodo == "cosine":
            similaridade = similaridade_cosseno(usuario_alvo, data[outro_usuario])
        else:
            similaridade = distancia_euclidiana(usuario_alvo, data[outro_usuario])

        if similaridade > 0:
            soma_ponderada += similaridade * data[outro_usuario][item_id]
            soma_similaridade += similaridade

    if soma_similaridade == 0:
        return 0

    return soma_ponderada / soma_similaridade


# Função para calcular o RMSE
def calcular_rmse(data, metodo="cosine"):
    previsoes = []
    reais = []

    for usuario in data:
        for item in data[usuario]:
            avaliacao_real = data[usuario][item]
            avaliacao_prevista = prever_avaliacao(data, usuario, item, metodo)
            if avaliacao_prevista != 0:
                previsoes.append(avaliacao_prevista)
                reais.append(avaliacao_real)

    return np.sqrt(mean_squared_error(reais, previsoes))


# Calcular o RMSE para Similaridade Cosseno e Distância Euclidiana
rmse_cosseno = calcular_rmse(dados_teste, metodo="cosine")
rmse_euclidiana = calcular_rmse(dados_teste, metodo="euclidean")

print(f"RMSE Similaridade Cosseno: {rmse_cosseno}")
print(f"RMSE Distância Euclidiana: {rmse_euclidiana}")
