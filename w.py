def transpose(m):
    height=len(m)
    width=len(m[0])
    return( [[(m[h][w]) for h in range(height)] for w in range(width)])


if __name__ == '__main__':
    m=[[1,2,3],
       [4,5,6]]
    print(m)
    transpose(m)