#!/usr/bin/python
# -*- coding: utf-8 -*-
from math import inf


def dynamic_programming(weight, quantity, penalty, max_capacity):
    new_matrix = [[0 for _ in range(len(quantity))] for _ in range(max_capacity + 1)] # macierz decyzji xi
    f_matrix = [[inf for _ in range(len(quantity))] for _ in range(max_capacity + 1)] # macierz funkcji f

    for i in range(len(f_matrix[0])):
        for j in range(len(f_matrix)):
            # indeksowanie
            index = len(f_matrix[0]) - i - 1

            # wyliczam maksymalną liczbe przedmiotów
            x = round(j / weight[index])
            if x > quantity[index]:
                x = quantity[index]

            # wyróżniam ostatni etap
            if i == 0:
                new_matrix[j][i] = x
                f_matrix[j][i] = penalty[x][index]
            else:
                # sprawdzam wszystkie możliwe x
                for x2 in range(x + 1):
                    # obliczam koszt
                    cost = penalty[x2][index] + f_matrix[j - weight[index] * x2][i - 1]

                    # jeśli koszt jest mniejszy to uaktualniam macierz f
                    if f_matrix[j][i] > cost:
                        new_matrix[j][i] = x2
                        f_matrix[j][i] = cost
    return new_matrix, f_matrix


def get_results(a, y, x_matrix, f):
    free_space = y
    strategy = list()

    for j in range(len(f[0])-1, -1, -1):

        input_index = len(f[0]) - j - 1
        strategy.append((int(x_matrix[free_space][j]), input_index, f[free_space][j]))
        free_space = int(free_space - a[input_index] * x_matrix[free_space][j])

    return strategy
