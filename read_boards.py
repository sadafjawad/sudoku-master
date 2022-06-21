boardList = []
try:
    with open("sudoku_boards.txt", "r") as boards:
        temp = boards.readlines()
        temp=[i for i in temp if not i.startswith("Grid")]
        index=0
        for k in range(50):
            board = []
            for i in range(9):
                row = []
                strRow = temp[index]
                for j in range(9):
                    row.append(int(strRow[j]))
                board.append(row)
                index+=1
            boardList.append(board)
except FileNotFoundError:
    print("not found")

