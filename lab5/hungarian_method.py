import numpy as np
from copy import deepcopy
from math import inf


class Matrix:
    def __init__(self, matrix):
        self.matrix = np.array(matrix)
        self.base_matrix = deepcopy(self.matrix)
        self.size = len(matrix)
        self.independent_lst = []
        self.cols = []  # zapisuję tutaj ilość zer w kolumnie
        self.rows = []  # tutaj w wierszu
        self.lines = 0

    def reduce_matrix(self):
        redu_sum = 0
        # Odejmujemy od wierszy
        for row in range(len(self.matrix)):
            mini = min(self.matrix[row])
            redu_sum += mini
            for col in range(len(self.matrix)):
                self.matrix[row][col] -= mini
        # Odejmujemy od kolumn
        for col in range(len(self.matrix)):
            mini = min(self.matrix[:, col])
            redu_sum += mini
            for row in range(len(self.matrix)):
                self.matrix[row][col] -= mini
        return redu_sum

    def rows_fun(self, mini, ind):  # funkcja do obliczania zera niezależnego dla wyznaczonego wiersza
        if mini == 0:  # sprawdzam czy w danym wierszu nie ma żadnych zer
            self.rows[ind] = inf  # jeśli nie ma to 'usuwam' wiersz
            return
        for i in range(self.size):
            if self.matrix[ind][i] == 0:
                flag = 1  # jeśli nie koliduje z innymi zerami to wykona się instrukcja z 25 linii
                for j in range(self.size):
                    if (ind, j) in self.independent_lst or (
                    j, i) in self.independent_lst:  # sprawdzam czy nie koliduje z innymi, wyznaczonymi już zerami
                        flag = 0  # jeśli tak to nie wykona się 26 linia
                        break
                if flag:
                    self.independent_lst.append((ind, i))  # dodaje do listy
                    self.rows[ind] = inf
                    self.cols[i] = inf  # te rzad i kolumna nie będą już rozważane
                    return
                else:
                    self.rows[ind] = inf  # jeśli nie doszło do zmiany to nie biorę pod uwagę już tylko tego rzędu
        return

    def cols_fun(self, mini, ind):  # analogicznie tylko z kolumnami
        if mini == 0:
            self.cols[ind] = inf
            return
        for i in range(self.size):
            if self.matrix[i][ind] == 0:
                flag = 1
                for j in range(self.size):
                    if (j, ind) in self.independent_lst or (i, j) in self.independent_lst:
                        flag = 0
                        break
                if flag:
                    self.independent_lst.append((i, ind))
                    self.cols[ind] = inf
                    self.rows[i] = inf
                    return
                else:
                    self.cols[ind] = inf
        return

    def calc_independent(self):
        m = self.matrix
        iter = 0  # iteracje, które używam w drugiej pętli w celu upewnienia się, że nie dojdzie do pętli nieskończonej
        for i in range(self.size):
            row = 0
            col = 0
            for j in range(self.size):
                if m[i][j] == 0:
                    row += 1
                if m[j][i] == 0:
                    col += 1
            self.rows.append(row)
            self.cols.append(col)  # uzupełniam tutaj listy z ilością zer w wierszu/kolumnie

        while self.rows.count(inf) < self.size and self.cols.count(
                inf) < self.size and iter <= self.size * 2:  # jeżeli są jeszcze jakieś niesprawdzone wiersze/kolumny
            mini1 = min(self.rows)
            mini2 = min(self.cols)
            if mini1 > mini2:  # wybieram mniejszą wartość wśród wierszy i kolumn - dzięki temu żadne zero nie zostanie 'zabrane' wierszom lub kolumnom
                mini = mini2
                ind = self.cols.index(mini)
                self.cols_fun(mini, ind)
            else:
                mini = mini1
                ind = self.rows.index(mini)
                self.rows_fun(mini, ind)

            iter += 1

    def step3(self):
        if len(self.independent_lst) != self.size:
            row_tab = []
            col_tab = []
            marked_row = []
            marked_col = []

            # zapisujemy wiersze i kolumny, w któych są zera niezależne
            for index in self.independent_lst:
                row, col = index
                row_tab.append(row)
                col_tab.append(col)

            # oznaczamy wiersze, które nie mają zera niezależnego
            for i in range(self.size):
                if i not in row_tab:
                    marked_row.append(i)

            # oznaczamy kolumny, które mają zera niezależne
            for row in marked_row:
                for i in range(self.size):
                    if self.matrix[row][i] == 0 and (row, i) not in self.independent_lst:
                        marked_col.append(i)

            # oznaczamy każdy wiersz mający w oznakowanej kolumnie niezależne zero
            for col in marked_col:
                for i in range(self.size):
                    if self.matrix[i][col] == 0 and (i, col) in self.independent_lst:
                        marked_row.append(i)

            # wyliczamy liczbę linii wykreślających
            self.lines = self.size - len(marked_row) + len(marked_col)

            # STEP 4
            # jeśli liczba linii nie jest równa rzędowi macierzy, przechodzimy do kroku 4
            if self.lines != self.size:
                # szukamy najmniejszego elementu w rzędach nieprzykrytych liniami
                min = inf
                for row in range(self.size):
                    if row in marked_row:
                        for col in range(self.size):
                            if col not in marked_col:
                                if self.matrix[row][col] < min:
                                    min = self.matrix[row][col]
                for row in range(self.size):
                    for col in range(self.size):
                        # dodajemy ten element do linii przykrytych dwoma liniami
                        if row not in marked_row and col in marked_col:
                            self.matrix[row][col] += min
                        # odejmujemy ten element od wszystkich, nie przykrytych liniami
                        elif row in marked_row and col not in marked_col:
                            self.matrix[row][col] -= min

        else:
            'Znaleziono już zbiór zer niezależnych'

    def hungarian_method(self):
        self.reduce_matrix()
        self.calc_independent()
        self.step3()
        print("Macierz przejściowa:")
        print(self.matrix)
        while len(self.independent_lst) != self.size:
            self.calc_independent()
            self.step3()
            print("Macierz przejściowa:")
            print(self.matrix)
            return
        print("Macierz końcowa:")
        print(self.matrix)

    def final_cost(self):
        cost = 0
        for point in self.independent_lst:
            cost += self.base_matrix[point[0]][point[1]]
        return cost

    def __str__(self):
        return str(self.matrix)


