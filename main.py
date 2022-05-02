"""
    numba - JIT compiler that supports CUDA GPU
        programming by directly compiling a restricted subset of Python
        code into CUDA kernels and device functions
        following the CUDA execution model
    unicodedata - use for decoding of loaded corrupted text
    time - used for tracking of elapsed time of cuda processing the data
    numpy - library used for working with arrays
    fei.ppds - we are using print from this module to keep it synced
"""
import time
import unicodedata
import numpy as np
from numba import cuda
from fei.ppds import print

"""
    This code snippet displays the implementation of corrupted
    text correction with edit distance algorithm running on cuda
    with optimisation through streams
"""

dict_lines = []


def load_data():
    """
        This method loads, cleans and saves data from corrupted file
        into array.
    """
    words = []
    split_streams = []
    counter = 0
    with open('data.txt', 'r') as input_file:
        for line in input_file:
            for word in line.split():
                clean_word = unicodedata \
                    .normalize('NFD', word) \
                    .encode('ascii', 'ignore') \
                    .decode("utf-8")
                words.append(clean_word)
                if counter % 10 == 0:
                    split_streams.append(np.asarray(words))
                counter += 1
        input_file.close()
    print(words)
    return words


@cuda.jit
def edit_dist(pass_data):
    """
        Edit distance algorithm aims to find minimum number
        operations to convert string. We have a list of values filled up
        and here we use cuda to choose the minimal value from list of ordinals
        ASCII values.
        Attributes:
            pass_data - array of ASCII values from loaded corrupted words
    """
    thd = cuda.grid(1)
    num_iters = pass_data.size // cuda.blockDim.x
    temp_val = 0
    for j in range(num_iters):
        i = j * cuda.blockDim.x + thd
        if pass_data[i] < temp_val:
            pass_data[i] = temp_val
        else:
            temp_val = pass_data[i]


"""
    Main part of our experimentation which loads the
    dictionary of words to compare and then
    gets data from corrupted file for correction.
    It uses 50 streams with 100 events to track and
    speed up the process
"""
with open('resource_dict.txt', 'r') as reader:
    dict_lines = [unicodedata.normalize('NFD', line.rstrip())
                  .encode('ascii', 'ignore')
                  .decode("utf-8") for line in
                  reader]
    reader.close()

data_gpu = []
gpu_out = []
streams = []
start_events = []
end_events = []
data = []
loaded_data = load_data()

for _ in range(len(loaded_data)):
    streams.append(cuda.stream())
    start_events.append(cuda.event())
    end_events.append(cuda.event())

    for item in loaded_data[_]:
        print(item)
        data.append(np.array(ord(item)).astype('float32'))

start = time.perf_counter()

for k in range(len(loaded_data)):
    data_gpu.append(cuda.to_device(data[k], stream=streams[k]))

for k in range(len(loaded_data)):
    start_events[k].record(streams[k])
    dp = [[0 for i in range(0, len(loaded_data[k]))]
          for j in range(2)]
    for dc_word in dict_lines:
        edit_dist[1, 32, streams[k]](data_gpu[k])

for k in range(len(data)):
    end_events[k].record(streams[k])

for k in range(len(data)):
    gpu_out.append(data_gpu[k].copy_to_host(stream=streams[k]))

for k in range(len(data)):
    assert (np.allclose(gpu_out[k], data[k]))

kernel_times = []

for k in range(len(data)):
    print(f'CUDA TEST {k}: ', start_events[k].elapsed_time(end_events[k]))
    kernel_times.append(start_events[k].elapsed_time(end_events[k]))

end_time = time.perf_counter() - start
print(f'Elapsed time in seconds: {end_time}')
