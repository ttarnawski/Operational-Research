#!/usr/bin/python
# -*- coding: utf-8 -*-
from math import inf


def g_tsp(G, w):
    E = {}     # słownik postaci - (wierzchołek początkowy: wierzchołek końcowy)
    suma = 0   # sumaryczna długość cyklu Hamiltona

    # pętla wykonuje się do momentu, aż ostateczne rozwiązanie będzie miało tyle samo krawędzi ile jest wierzchołków
    while len(E.keys()) < len(G.keys()):

        # sprawdzam czy w macierzy wag występuje jeszcze jakaś wartość liczbowa
        no_inf_exists = False
        for i in range(len(w)):
            for j in range(len(w)):
                if w[i][j] != inf:
                    no_inf_exists = True
                    break                           # jeśli nie i ilość krawędzi jest mniejsza od licby wierzchołków
            if no_inf_exists is True:               # to niemożliwe jest wyznaczenie tsp
                break
        if no_inf_exists is False and len(E.keys()) < len(G.keys()):
            print('Nie można wyznaczyć rozwiązania')
            return None

        # poszukiwanie krawędzi z najmniejszą wagą
        min_value = inf
        for i in range(len(w)):
            for j in range(len(w)):
                if w[i][j] < min_value:
                    min_value = w[i][j]
                    row = i
                    col = j

        w[row][col] = inf    # usuwam krawędź z macierzy wag

        # sprawdzam, czy w rozwiązaniu nie powtarza się wierzchołek początkowy lub końcowy
        if row in E.keys() or col in E.values():
            continue

        # sprawdzam czy nie tworzę podcyklu, wykluczam przypadki jeśli jest to ostania iteracja
        if col in E.keys() and row in E.values() and (len(E.keys()) < len(G.keys()) - 1):
            path_exist = False
            current = col
            for i in range(len(E.keys())):
                if current not in E.keys():
                    break
                current = E[current]
                if current == row:
                    path_exist = True
            if path_exist is True:
                continue

        E[row] = col     # dodaję krawędź do rozwiązania
        suma += min_value      # dodaję wagę do rozwiązania
    return E, suma
