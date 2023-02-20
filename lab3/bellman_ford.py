#!/usr/bin/python
# -*- coding: utf-8 -*-

from math import inf


def bellman_ford(G, w, s):
    # inicjalizacja zmiennych przechowujących koszty dojścia z wierzchołka startowego do wierzchołka v po najkrótszej ścieżce
    # oraz listę z numerami wierzchołków grafu, które są poprzednikami wierzchołka v na najkrótszej ścieżce
    cost = {i: inf for i in G.keys()}
    previous_v = {i: -1 for i in G.keys()}

    # ustawiam koszt dla początkowego wierzchołka równy 0
    cost[s] = 0

    for i in range(len(G) - 1):     # n-1 razy
        for u in G.keys():
            for v in G[u]:      # sprawdzam dla każdego wierzchołka v sąsiadującego z u
                if cost[v] > cost[u] + w[u][v]:     # jeżeli koszt dojścia do wierzchołka v może być mniejszy, aktualizuje go
                    cost[v] = cost[u] + w[u][v]
                    previous_v[v] = u       # ustalam wierzchołek u jako ostatni wierzchołek przed doatrciem do v

    for u in G.keys():
        for v in G[u]:
            if cost[v] > cost[u] + w[u][v]:     # sprawdzam istnienie ujemnego cyklu
                raise Exception('Cykl ujemny')

    return cost, previous_v