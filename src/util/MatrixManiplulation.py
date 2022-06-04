# flip 2d array on it's diagonal
# takes 2d square array, length of row/col
# NOTE - you must deeply copy the array BEFORE using this function, otherwise the original will be overwritten
def mirror_matrix(mat, n):
    # traverse a matrix and swap
    # mat[i][j] with mat[j][i]
    for i in range(n):
        for j in range(i + 1):
            t = mat[i][j]
            mat[i][j] = mat[j][i]
            mat[j][i] = t
    return mat