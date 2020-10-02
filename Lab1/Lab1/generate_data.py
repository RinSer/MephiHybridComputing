import sys, os, math, socket
import numpy as np

'''
Random matrix stream generator for
Hybrid computing labs
Usage:
<script_name>.py [stream_size_in_MegaBytes] [tcp_port_out] [tcp_port_in]
Produces stream with square matrix of floats
and sends it as byte stream to tcp_port_out
and returns result received from tcp_port_in
'''

NUM_AVERAGES_DISPLAYED = 3

def send_file_to_socket(port, file_path):
    '''
    Sends string as byte stream to an open tcp socket
    '''
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost', int(port))
    sock.connect(server_address)

    with open(file_path, 'rb') as input_file:
        sock.sendfile(input_file)

    sock.close()
    os.remove(file_path)


def get_string_from_socket(port):
    '''
    Listens to tcp port until get
    all the stream and then prints it
    '''
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost', int(port))
    sock.bind(server_address)
    sock.listen(1)
    connection, _ = sock.accept()

    result = []
    data = connection.recv(256)
    while data:
        result.append(data)
        data = connection.recv(256)
    result_str = ''.join([part.decode() for part in result])
    lines = result_str.split('\n')
    execution_time = lines[-2]
    numbers = lines[0].split(' ')
    print(len(numbers)-1)
    print(' '.join(numbers[:NUM_AVERAGES_DISPLAYED]))
    print(execution_time)

    connection.close()
    sock.close()


def generate_stream_with_matrix(sizePorts):
    '''
    Function to generate file with
    random matrix of given size
    '''
    sizeInBytes = float(sizePorts[0]) * (2**20) # 1 Mb = 2^20 bytes
    num_rows_and_cols = int(math.sqrt(sizeInBytes / 11)) # 11 byte chars for each number
    matrix = np.random.rand(num_rows_and_cols, num_rows_and_cols)
    print(len(matrix))
    print(' '.join([str(sum(vector) / len(vector)) for vector in matrix][:NUM_AVERAGES_DISPLAYED]))
    matrix_file_path = str(num_rows_and_cols) + '.mtrx'
    np.savetxt(matrix_file_path, matrix, fmt='%.8f', delimiter=' ')
    # matrix_str = np.array2string(matrix, formatter={'float_kind':lambda x: "%.8f" % x}, separator=' ').replace('[','').replace(']','')

    # print(matrix_str.split('\n')[0])
    send_file_to_socket(sizePorts[1], matrix_file_path)
    get_string_from_socket(sizePorts[2])
    

if __name__ == "__main__":
    if len(sys.argv) > 2:
        generate_stream_with_matrix(sys.argv[1:])
    else:
        print("Usage: <script_name>.py [stream_size_in_MegaBytes] [tcp_port_out] [tcp_port_in]")