# def cost_function(a, d, q, y, phase):
#     # obliczenie maksymalnej liczby przedmiotów jaką można zmieścić
#     x = int(y/a[phase])
#     if x > d[phase]:
#         x = d[phase]
#
#     if phase == len(a) - 1:
#         return q[x]
#     else:
#         min_cost = np.inf
#         for possible_x in range(x):
#             cost = q[x] + cost_function(a, d, q, y-a[phase]*x, phase+1)


def dynamic(a, d, q, y):
    # a - waga jednej sztuki
    # d - liczba dostępnych sztuk
    # q - macierz kosztów zabrania odpowiedzniej liczby towarów
    # koszty w formie kary, tzn dla makzymalnej liczby danego towaru koszt wynosi 0
    # y - maksymalna ładowność

    # inicjalizacja x jako macierz None'ów
    # i f jako macierz wartości maksymalnych
    # x_matrix = np.array([[[None] for i in range(y+1)] for j in range(len(d))])
    x_matrix = np.zeros((y + 1, len(d)))
    f = np.full((y + 1, len(d)), np.inf)

    for j in range(f.shape[1]):
        for i in range(f.shape[0]):
            # indeksowanie dla macierzy wejściowych
            # czyli dal j = 0, input_index = etap końcowy
            input_index = f.shape[1] - j - 1

            # wyliczenie maksymalnej liczby przedmiotów
            x = int(i / a[input_index])
            if x > d[input_index]:
                x = d[input_index]

            # jeśli jest to etap ostatni
            if j == 0:
                x_matrix[i, j] = x
                f[i][j] = q[x][input_index]
            # jeśli nie
            else:
                # sprawdzenie wszyskich możliwych ilości x
                for possible_x in range(x + 1):
                    # obliczenie kosztu
                    cost = q[possible_x][input_index] + f[i - a[input_index] * possible_x][j - 1]

                    # sprawdzenie czy koszt jest mniejszy lub równy
                    if cost < f[i, j]:
                        # uaktualnienie
                        x_matrix[i, j] = possible_x
                        f[i, j] = cost

    return x_matrix, f


def get_results(a, y, x_matrix, f):
    free_space = y
    strategy = list()

    for j in range(f.shape[1] - 1, -1, -1):
        input_index = f.shape[1] - j - 1
        strategy.append(f"| {int(x_matrix[free_space, j])}: x{input_index} (f={f[free_space, j]})|")
        free_space = int(free_space - a[input_index] * x_matrix[free_space, j])

    return strategy
