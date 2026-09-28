# 🚚 Otimização do Problema do Caixeiro Viajante

Projeto desenvolvido com o objetivo de implementar e comparar diferentes estratégias de otimização aplicadas ao **Problema do Caixeiro Viajante (PCV)**.

O problema consiste em encontrar uma rota que visite todas as cidades uma única vez, retornando à cidade de origem e buscando minimizar a distância total percorrida.

## 📌 Algoritmos implementados

Foram implementados três métodos de otimização:

- Random Search (Otimização Aleatória)
- Algoritmo Genético
- Ant Colony Optimization (ACO)

Todos os algoritmos utilizam a mesma instância do Problema do Caixeiro Viajante, composta por **10 cidades**.

## 🗺️ Representação do problema

As cidades são representadas através de coordenadas `(x, y)`.

A distância entre duas cidades é calculada utilizando a distância euclidiana:

```text
d = √((x₂ - x₁)² + (y₂ - y₁)²)
```

O objetivo é encontrar a rota com a **menor distância total possível**, considerando também o retorno da última cidade para a cidade inicial.

## 🎲 Random Search

O Random Search gera rotas aleatórias e mantém a melhor solução encontrada durante as iterações.

Configuração utilizada:

- 100 iterações por execução
- 10 execuções independentes
- 1 nova solução avaliada por iteração

## 🧬 Algoritmo Genético

O Algoritmo Genético utiliza uma população de possíveis rotas que evoluem durante as gerações.

Parâmetros utilizados:

- População: 50 indivíduos
- Gerações: 100
- Seleção: torneio
- Tamanho do torneio: 3 indivíduos
- Crossover: Order Crossover (OX)
- Taxa de crossover: 90%
- Mutação: inversão
- Taxa de mutação: 20%
- Elitismo: 2 indivíduos
- Execuções independentes: 10

## 🐜 Ant Colony Optimization (ACO)

O ACO utiliza o comportamento de uma colônia de formigas como estratégia para encontrar rotas de menor distância.

Parâmetros utilizados:

- Número de formigas: 20
- Iterações: 100
- Alpha (α): 1.0
- Beta (β): 2.0
- Taxa de evaporação: 0.5
- Feromônio inicial: 1.0
- Execuções independentes: 10

## 📊 Resultados

Foram realizadas **10 execuções independentes para cada algoritmo**, utilizando 100 iterações ou gerações em cada execução.

No total foram realizadas **30 execuções**.

| Algoritmo | Média | Desvio padrão | Melhor resultado |
|---|---:|---:|---:|
| Random Search | 318.20 | 17.11 | 295.97 |
| Algoritmo Genético | 242.13 | 0.00 | 242.13 |
| ACO | 242.13 | 0.00 | 242.13 |

Para a instância e os parâmetros utilizados, o Algoritmo Genético e o ACO apresentaram menores distâncias e menor variabilidade que o Random Search.

## 📈 Gráficos de convergência

Também foram gerados gráficos mostrando a evolução da melhor distância encontrada durante as 100 iterações ou gerações.

Os arquivos gerados são:

```text
convergencia_random_search.png
convergencia_genetico.png
convergencia_aco.png
```

Os gráficos permitem visualizar o comportamento de convergência dos três métodos.

## 🛠️ Tecnologias utilizadas

- Python
- Matplotlib
- Visual Studio Code

## ▶️ Como executar

Clone o repositório:

```bash
git clone URL_DO_REPOSITORIO
```

Entre na pasta:

```bash
cd caixeiro-viajante-otimizacao
```

Instale o Matplotlib:

```bash
pip install matplotlib
```

Execute os experimentos:

```bash
python main.py
```

Para gerar os gráficos:

```bash
python graficos.py
```

## 📁 Estrutura do projeto

```text
caixeiro-viajante-otimizacao/
│
├── main.py
├── graficos.py
├── convergencia_random_search.png
├── convergencia_genetico.png
├── convergencia_aco.png
└── README.md
```

## 🎯 Objetivo acadêmico

O projeto foi desenvolvido para analisar experimentalmente diferentes estratégias de otimização aplicadas ao Problema do Caixeiro Viajante, comparando a qualidade e a estabilidade das soluções obtidas por cada método.