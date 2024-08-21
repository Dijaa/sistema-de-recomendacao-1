import random

# Dados iniciais
avaliacoes = {
    "Paulo": {
        "Filme1": 3.0,
        "Filme2": 3.5,
        "Filme3": 1.5,
        "Filme4": 5.0,
        "Filme5": 3.0,
        "Filme6": 3.5,
    },
    "Joao": {"Filme1": 2.5, "Filme2": 3.0, "Filme4": 3.5, "Filme6": 4.0},
    "Marcia": {
        "Filme2": 3.5,
        "Filme3": 3.0,
        "Filme4": 4.0,
        "Filme5": 2.5,
        "Filme6": 4.5,
    },
    "Carlos": {
        "Filme1": 3.0,
        "Filme2": 4.0,
        "Filme4": 5.0,
        "Filme5": 3.5,
        "Filme6": 3.0,
    },
    "Ana": {
        "Filme1": 2.5,
        "Filme2": 3.5,
        "Filme3": 3.0,
        "Filme4": 3.5,
        "Filme5": 2.5,
        "Filme6": 3.0,
    },
    "Mauro": {"Filme2": 4.0, "Filme4": 4.0, "Filme5": 1.0},
}

# Lista de filmes
filmes = ["Filme1", "Filme2", "Filme3", "Filme4", "Filme5", "Filme6"]


# Função para gerar uma avaliação similar com variação
def gerar_avaliacao_similar(user_avaliacoes):
    max_filmes = len(
        user_avaliacoes
    )  # Número máximo de filmes que o usuário base avaliou
    # Pesos ajustados para número de filmes avaliados
    pesos = [10, 30, 30, 20, 10]
    # Ajusta os pesos para que correspondam ao número de filmes disponíveis
    pesos = pesos[:max_filmes] if max_filmes <= len(pesos) else [10] * max_filmes
    num_filmes = random.choices(range(1, max_filmes + 1), weights=pesos, k=1)[0]

    filmes_selecionados = random.sample(list(user_avaliacoes.keys()), num_filmes)
    return {
        filme: round(
            min(
                5.0,
                max(
                    1.0,
                    round(
                        random.uniform(
                            user_avaliacoes[filme] - 1, user_avaliacoes[filme] + 1
                        )
                        * 2
                    )
                    / 2,
                ),
            ),
            1,
        )
        for filme in filmes_selecionados
    }


# Expandindo o dataset
for i in range(7, 1001):
    user = f"User{i}"
    user_base = random.choice(list(avaliacoes.keys()))  # Escolhe um usuário existente
    avaliacoes[user] = gerar_avaliacao_similar(avaliacoes[user_base])

# Exibindo alguns exemplos
for user, user_avaliacoes in list(avaliacoes.items())[:1000]:
    print(f"{user}: {user_avaliacoes}")

# Salvando o dataset
import json

with open("avaliacoes.json", "w") as f:
    json.dump(avaliacoes, f)
