# Assignment - Q3

def traverse(matrix):

    n = len(matrix)
    result = [[] for k in range(n*2-1)]
    i = 0
    j = 0
    k = 0
    while i < n and j < n and k < n:
       
        if i <= k and j <= k:
            result[k].append(matrix[i][j])
            i -= 1
            j += 1
        else:
            k += 1
            j = 0
            i = k
    
    i = n-1
    j = 1
    k = n
    while k < 2*n-1:     
        if i < n and j < n:
            result[k].append(matrix[i][j])
            i -= 1
            j += 1
        else:
            k += 1
            i = n-1
            j = k-n+1

    return result

length = 8
matrix = [[[i,j] for j in range(length)] for i in range(length)]

M = traverse(matrix)
l = len(M)

print('\nTRAVERSED MATRIX -\n')
for k in range(l):
    print(M[k])
print('\n')