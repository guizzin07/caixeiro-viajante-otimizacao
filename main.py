import math
import random
import statistics
import matplotlib.pyplot as plt

# ==========================================
# PROBLEMA DO CAIXEIRO VIAJANTE
# ==========================================

# Coordenadas das cidades
# o código define 10 cidades por coordenadas (x, y)
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

# distância euclidiana para descobrir a distância entre duas cidades
# Calcula a distância entre duas cidades
def calcular_distancia(cidade1, cidade2):
    x1, y1 = cidade1
    x2, y2 = cidade2

    return math.sqrt(
        (x2 - x1) ** 2 +
        (y2 - y1) ** 2
    )

# soma todas as distâncias de uma rota e, no final, calcula o caminho da última cidade de volta para a primeira
# Calcula a distância total de uma rota
def calcular_distancia_rota(rota):

    distancia_total = 0

    for i in range(len(rota) - 1):

        cidade_atual = cidades[rota[i]]
        proxima_cidade = cidades[rota[i + 1]]

        distancia_total += calcular_distancia(
            cidade_atual,
            proxima_cidade
        )

    # Retorno para a cidade inicial
    distancia_total += calcular_distancia(
        cidades[rota[-1]],
        cidades[rota[0]]
    )

    return distancia_total


# ==========================================
# RANDOM SEARCH
# ==========================================

def random_search(numero_iteracoes=100):

    melhor_rota = None
    melhor_distancia = float("inf")

    historico = []

    for iteracao in range(numero_iteracoes):
# Calcula a distância e compara com a melhor encontrada até aquele momento. Se for menor, substitui a melhor rota.
        
        rota = list(range(len(cidades)))
        random.shuffle(rota)

        distancia = calcular_distancia_rota(rota)

        if distancia < melhor_distancia:
            melhor_distancia = distancia
            melhor_rota = rota.copy()

        # Guarda a melhor distância da iteração
        historico.append(melhor_distancia)

        print(
            f"Iteração {iteracao + 1}: "
            f"Melhor distância = {melhor_distancia:.2f}"
        )

    return melhor_rota, melhor_distancia, historico


# Executando o Random Search
# ==========================================
# 10 EXECUÇÕES DO RANDOM SEARCH
# ==========================================

resultados_random = []
melhor_resultado_geral = float("inf")
melhor_rota_geral = None

for execucao in range(10):

    print(f"\nEXECUÇÃO {execucao + 1}")

    melhor_rota, melhor_distancia = random_search(100)

    resultados_random.append(melhor_distancia)

    if melhor_distancia < melhor_resultado_geral:
        melhor_resultado_geral = melhor_distancia
        melhor_rota_geral = melhor_rota.copy()


# Calculando média e desvio padrão
media_random = statistics.mean(resultados_random)
desvio_random = statistics.stdev(resultados_random)


print("\n================================")
print("RESULTADOS FINAIS - RANDOM SEARCH")
print("================================")

for i, resultado in enumerate(resultados_random):
    print(f"Execução {i + 1}: {resultado:.2f}")

print("--------------------------------")
print(f"Média: {media_random:.2f}")
print(f"Desvio padrão: {desvio_random:.2f}")
print(f"Melhor resultado: {melhor_resultado_geral:.2f}")
print(f"Melhor rota: {melhor_rota_geral}")
# ==========================================
# ALGORITMO GENÉTICO
# ==========================================
# Ou seja:
# População = 50: existem 50 soluções candidatas.
# Crossover = 90%: grande chance de combinar duas rotas.
# Mutação = 20%: chance de alterar uma rota.
# Elitismo = 2: as duas melhores soluções são preservadas.

TAMANHO_POPULACAO = 50
TAXA_CROSSOVER = 0.9
TAXA_MUTACAO = 0.2
ELITISMO = 2


# Cria a população inicial
def criar_populacao(tamanho):
    populacao = []

    for _ in range(tamanho):
        individuo = list(range(len(cidades)))
        random.shuffle(individuo)
        populacao.append(individuo)

    return populacao


# Seleção por torneio
def selecao_torneio(populacao, tamanho_torneio=3):

    participantes = random.sample(
        populacao,
        tamanho_torneio
    )
# O código escolhe 3 indivíduos aleatoriamente e pega o melhor deles:
    melhor = min(
        participantes,
        key=calcular_distancia_rota
    )

    return melhor.copy()


# Order Crossover (OX)
def crossover_ox(pai1, pai2):

    tamanho = len(pai1)

    inicio, fim = sorted(
        random.sample(range(tamanho), 2)
    )

    filho = [None] * tamanho

    # Copia um trecho do primeiro pai
    filho[inicio:fim + 1] = pai1[inicio:fim + 1]

    # Pega as cidades do segundo pai
    # que ainda não estão no filho
    restantes = [
        cidade
        for cidade in pai2
        if cidade not in filho
    ]

    indice_restantes = 0

    for i in range(tamanho):
        if filho[i] is None:
            filho[i] = restantes[indice_restantes]
            indice_restantes += 1

    return filho


