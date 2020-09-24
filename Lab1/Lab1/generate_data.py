import sys
import numpy as np

# Random matrix file generator for
# Hybrid computing labs
# Usage:
# <script_name>.py [n_rows] [n_cols]
# If only n_rows is presented the matrix will be square 

def generate_five_files():
    '''
    Generated five files with 
    matrices from 2x2 to 1250x1250
    with step x50
    '''
    i = 1000
    while i < 16001:
        matrix = np.random.randint(0, 99999, size=(i, i))
        np.savetxt(str(i) + '.txt', matrix, fmt='%d', delimiter=' ')
        i *= 2


def generate_file_with_matrix(size):
    '''
    Function to generate file with
    random matrix of given size
    '''
    num_rows = int(size[0])
    num_cols = num_rows
    if (len(size) > 1):
        num_cols = int(size[1])
    matrix = np.random.randint(0, 99999, size=(num_rows, num_cols))
    np.savetxt(str(num_rows) + 'x' + str(num_cols) + '.txt', matrix, fmt='%d', delimiter=' ')
    

if __name__ == "__main__":
    if len(sys.argv) > 1:
        generate_file_with_matrix(sys.argv[1:])
    else:
        generate_five_files()