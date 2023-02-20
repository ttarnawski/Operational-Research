#!/usr/bin/python
# -*- coding: utf-8 -*-

def dfs_recursive(G, s, visited=[]):
    if s not in visited: # sprawdzam czy wierzchołek jest już zaznaczony jako odwiedzony
        visited.append(s) # dodaję wierzchołek do listy odwiedzonych
        for v in G[s]: # patrzę na wierzchołki, które z nim sąsiadują
            dfs_recursive(G, v, visited) # wywołuję funkcję dla kolejnego wierzchołka

    order = {}
    for i in range(len(visited)): # numeruję wierzchołki
        order[i + 1] = visited[i]
    return order


def is_acyclic(G):
    for v in G:     # sprawdzam istnienie cyklu utworzonego rozpoczynającego się w każdym wierzchołku
        counter = 1     # licznik, który posłuży do wyeliminowania "cykli" składających się z 2 wierzchołków
        dfs = dfs_recursive(G, v, [])   # przeszukuję graf w głąb
        previous_v = None   # zmienna, która będzie w kolejnej pętli for oznaczać poprzedni badany wierzchołek
        for elem in dfs.values():   # odwiedzam wierzchołki w kolejności występowania w dfsie
            if elem == v:   # jeżeli wierzchołek w zewnętrznej pętli jest tym samym wierzchołkiem co w wewnętrznej pętli
                continue    # to przechodzę do kolejnego
            if previous_v is not None and elem not in G[previous_v]:
                counter = 2     # jeżeli dwa ostatnie badane wierzchołki nie sąsiadują ze sobą w grafie
                previous_v = elem   # to szukam kolejngo możliwego cyklu
                continue
            counter += 1
            if v in G[elem] and counter > 2:    # graf jest cykliczny jeśli kończymy cykl w wierzchołku od którego wychodziliśmy
                return False    # i cykl musi zawierać więcej niż 2 wierzchołki
            previous_v = elem
    return True


def is_consistent(G):
    dfs = dfs_recursive(G, 1)   # sprawdzenie czy liczba wierzchołków w grafie jest równa liczbie wierzchołków
    return len(G.keys()) == len(dfs.keys())     # w algorytmie przeszukiwania grafu
