from math import inf


def dynamic_programming(production_cost, storage_cost, demand, y_min, y_max, y_start, y_end):
    # macierz stanów
    new_matrix = [[0 for _ in range(len(demand))] for _ in range(y_max - y_min + 1)] # macierz decyzji xi

    # macierz funkcji celu
    f_matrix = [[inf for _ in range(len(demand))] for _ in range(y_max - y_min + 1)] # macierz funkcji f

    # dopuszczalne przedmioty w magazynie
    y = []
    for i in range(y_min, y_max + 1):
        y.append(i)

    # i - kolejne etapy (miesiące)
    # j - kolejne stany w danym etapie (kolejne decyzje)
    for i in range(len(f_matrix[0])):
        for j in range(len(f_matrix)):
            # indeksowanie
            index = len(f_matrix[0]) - i - 1

            # wyróżniam ostatni etap
            if i == 0:
                x_min = y_end + demand[index] - y[j]
                x_max = y_end + demand[index] - y[j]
            else:
                x_min = max(y_min + demand[index] - y[j], 0)
                x_max = min(y_max + demand[index] - y[j], len(production_cost) - 1)
            if x_min > x_max or x_min < 0 or x_max < 0 or x_max > len(production_cost) - 1:
                new_matrix[j][i] = None
                f_matrix[j][i] = inf
                continue

            # sprawdzam wszystkie możliwe x
            for x2 in range(x_min, x_max + 1):
                # obliczam koszt
                if i != 0:
                    cost = production_cost[x2] + storage_cost[y[j] + x2 - demand[index] - y_min] + f_matrix[y[j] + x2 - demand[index] - y_min][i - 1]
                else:
                    cost = production_cost[x2]
                # jeśli koszt jest mniejszy to uaktualniam macierz f
                if f_matrix[j][i] > cost:
                    new_matrix[j][i] = x2
                    f_matrix[j][i] = cost
    return new_matrix, f_matrix


def get_results(q, y_min, y_begining, x_matrix, f):
    state = y_begining
    strategy = f"Total cost = {f[y_begining - y_min][-1]}\n"
    for j in range(len(f[0]) - 1, -1, -1):
        input_index = len(f[0]) - j - 1
        decision = int(x_matrix[state - y_min][j])
        strategy += f"{state}, {decision}\n"
        state = int(state + decision - q[input_index])
    strategy += f"|y{len(q)} = {state}|\n"
    return strategy

    return strategy
