import math
import random
import matplotlib.pyplot as plt


# ==========================================
# CIDADES
# ==========================================

cidades = [
    (10, 20),
    (20, 40),
    (30, 10),
    (40, 30),
    (50, 50),
    (60, 20),
    (70, 40),
    (80, 10),
    (90, 30),
    (100, 50)
]


def calcular_distancia(cidade1, cidade2):
    x1, y1 = cidade1
    x2, y2 = cidade2

    return math.sqrt(
        (x2 - x1) ** 2 +
        (y2 - y1) ** 2
    )


def calcular_distancia_rota(rota):

    distancia_total = 0

    for i in range(len(rota) - 1):
        distancia_total += calcular_distancia(
            cidades[rota[i]],
            cidades[rota[i + 1]]
        )

    # Retorno à cidade inicial
    distancia_total += calcular_distancia(
        cidades[rota[-1]],
        cidades[rota[0]]
    )

    return distancia_total


# ==========================================
# RANDOM SEARCH
# ==========================================

def random_search(numero_iteracoes=100):

    melhor_distancia = float("inf")
    historico = []

    for _ in range(numero_iteracoes):

        rota = list(range(len(cidades)))
        random.shuffle(rota)

        distancia = calcular_distancia_rota(rota)

        if distancia < melhor_distancia:
            melhor_distancia = distancia

        historico.append(melhor_distancia)

    return historico


# ==========================================
# ALGORITMO GENÉTICO
# ==========================================

TAMANHO_POPULACAO = 50
TAXA_CROSSOVER = 0.9
TAXA_MUTACAO = 0.2
ELITISMO = 2


def criar_populacao():

    populacao = []

    for _ in range(TAMANHO_POPULACAO):

        individuo = list(range(len(cidades)))
        random.shuffle(individuo)

        populacao.append(individuo)

    return populacao


def selecao_torneio(populacao):

    participantes = random.sample(
        populacao,
        3
    )

    return min(
        participantes,
        key=calcular_distancia_rota
    ).copy()


def crossover_ox(pai1, pai2):

    tamanho = len(pai1)

    inicio, fim = sorted(
        random.sample(range(tamanho), 2)
    )

    filho = [None] * tamanho

    filho[inicio:fim + 1] = pai1[inicio:fim + 1]

    restantes = [
        cidade
        for cidade in pai2
        if cidade not in filho
    ]

    indice = 0

    for i in range(tamanho):

        if filho[i] is None:

            filho[i] = restantes[indice]
            indice += 1

    return filho


def mutacao_inversao(individuo):

    inicio, fim = sorted(
        random.sample(range(len(individuo)), 2)
    )

    individuo[inicio:fim + 1] = reversed(
        individuo[inicio:fim + 1]
    )

    return individuo


def algoritmo_genetico(numero_geracoes=100):

    populacao = criar_populacao()

    melhor_distancia = float("inf")

    historico = []

    for _ in range(numero_geracoes):

        populacao.sort(
            key=calcular_distancia_rota
        )

        distancia = calcular_distancia_rota(
            populacao[0]
        )

        if distancia < melhor_distancia:
            melhor_distancia = distancia

        historico.append(melhor_distancia)

        # Elitismo
        nova_populacao = [
            individuo.copy()
            for individuo in populacao[:ELITISMO]
        ]

        while len(nova_populacao) < TAMANHO_POPULACAO:

            pai1 = selecao_torneio(populacao)
            pai2 = selecao_torneio(populacao)

            if random.random() < TAXA_CROSSOVER:
                filho = crossover_ox(pai1, pai2)
            else:
                filho = pai1.copy()

            if random.random() < TAXA_MUTACAO:
                filho = mutacao_inversao(filho)

            nova_populacao.append(filho)

        populacao = nova_populacao

    return historico


# ==========================================
# ACO
# ==========================================

NUMERO_FORMIGAS = 20
ALPHA = 1.0
BETA = 2.0
EVAPORACAO = 0.5
FEROMONIO_INICIAL = 1.0


