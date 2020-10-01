import sys, math, socket
import numpy as np

# Random matrix stream generator for
# Hybrid computing labs
# Usage:
# <script_name>.py [stream_size_in_MegaBytes] [tcp_port_out] [tcp_port_in]
# Produces stream with square matrix of floats

def generate_stream_with_matrix(sizePorts):
    '''
    Function to generate file with
    random matrix of given size
    '''
    sizeInBytes = float(sizePorts[0]) * (2**20) # 1 Mb = 2^20 bytes
    num_rows_and_cols = int(math.sqrt(sizeInBytes / 11)) # 11 byte chars for each number
    matrix = np.random.rand(num_rows_and_cols, num_rows_and_cols)
    print(' '.join([str(sum(vector) / len(vector)) for vector in matrix]))
    #np.savetxt(file_name + '.txt', matrix, fmt='%.8f', delimiter=' ')
    matrix_str = np.array2string(matrix, formatter={'float_kind':lambda x: "%.8f" % x}, separator=' ').replace('[','').replace(']','')

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost', int(sizePorts[1]))
    sock.connect(server_address)

    #print(matrix_str.encode('utf-8'))
    sock.sendall(matrix_str.encode('utf-8'))
    sock.close()

    # open connection to receive the result
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost', int(sizePorts[2]))
    sock.bind(server_address)
    sock.listen(1)
    connection, _ = sock.accept()

    result = []
    data = connection.recv(8)
    while data:
        result.append(data)
        print(data)
        data = connection.recv(8)
    print(result)

    connection.close()
    sock.close()
    

if __name__ == "__main__":
    if len(sys.argv) > 2:
        generate_stream_with_matrix(sys.argv[1:])
    else:
        print("Usage: <script_name>.py [stream_size_in_MegaBytes] [tcp_port_out] [tcp_port_in]")