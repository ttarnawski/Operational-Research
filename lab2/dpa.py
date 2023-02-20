#!/usr/bin/python
# -*- coding: utf-8 -*-
from math import inf

def dpa(G, a, s):
    suma = 0    # deklaracje zmiennych
    A = list()
    alfa = [0 for i in range(len(G))]
    beta = [inf for i in range(len(G))]
    Q = [i for i in range(len(G))]

    beta[s] = 0     # ustalam wagę krawędzi łączącej s z MST na 0
    Q.remove(s)     # usuwam s ze zbioru wierzchołków nienależących do MST
    previous_u = s      # s ustawiam jako poprzednio wybrany wierzchołek

    while Q:    # wykonuje dopóki zbiór wierzhołków nienależących do MST nie jest pusty
        for u in Q:
            if u in G[previous_u]:      # biorę pod uwagę wierzchołki, które są na liście sąsiędztwa poprzednio rozpatrywanego wierzchołka
                if a[u][previous_u] < beta[u]:      # jeżeli waga krawędzi (u, previous_u) jest mniejsza od wagi krawędzi łączącej u z MST
                    alfa[u] = previous_u     # previous_v jest poprzednikiem wierzchołka u w MST
                    beta[u] = a[u][previous_u]      # waga krawędzi łączącej u z MST jest ustawiana na wartość wagi krawędzi (u, previous_u)

        min = inf
        for u in Q:     # szukam minimum dla wagi łączącej u z MST
            if beta[u] < min:
                min = beta[u]
                previous_u = u      # oznaczam ten wierzchołek jako ostatnio wybrany

        Q.remove(previous_u)    # usuwam ten sam wierzchołek
        A.append((alfa[previous_u], previous_u))     # dodaje do rozwiązania krawędź łącząca poprzednika previous_u z previous_u
        suma += a[alfa[previous_u]][previous_u]      # dodaje do sumy wagę tej krawędzi
    return A, suma