# Mutação por inversão
def mutacao_inversao(individuo):

    inicio, fim = sorted(
        random.sample(range(len(individuo)), 2)
    )

    individuo[inicio:fim + 1] = reversed(
        individuo[inicio:fim + 1]
    )

    return individuo


# ==========================================
# EXECUÇÃO DO ALGORITMO GENÉTICO
# ==========================================

def algoritmo_genetico(numero_geracoes=100):

    populacao = criar_populacao(TAMANHO_POPULACAO)

    melhor_rota = None
    melhor_distancia = float("inf")

    for geracao in range(numero_geracoes):

        # Ordena do melhor para o pior
        populacao.sort(
            key=calcular_distancia_rota
        )

        distancia_atual = calcular_distancia_rota(
            populacao[0]
        )

        # Guarda o melhor resultado encontrado
        if distancia_atual < melhor_distancia:
            melhor_distancia = distancia_atual
            melhor_rota = populacao[0].copy()

        # ELITISMO
        nova_populacao = [
            individuo.copy()
            for individuo in populacao[:ELITISMO]
        ]

        # Cria os demais indivíduos
        while len(nova_populacao) < TAMANHO_POPULACAO:

            pai1 = selecao_torneio(populacao)
            pai2 = selecao_torneio(populacao)

            # CROSSOVER
            if random.random() < TAXA_CROSSOVER:
                filho = crossover_ox(pai1, pai2)
            else:
                filho = pai1.copy()

            # MUTAÇÃO
            if random.random() < TAXA_MUTACAO:
                filho = mutacao_inversao(filho)

            nova_populacao.append(filho)

        populacao = nova_populacao

        print(
            f"Geração {geracao + 1}: "
            f"Melhor distância = {melhor_distancia:.2f}"
        )

    # Verificação final
    populacao.sort(
        key=calcular_distancia_rota
    )

    distancia_final = calcular_distancia_rota(
        populacao[0]
    )

    if distancia_final < melhor_distancia:
        melhor_distancia = distancia_final
        melhor_rota = populacao[0].copy()

    return melhor_rota, melhor_distancia


# ==========================================
# TESTE DO ALGORITMO GENÉTICO
# ==========================================

# ==========================================
# 10 EXECUÇÕES DO ALGORITMO GENÉTICO
# ==========================================

resultados_ag = []
melhor_resultado_ag = float("inf")
melhor_rota_ag_geral = None

for execucao in range(10):

    print(f"\nEXECUÇÃO {execucao + 1} - ALGORITMO GENÉTICO")

    melhor_rota, melhor_distancia = algoritmo_genetico(100)

    resultados_ag.append(melhor_distancia)

    if melhor_distancia < melhor_resultado_ag:
        melhor_resultado_ag = melhor_distancia
        melhor_rota_ag_geral = melhor_rota.copy()


# Calculando média e desvio padrão
media_ag = statistics.mean(resultados_ag)
desvio_ag = statistics.stdev(resultados_ag)


print("\n========================================")
print("RESULTADOS FINAIS - ALGORITMO GENÉTICO")
print("========================================")

for i, resultado in enumerate(resultados_ag):
    print(f"Execução {i + 1}: {resultado:.2f}")

print("----------------------------------------")
print(f"Média: {media_ag:.2f}")
print(f"Desvio padrão: {desvio_ag:.2f}")
print(f"Melhor resultado: {melhor_resultado_ag:.2f}")
print(f"Melhor rota: {melhor_rota_ag_geral}")
# ==========================================
# ACO - COLÔNIA DE FORMIGAS
# ==========================================

NUMERO_FORMIGAS = 20
ALPHA = 1.0
BETA = 2.0
EVAPORACAO = 0.5
FEROMONIO_INICIAL = 1.0


# Cria a matriz de distâncias entre as cidades
def criar_matriz_distancias():

    numero_cidades = len(cidades)

    matriz = [
        [0.0 for _ in range(numero_cidades)]
        for _ in range(numero_cidades)
    ]

    for i in range(numero_cidades):
        for j in range(numero_cidades):

            if i != j:
                matriz[i][j] = calcular_distancia(
                    cidades[i],
                    cidades[j]
                )

    return matriz


