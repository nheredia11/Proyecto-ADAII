import math
from typing import List, Tuple
from itertools import product

# Función para leer los datos de entrada desde un archivo
def read_input(file_path: str) -> Tuple[List[Tuple[float, float]], float]:
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    # Leer el número de agentes
    n = int(lines[0].strip())
    
    # Leer los agentes
    agents = [tuple(map(float, line.strip().split(','))) for line in lines[1:n+1]]
    
    # Leer el valor máximo de esfuerzo
    Rmax = float(lines[n + 1].strip())
    
    return agents, Rmax

# Función para calcular el extremismo dado un conjunto de agentes
def calculate_extremism(agents: List[Tuple[float, float]]) -> float:
    n = len(agents)
    sum_of_squares = sum(op ** 2 for op, _ in agents)
    return math.sqrt(sum_of_squares) / n

# Función para calcular el esfuerzo necesario para moderar a un agente
def calculate_effort(op: float, recp: float) -> int:
    return math.ceil(abs(op) * (1 - recp))

# Función para calcular la reducción del extremismo de un agente
def calculate_reduction(op: float, recp: float) -> float:
    return abs(op) * recp

# Aplicar una estrategia a los agentes
def apply_strategy(agents: List[Tuple[float, float]], strategy: List[int]) -> List[Tuple[float, float]]:
    return [(0, recp) if mod else (op, recp) for (op, recp), mod in zip(agents, strategy)]

# Evaluar una estrategia basada en el extremismo
def evaluate_strategy(agents: List[Tuple[float, float]], strategy: List[int], Rmax: float, memo_extremism: dict) -> float:
    effort = 0
    for i, (op, recp) in enumerate(agents):
        if strategy[i]:
            effort += calculate_effort(op, recp)
            if effort > Rmax:
                return float('inf')  # Terminación anticipada si se excede Rmax
    
    strategy_key = tuple(strategy)
    if strategy_key in memo_extremism:
        return memo_extremism[strategy_key]
    
    modified_agents = apply_strategy(agents, strategy)
    extremism = calculate_extremism(modified_agents)
    memo_extremism[strategy_key] = extremism
    return extremism

# Estrategia Voraz con ajuste marginal
def modexV(agents: List[Tuple[float, float]], Rmax: float) -> Tuple[List[int], int, float]:
    n = len(agents)
    total_effort = 0
    selected_agents = [0] * n
    current_extremism = calculate_extremism(agents)
    
    # Calcular reducciones y esfuerzos
    reductions = [(calculate_reduction(op, recp), calculate_effort(op, recp), idx) for idx, (op, recp) in enumerate(agents)]
    
    # Filtrar agentes con esfuerzo cero
    reductions = [(reduction, effort, idx) for reduction, effort, idx in reductions if effort > 0]
    
    # Ordenar por relación reducción/esfuerzo
    reductions.sort(key=lambda x: x[0] / x[1], reverse=True)
    
    for reduction, effort, idx in reductions:
        if total_effort + effort <= Rmax:
            total_effort += effort
            selected_agents[idx] = 1

            modified_agents = apply_strategy(agents, selected_agents)
            new_extremism = calculate_extremism(modified_agents)

            if new_extremism < current_extremism:
                current_extremism = new_extremism
            else:
                total_effort -= effort
                selected_agents[idx] = 0  # Revertir selección
    
    return selected_agents, total_effort, current_extremism

# Algoritmo basado en programación dinámica
def modexPD(agents: List[Tuple[float, float]], Rmax: float) -> Tuple[List[int], int, float]:
    n = len(agents)
    efforts = [calculate_effort(op, recp) for op, recp in agents]
    
    dp = [[float('inf')] * (int(Rmax) + 1) for _ in range(n + 1)]
    dp[0][0] = 0
    
    for i in range(1, n + 1):
        op, _ = agents[i-1]
        for j in range(int(Rmax) + 1):
            dp[i][j] = dp[i-1][j] + op**2  # No seleccionamos al agente i-1
            if j >= efforts[i-1]:
                dp[i][j] = min(dp[i][j], dp[i-1][j-efforts[i-1]])
    
    min_sum_squares = min(dp[n])
    total_effort = dp[n].index(min_sum_squares)
    final_extremism = math.sqrt(min_sum_squares) / n
    
    selected_agents = [0] * n
    j = total_effort
    for i in range(n, 0, -1):
        op, _ = agents[i-1]
        if j >= efforts[i-1] and dp[i][j] == dp[i-1][j-efforts[i-1]]:
            selected_agents[i-1] = 1
            j -= efforts[i-1]
    
    return selected_agents, total_effort, final_extremism

# Algoritmo Fuerza Bruta
def modexFB(agents: List[Tuple[float, float]], Rmax: float) -> Tuple[List[int], float]:
    best_strategy = None
    best_extremism = float('inf')
    best_total_effort = 0
    memo_extremism = {}

    for strategy in product([0, 1], repeat=len(agents)):
        effort = sum(calculate_effort(op, recp) for (op, recp), mod in zip(agents, strategy) if mod)
        if effort <= Rmax:
            extremism = evaluate_strategy(agents, strategy, Rmax, memo_extremism)
            if extremism < best_extremism:
                best_extremism = extremism
                best_strategy = strategy
                best_total_effort = effort
    
    return best_strategy, best_total_effort, best_extremism

# Ejemplo de uso
if __name__ == "__main__":
    file_path = 'Prueba2.txt'  # Cambia el nombre del archivo según corresponda
    agents, Rmax = read_input(file_path)
    
    print("=== Algoritmo Voraz ===")
    best_strategy_v, total_effort_v, final_extremism_v = modexV(agents, Rmax)
    print("Best strategy:", best_strategy_v)
    print("Total effort:", total_effort_v)
    print("Final extremism:", final_extremism_v)

    print("\n=== Algoritmo PD ===")
    best_strategy_pd, total_effort_pd, final_extremism_pd = modexPD(agents, Rmax)
    print("Best strategy:", best_strategy_pd)
    print("Total effort:", total_effort_pd)
    print("Final extremism:", final_extremism_pd)


    print("\n=== Algoritmo Fuerza Bruta ===")
    best_strategy_FB, total_effort_FB, best_extremism_FB = modexFB(agents, Rmax)
    print("Best strategy:", best_strategy_FB)
    print("Total effort:", total_effort_FB)
    print("Final extremism:", best_extremism_FB)