def criar_matriz_distancias():

    n = len(cidades)

    matriz = [
        [0.0 for _ in range(n)]
        for _ in range(n)
    ]

    for i in range(n):
        for j in range(n):

            if i != j:
                matriz[i][j] = calcular_distancia(
                    cidades[i],
                    cidades[j]
                )

    return matriz


def escolher_proxima_cidade(
    atual,
    nao_visitadas,
    feromonios,
    matriz
):

    probabilidades = []
    soma = 0

    for cidade in nao_visitadas:

        feromonio = (
            feromonios[atual][cidade] ** ALPHA
        )

        heuristica = (
            1.0 / matriz[atual][cidade]
        ) ** BETA

        valor = feromonio * heuristica

        probabilidades.append(
            (cidade, valor)
        )

        soma += valor

    sorteio = random.random() * soma

    acumulado = 0

    for cidade, valor in probabilidades:

        acumulado += valor

        if acumulado >= sorteio:
            return cidade

    return probabilidades[-1][0]


def construir_rota(feromonios, matriz):

    n = len(cidades)

    atual = random.randrange(n)

    rota = [atual]

    nao_visitadas = set(range(n))
    nao_visitadas.remove(atual)

    while nao_visitadas:

        proxima = escolher_proxima_cidade(
            atual,
            list(nao_visitadas),
            feromonios,
            matriz
        )

        rota.append(proxima)

        nao_visitadas.remove(proxima)

        atual = proxima

    return rota


def algoritmo_aco(numero_iteracoes=100):

    n = len(cidades)

    matriz = criar_matriz_distancias()

    feromonios = [
        [
            FEROMONIO_INICIAL
            for _ in range(n)
        ]
        for _ in range(n)
    ]

    melhor_distancia = float("inf")

    historico = []

    for _ in range(numero_iteracoes):

        rotas = []

        for _ in range(NUMERO_FORMIGAS):

            rota = construir_rota(
                feromonios,
                matriz
            )

            distancia = calcular_distancia_rota(
                rota
            )

            rotas.append(
                (rota, distancia)
            )

            if distancia < melhor_distancia:
                melhor_distancia = distancia

        historico.append(melhor_distancia)

        # Evaporação
        for i in range(n):
            for j in range(n):

                feromonios[i][j] *= (
                    1 - EVAPORACAO
                )

        # Depósito
        for rota, distancia in rotas:

            deposito = 1.0 / distancia

            for i in range(len(rota)):

                cidade1 = rota[i]
                cidade2 = rota[
                    (i + 1) % len(rota)
                ]

                feromonios[cidade1][cidade2] += deposito
                feromonios[cidade2][cidade1] += deposito

    return historico


# ==========================================
# EXECUTAR OS ALGORITMOS
# ==========================================

print("Executando Random Search...")
historico_random = random_search(100)

print("Executando Algoritmo Genético...")
historico_ag = algoritmo_genetico(100)

print("Executando ACO...")
historico_aco = algoritmo_aco(100)


# ==========================================
# GRÁFICO RANDOM SEARCH
# ==========================================

plt.figure()

plt.plot(
    range(1, 101),
    historico_random
)

plt.title("Convergência - Random Search")
plt.xlabel("Iteração")
plt.ylabel("Melhor distância encontrada")
plt.grid()

plt.savefig(
    "convergencia_random_search.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()


# ==========================================
# GRÁFICO ALGORITMO GENÉTICO
# ==========================================

plt.figure()

plt.plot(
    range(1, 101),
    historico_ag
)

plt.title("Convergência - Algoritmo Genético")
plt.xlabel("Geração")
plt.ylabel("Melhor distância encontrada")
plt.grid()

plt.savefig(
    "convergencia_genetico.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()


# ==========================================
# GRÁFICO ACO
# ==========================================

plt.figure()

plt.plot(
    range(1, 101),
    historico_aco
)

plt.title("Convergência - ACO")
plt.xlabel("Iteração")
plt.ylabel("Melhor distância encontrada")
plt.grid()

plt.savefig(
    "convergencia_aco.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()


print("\n================================")
print("GRÁFICOS GERADOS COM SUCESSO!")
print("================================")

print("convergencia_random_search.png")
print("convergencia_genetico.png")
print("convergencia_aco.png")