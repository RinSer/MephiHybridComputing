import sys, math
import numpy as np

# Random matrix file generator for
# Hybrid computing labs
# Usage:
# <script_name>.py [file_size_in_MegaBytes] [file_path]
# Produces file with square matrix of floats

def generate_five_files():
    '''
    Generated five files with 
    matrices of sizes from 125Mb to 2Gb
    '''
    mega_bytes = 125
    while mega_bytes < 2001:
        generate_file_with_matrix([mega_bytes, str(mega_bytes)])
        mega_bytes *= 2


def generate_file_with_matrix(sizeName):
    '''
    Function to generate file with
    random matrix of given size
    '''
    sizeInBytes = float(sizeName[0]) * (2**20) # 1 Mb = 2^20 bytes
    num_rows_and_cols = int(math.sqrt(sizeInBytes / 11)) # 11 byte chars for each number
    file_name = str(num_rows_and_cols)
    if (len(sizeName) > 1):
        file_name = sizeName[1]
    matrix = np.random.rand(num_rows_and_cols, num_rows_and_cols)
    np.savetxt(file_name + '.txt', matrix, fmt='%.8f', delimiter=' ')
    

if __name__ == "__main__":
    if len(sys.argv) > 1:
        generate_file_with_matrix(sys.argv[1:])
    else:
        generate_five_files()