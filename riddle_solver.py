current_riddle = [
    [8, 2, 4, 5, 4, 6, 7, 1],
    [1, 0, 6, 5, 2, 0, 3, 5],
    [2, 1, 2, 1, 3, 1, 2, 2],
    [2, 2, 0, 1, 3, 2, 0, 1],
    [0, 2, 8, 0, 3, 4, 8, 1],
    [1, 7, 5, 4, 5, 3, 2, 8]
]


def solver_type1(arr):
    res = ""
    if len(arr[0]) != 3 or len(arr) != 6:
        return "Invalid array, try again"
    for x in range(len(arr[0])):
        a, b = 0, 0
        if arr[2][x] != 0:
            a = int(str(int(arr[0][x]) * int(arr[1][x])) * int(arr[2][x]))
        if arr[3][x] != 0:
            b = int(str(int(arr[5][x]) * int(arr[4][x])) * int(arr[3][x]))
        res += str(a + b)
    return res

