import sys, math, socket
import numpy as np

# Random matrix stream generator for
# Hybrid computing labs
# Usage:
# <script_name>.py [stream_size_in_MegaBytes] [tcp_port]
# Produces stream with square matrix of floats

def generate_stream_with_matrix(sizePort):
    '''
    Function to generate file with
    random matrix of given size
    '''
    sizeInBytes = float(sizePort[0]) * (2**20) # 1 Mb = 2^20 bytes
    num_rows_and_cols = int(math.sqrt(sizeInBytes / 11)) # 11 byte chars for each number
    matrix = np.random.rand(num_rows_and_cols, num_rows_and_cols)
    print(matrix[0])
    print(sum(matrix[0]) / len(matrix[0]))
    #np.savetxt(file_name + '.txt', matrix, fmt='%.8f', delimiter=' ')
    matrix_str = np.array2string(matrix, formatter={'float_kind':lambda x: "%.8f" % x}, separator=' ').replace('[','').replace(']','')

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost', int(sizePort[1]))
    sock.connect(server_address)

    #print(matrix_str.encode('utf-8'))
    sock.sendall(matrix_str.encode('utf-8'))
    sock.close()
    

if __name__ == "__main__":
    if len(sys.argv) > 2:
        generate_stream_with_matrix(sys.argv[1:])
    else:
        print("Usage: <script_name>.py [stream_size_in_MegaBytes] [tcp_port]")