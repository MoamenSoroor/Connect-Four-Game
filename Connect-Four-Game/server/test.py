
mat = [[x for x in range(4)],
       [x for x in range(4,8)],
       [x for x in range(8,12)],
       [x for x in range(12,16)]]

print(mat)
d = 4

for k in range(0,d):
    print("d: ",end=" ")
    row , col = range(0,k + 1), range(k,-1,-1)
    for i,j in zip(row,col):
        print(mat[i][j],end =" ")

    print("")

for k in range(0,d):
    print("d: ",end=" ")
    row , col = range(d-k-1 , d + 1 ), range(0,k + 1)
    for i,j in zip(row,col):
        print(mat[i][j],end =" ")

    print("")


for k in range(0,d):
    print("d: ",end=" ")
    row , col = range(0,k + 1), range(d-k-1 , d + 1 )
    for i,j in zip(row,col):
        print(mat[i][j],end =" ")

    print("")