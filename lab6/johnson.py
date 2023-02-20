from math import inf

def johnson(matrix0):
    # tworzę macierz pomocniczą w celu rozwiązania fikcyjnego problemu zawierającego 2 maszyny
    matrix = [[0 for _ in range(10)] for _ in range(2)]
    for i in range(2):
        if i == 0:
            for j in range(10):
                matrix[0][j] = matrix0[0][j] + matrix0[1][j]
        if i == 1:
            for j in range(10):
                matrix[1][j] = matrix0[1][j] + matrix0[2][j]

    ### Algorytm Johnsona dla 2 maszyn ###

    new_matrix = [[0 for _ in range(10)] for _ in range(2)]

    # lista z zadaniami, które zostały już uszeregowane
    marked_indexes = []

    # szukam elementu minimalnego dla pierwszej i drugiej maszyny i umieszczam w nowej macierzy
    for i in range(2):
        if i == 0:
            min = inf
            min_i = 0
            min_j = 0
            for j in range(len(matrix[0])):
                if matrix[i][j] < min:
                    min = matrix[i][j]
                    min_i = i
                    min_j = j
            new_matrix[0][0] = matrix[min_i][min_j]
            new_matrix[1][0] = matrix[1][min_j]
            marked_indexes.append(min_j)
        if i == 1:
            min = inf
            min_i = 1
            min_j = 0
            for j in range(len(matrix[0])):
                if matrix[i][j] < min and j not in marked_indexes:
                    min = matrix[i][j]
                    min_i = i
                    min_j = j
            new_matrix[1][-1] = matrix[min_i][min_j]
            new_matrix[0][-1] = matrix[0][min_j]
            marked_indexes.append(min_j)

    # kontynuuję szeregowanie zadań wg kosztów, dopóki nie odznaczę wszystkich zadań
    while len(marked_indexes) != len(matrix[0]):
        min = inf
        min_j = 1
        for j in range(len(matrix[0])):
            if matrix[1][j] <= min and j not in marked_indexes:
                min = matrix[1][j]
                min_j = j
        new_matrix[1][-len(marked_indexes)] = matrix[1][min_j]
        new_matrix[0][-len(marked_indexes)] = matrix[0][min_j]
        marked_indexes.append(min_j)

    # kolejność zadań
    marked_indexes.append(marked_indexes.pop(1))

    # końcowe uszeregowanie zadań
    order_matrix = [[0 for _ in range(10)] for _ in range(3)]
    for i in range(10):
        for index in marked_indexes:
            for j in range(3):
                order_matrix[j][index] = matrix0[j][index]

    # obliczenie długości uszeregowania (czasu zakończenia)
    m1 = []
    m2 = []
    m3 = []
    for j in range(10):
        if j == 0:
            m1.append(order_matrix[0][0])
            m2.append(order_matrix[0][0] + order_matrix[1][0])
            m3.append(order_matrix[0][0] + order_matrix[1][0] + order_matrix[2][0])
        else:
            m1.append(order_matrix[0][j] + m1[j - 1])
            m2.append(max(m2[j - 1], m1[j]) + order_matrix[1][j])
            m3.append(max(m3[j - 1], m2[j]) + order_matrix[2][j])

    print(marked_indexes)
    print(m1)
    print(m2)
    print(m3)
