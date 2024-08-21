from math import sqrt
import json

with open("avaliacoes.json", "r") as f:
    avaliacoes = json.load(f)


def sim_cosseno(usuario1, usuario2):
    # Identificar os itens em comum
    itens_comuns = {}
    for item in avaliacoes[usuario1]:
        if item in avaliacoes[usuario2]:
            itens_comuns[item] = 1

    # Se não houver itens em comum, retornar similaridade zero
    if len(itens_comuns) == 0:
        return 0

    # Calcular os componentes necessários para a similaridade do cosseno
    soma_produto = sum(
        [
            avaliacoes[usuario1][item] * avaliacoes[usuario2][item]
            for item in itens_comuns
        ]
    )
    soma_quad_usuario1 = sum(
        [pow(avaliacoes[usuario1][item], 2) for item in itens_comuns]
    )
    soma_quad_usuario2 = sum(
        [pow(avaliacoes[usuario2][item], 2) for item in itens_comuns]
    )

    # Calcular a similaridade do cosseno
    denominador = sqrt(soma_quad_usuario1) * sqrt(soma_quad_usuario2)

    if denominador == 0:
        return 0

    return soma_produto / denominador


def calc_similaridades_cosseno(alvo):
    similaridades = [
        (sim_cosseno(alvo, usuario2), usuario2)
        for usuario2 in avaliacoes
        if usuario2 != alvo
    ]
    return similaridades


def calc_recomendacoes_cosseno(alvo):
    totais = {}
    soma_sim = {}
    for usuario2 in avaliacoes:
        if usuario2 == alvo:
            continue
        similaridade = sim_cosseno(alvo, usuario2)

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


print(calc_recomendacoes_cosseno("User1000"))
