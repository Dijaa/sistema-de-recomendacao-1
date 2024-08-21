from math import sqrt
import json


with open("avaliacoes.json", "r") as f:
    avaliacoes = json.load(f)


def dist_euclidiana(usuario1, usuario2):
    sim = {}
    for item in avaliacoes[usuario1]:
        if item in avaliacoes[usuario2]:
            sim[item] = 1

    if len(sim) == 0:
        return 0

    distancia = sum(
        [
            pow(avaliacoes[usuario1][item] - avaliacoes[usuario2][item], 2)
            for item in avaliacoes[usuario1]
            if item in avaliacoes[usuario2]
        ]
    )

    # print(distancia)

    # similaridade 👇
    return 1 / (1 + sqrt(distancia))


def calc_similaridades(alvo):
    similaridades = [
        (dist_euclidiana(alvo, usuario2), usuario2)
        for usuario2 in avaliacoes
        if usuario2 != alvo
    ]

    return similaridades


# calc_similaridades('Paulo')
# dist_euclidiana('Paulo', 'Mauro')


def calc_recomendacoes(alvo):
    totais = {}
    soma_sim = {}
    for usuario2 in avaliacoes:
        if usuario2 == alvo:
            continue
        similaridade = dist_euclidiana(alvo, usuario2)

        if similaridade <= 0:
            continue

        for item in avaliacoes[usuario2]:
            if item not in avaliacoes[alvo]:
                totais.setdefault(item, 0)
                totais[item] += avaliacoes[usuario2][item] * similaridade
                soma_sim.setdefault(item, 0)
                soma_sim[item] += similaridade

    ranking = [(total / soma_sim[item], item) for item, total in totais.items()]
    ranking.sort()
    ranking.reverse()

    return ranking


print(calc_recomendacoes("User1000"))
