import numpy as np

def delete_empty_rows(matrix):
    # vraci upravenou puvodni matici, ve ktere smaze radky, co obsahuji pouze 0
    new_matrix = []
    for row in matrix:
        if not np.any(row):
            pass
        else:
            new_matrix.append(row)
    return np.array(new_matrix)

def find_values(matrix, currentValues, startingRow):
    # funkce spocita hodnotu dalsiho x
    curRow = matrix[startingRow]
    notKnowValues = 0
    i=0
    while i<len(curRow):
        if curRow[i] == 0:
            notKnowValues += 1
        i+=1
    knownA = curRow[notKnowValues+1:-1]
    knownSum = np.sum(np.multiply(knownA, currentValues))
    result = (curRow[-1] - knownSum) / curRow[notKnowValues]
    currentValues = np.insert(currentValues, 0, result)
    return currentValues


def count_pivots(matrix):
    # funkce pocita pocet pivotu, kdyz jich bude min nez je pocet sloupcu-1, bude soustava mit nekonecne reseni
    pivots = 0
    for row in matrix:
        if np.any(row):
            pivots += 1
    return pivots
#
#
# def find_first_nonzero(matrix, row, column):
#     # v zadanem sloupci najde prvni nenulovy radek
#     if np.any(matrix[row:, column]):
#         firstRow = (matrix[row:, column] != 0).argmax(axis=0) + row
#         # firstRow = (matrix[row:, firstColumn]).argmax(axis=0)
#
#         return firstRow, 0
#     elif column + 1 == len(matrix[0, :]):
#         return row, 'reseni splnuje nekonecne mnoho x'
#     else:
#         return find_first_nonzero(matrix, row, column + 1)


def swap_arrays(matrix, firstRow, secondRow):
    # prohodi radky, kdyz je na zacatku 0
    # matrix[firstRow], matrix[secondRow] = matrix[secondRow], matrix[firstRow]
    matrix[[firstRow, secondRow]] = matrix[[secondRow, firstRow]]
    return matrix


def deduct_arrays(matrix, mainRow, secondRow):
    # odecte od sebe dva radky, tak aby pod pivotem byly nuly
    pivotIndex = (matrix[mainRow, :] != 0).argmax(axis=0)
    if matrix[secondRow, pivotIndex] != 0:
        koef = matrix[secondRow, pivotIndex] / matrix[mainRow, pivotIndex]
        decuctionArray = matrix[mainRow] * koef
        matrix[secondRow] -= decuctionArray
        return matrix


row = input('Napiste prvni radek rozsirene matice soustavy, cisla piste oddelene mezerou').strip()
rows = []
row = row.split(' ')
row = [float(i) for i in row]
len_row = len(row)
rows.append(row)
# nacteme prvni radek, pridame do rows
while len(row) != 0:
    row = input("Napiste n-ty radek, az skoncite, napiste prazdny radek").strip()
    if len(row) == 0:
        pass
    else:
        row = row.split(' ')
        row = [float(i) for i in row]
        if len_row != len(row):
            raise Exception("Pocet parametru v kazde rovnici musi byt stejny")
        rows.append(row)
matrix = np.array(rows).astype(float)
fRow = 0
fColumn = 0
blocked_rows = 0
for column in range(len(matrix[0, :])):
    if np.any(matrix[blocked_rows:, column]):
        firstRow = (matrix[blocked_rows:, column] != 0).argmax(axis=0) + blocked_rows
        matrix = swap_arrays(matrix, firstRow, blocked_rows)

        i = blocked_rows + 1
        while i < len(matrix):
            deduct_arrays(matrix, blocked_rows, i)
            i += 1
        blocked_rows += 1
    else:
        pass

for row in range(len(matrix)):
    if not matrix[row, :-1].any():
        if matrix[row, -1] != 0:
            print('Soustava nemá řešení')
            quit()

pivots = count_pivots(matrix)
if (len(matrix[0, :]) - 1) > pivots:
    print('Soustava má nekonečně mnoho řešení')
    quit()

matrix = delete_empty_rows(matrix)
reversedMatrix = matrix[::-1]
# print(reversedMatrix)
# reversedMatrix = delete_empty_rows(reversedMatrix)
currenValues = []

for i in range(len(matrix)):
    currenValues = find_values(reversedMatrix, currenValues, i)
print(currenValues)




