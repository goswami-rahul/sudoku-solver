import sys
import os

def solve(grid):
    """ main function to solve the grid.
    """
    availableOptions = {}   # keys -> tuple(row, col) of blank spaces;
			    # values -> set of possibilties
    m = len(grid)
    sRow = int(m**0.5)
    sCol = int(m**0.5)  # sRow x sCol (size of subGrid)

    assert m == sRow * sCol  # size of Grid must be a perfect square.  

    subGrids = [set() for _ in range(m)]  # subgrids of sudoku
    rowSets = [set() for _ in range(m)]
    colSets = [set() for _ in range(m)]

    for row in range(m):
	      for col in range(m):
		        num = grid[row][col]
		        if num == 0:
			          availableOptions[(row, col)] = set(range(1, m+1))
		        else:
			          subIndex = (row // sRow) * sRow + (col // sCol)
			          subGrids[subIndex].add(num)
			          rowSets[row].add(num)
			          colSets[col].add(num)

    i = 0
    while availableOptions:
        found = []           # list of indices of blanks whose values are found in each iteration
        for key in availableOptions:
            row, col = key
            subIndex = (row // sRow) * sRow + (col // sCol)
            availableOptions[key] -= subGrids[subIndex]
            availableOptions[key] -= rowSets[row]
            availableOptions[key] -= colSets[col]
            if len(availableOptions[key]) == 1:
                (value, ) = availableOptions[key]
                grid[row][col] = value
                subGrids[subIndex].add(value)
                rowSets[row].add(value)
                colSets[col].add(value)
                found.append(key)
        for key in found:
            del availableOptions[key]
        i += 1
        sys.stdout.write("\r--> number of iterations = %d" % i) # Show the curent iteration number.
    print()
    return grid

def input_sudoku(filename):
    """Take the input and preprocess it to return a 2D Matrix of NxN.
    """
    grid = []
    if not filename:
        filename = input("\nEnter the name of input file : ")
    if not os.path.isabs(filename):
        filename = os.path.join('./', filename)
    with open(filename, 'r') as fp:
	      for line in fp:
		        grid.append(list(map(int, line.split())))
    return grid

def output_sudoku(grid, outfile):
    """Prints the solved sudoku and writes it in the output file.
    """
    m = len(grid)
    if m < 10:     pad = 1
    else:          pad = 2

    print("\n")	
    out = "\n".join([" ".join([str(n).zfill(pad) for n in row]) for row in grid])
    print(out)
    if not outfile:
        outfile = input("\nEnter the name output file to write solution : ")
    
    if not os.path.isabs(outfile):
        outfile = os.path.join('./', outfile)
    with open(outfile, 'w') as fp:
        fp.write(out)

def test_sudoku():
    """Test the function with a 9 x 9 grid
       and a 16 x 16 grid.
    """
    grid_9x9_easy     = solve(input_sudoku('./9x9_easy.txt'))
    grid_16x16_medium = solve(input_sudoku('./16x16_medium.txt'))
    
    assert grid_9x9_easy == [[9, 7, 5, 2, 4, 6, 1, 8, 3],
                             [6, 3, 4, 5, 1, 8, 2, 7, 9],
                             [1, 2, 8, 9, 7, 3, 5, 4, 6],
                             [2, 9, 6, 1, 8, 4, 7, 3, 5],
                             [3, 4, 7, 6, 2, 5, 8, 9, 1],
                             [5, 8, 1, 7, 3, 9, 4, 6, 2],
                             [4, 6, 3, 8, 5, 1, 9, 2, 7],
                             [8, 1, 2, 3, 9, 7, 6, 5, 4],
                             [7, 5, 9, 4, 6, 2, 3, 1, 8]]
                  
    assert grid_16x16_medium == [[8, 7, 11, 10, 2, 12, 9, 1, 5, 3, 16, 6, 13, 14, 4, 15],
                                 [12, 5, 14, 13, 4, 11, 3, 10, 15, 9, 1, 7, 2, 6, 16, 8],
                                 [16, 3, 1, 6, 5, 8, 7, 15, 4, 14, 2, 13, 9, 10, 11, 12],
                                 [2, 15, 4, 9, 16, 14, 6, 13, 8, 11, 10, 12, 1, 7, 5, 3],
                                 [14, 13, 15, 8, 11, 2, 1, 9, 16, 10, 6, 3, 7, 4, 12, 5],
                                 [9, 4, 7, 5, 8, 6, 15, 12, 11, 2, 13, 14, 10, 3, 1, 16],
                                 [11, 2, 10, 3, 7, 5, 13, 16, 12, 8, 4, 1, 15, 9, 6, 14],
                                 [6, 16, 12, 1, 14, 10, 4, 3, 7, 5, 15, 9, 11, 2, 8, 13],
                                 [3, 8, 6, 12, 15, 13, 16, 7, 14, 4, 9, 11, 5, 1, 2, 10],
                                 [10, 1, 2, 4, 6, 9, 5, 14, 13, 15, 7, 16, 8, 12, 3, 11],
                                 [15, 14, 16, 11, 12, 4, 10, 8, 2, 1, 3, 5, 6, 13, 9, 7],
                                 [13, 9, 5, 7, 1, 3, 11, 2, 6, 12, 8, 10, 16, 15, 14, 4],
                                 [7, 11, 13, 15, 9, 16, 12, 5, 1, 6, 14, 4, 3, 8, 10, 2],
                                 [5, 12, 3, 14, 10, 7, 8, 6, 9, 13, 11, 2, 4, 16, 15, 1],
                                 [1, 10, 9, 2, 13, 15, 14, 4, 3, 16, 5, 8, 12, 11, 7, 6],
                                 [4, 6, 8, 16, 3, 1, 2, 11, 10, 7, 12, 15, 14, 5, 13, 9]]

if __name__ == '__main__':

    inputfile = ''
    outputfile = ''
    
    if len(sys.argv) == 2:
        inputfile = sys.argv[1]
    elif len(sys.argv) == 3:
        inputfile = sys.argv[1]
        outputfile = sys.argv[2]
    
    test_sudoku()
    grid = input_sudoku(inputfile)
    grid = solve(grid)
    output_sudoku(grid, outputfile)