# Escolhe a próxima cidade com base
# no feromônio e na distância
def escolher_proxima_cidade(
    cidade_atual,
    cidades_nao_visitadas,
    feromonios,
    matriz_distancias
):

    probabilidades = []
    soma = 0

    for cidade in cidades_nao_visitadas:

        feromonio = (
            feromonios[cidade_atual][cidade] ** ALPHA
        )

        distancia = matriz_distancias[cidade_atual][cidade]

        heuristica = (1.0 / distancia) ** BETA

        valor = feromonio * heuristica

        probabilidades.append(
            (cidade, valor)
        )

        soma += valor

    # Escolha proporcional à probabilidade
    sorteio = random.random() * soma

    acumulado = 0

    for cidade, valor in probabilidades:

        acumulado += valor

        if acumulado >= sorteio:
            return cidade

    return probabilidades[-1][0]


# Constrói a rota de uma formiga
def construir_rota(
    feromonios,
    matriz_distancias
):

    numero_cidades = len(cidades)

    # Cidade inicial aleatória
    cidade_atual = random.randrange(numero_cidades)

    rota = [cidade_atual]

    cidades_nao_visitadas = set(
        range(numero_cidades)
    )

    cidades_nao_visitadas.remove(
        cidade_atual
    )

    while cidades_nao_visitadas:

        proxima_cidade = escolher_proxima_cidade(
            cidade_atual,
            list(cidades_nao_visitadas),
            feromonios,
            matriz_distancias
        )

        rota.append(proxima_cidade)

        cidades_nao_visitadas.remove(
            proxima_cidade
        )

        cidade_atual = proxima_cidade

    return rota


# ==========================================
# ALGORITMO ACO
# ==========================================

def algoritmo_aco(numero_iteracoes=100):

    numero_cidades = len(cidades)

    matriz_distancias = criar_matriz_distancias()

    # Matriz inicial de feromônios
    feromonios = [
        [
            FEROMONIO_INICIAL
            for _ in range(numero_cidades)
        ]
        for _ in range(numero_cidades)
    ]

    melhor_rota = None
    melhor_distancia = float("inf")

    for iteracao in range(numero_iteracoes):

        rotas_formigas = []

        # Cada formiga constrói uma rota
        for _ in range(NUMERO_FORMIGAS):

            rota = construir_rota(
                feromonios,
                matriz_distancias
            )

            distancia = calcular_distancia_rota(
                rota
            )

            rotas_formigas.append(
                (rota, distancia)
            )

            # Guarda a melhor solução
            if distancia < melhor_distancia:

                melhor_distancia = distancia
                melhor_rota = rota.copy()

        # ==================================
        # EVAPORAÇÃO DO FEROMÔNIO
        # ==================================

        for i in range(numero_cidades):
            for j in range(numero_cidades):

                feromonios[i][j] *= (
                    1 - EVAPORACAO
                )

        # ==================================
        # DEPÓSITO DE FEROMÔNIO
        # ==================================

        for rota, distancia in rotas_formigas:

            quantidade_feromonio = (
                1.0 / distancia
            )

            for i in range(len(rota)):

                cidade1 = rota[i]

                cidade2 = rota[
                    (i + 1) % len(rota)
                ]

                feromonios[cidade1][cidade2] += (
                    quantidade_feromonio
                )

                feromonios[cidade2][cidade1] += (
                    quantidade_feromonio
                )

        print(
            f"Iteração {iteracao + 1}: "
            f"Melhor distância = "
            f"{melhor_distancia:.2f}"
        )

    return melhor_rota, melhor_distancia


# ==========================================
# TESTE DO ACO
# ==========================================

print("\n================================")
print("ACO - COLÔNIA DE FORMIGAS")
print("================================")

melhor_rota_aco, melhor_distancia_aco = algoritmo_aco(100)

# ==========================================
# 10 EXECUÇÕES DO ACO
# ==========================================

resultados_aco = []
melhor_resultado_aco = float("inf")
melhor_rota_aco_geral = None

for execucao in range(10):

    print(f"\nEXECUÇÃO {execucao + 1} - ACO")

    melhor_rota, melhor_distancia = algoritmo_aco(100)

    resultados_aco.append(melhor_distancia)

    if melhor_distancia < melhor_resultado_aco:
        melhor_resultado_aco = melhor_distancia
        melhor_rota_aco_geral = melhor_rota.copy()


# Calculando média e desvio padrão
media_aco = statistics.mean(resultados_aco)
desvio_aco = statistics.stdev(resultados_aco)


print("\n================================")
print("RESULTADOS FINAIS - ACO")
print("================================")

for i, resultado in enumerate(resultados_aco):
    print(f"Execução {i + 1}: {resultado:.2f}")

print("--------------------------------")
print(f"Média: {media_aco:.2f}")
print(f"Desvio padrão: {desvio_aco:.2f}")
print(f"Melhor resultado: {melhor_resultado_aco:.2f}")
print(f"Melhor rota: {melhor_rota_aco_geral}")
