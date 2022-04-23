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
"""

dict_lines = []
corrected_words = []


@cuda.jit
def my_kernel(passed_data):
    """
         This method gets word on current cuda position and starts
         the correction process through edit distance algorithm. It
         iterates over dictionary of words to compare with loaded word
         and saves the result od ED algorithm into object with key
         being the word from dictionary and value being the result.
         Then the minimal is chosen from this dictionary which should
         represent the most probable word deformation.
         Attributes:
             passed_data - array of loaded corrupted words
     """
    pos = cuda.grid(1)
    answers = {}
    if pos < passed_data.size:
        clean_word = passed_data[pos]
        answers[clean_word] = []
        dict_iter = 0
        for dc_word in dict_lines:
            if clean_word == dc_word:
                answers[clean_word].append(0)
                break
            temp_val = edit_dist(clean_word.lower(),
                                 dc_word,
                                 len(clean_word),
                                 len(dc_word))
            answers[clean_word].append(temp_val)
            dict_iter += 1

        min_val = min(answers[clean_word])
        min_index = answers[clean_word].index(min_val)
        print(f'WORD PROCESSED: {pos},'
              f'{clean_word} -> {dict_lines[min_index]}')
        corrected_words.append(dict_lines[min_index])


def load_data():
    """
        This method loads, cleans and saves data from corrupted file
        into array.
    """
    words = []
    with open('data.txt', 'r') as input_file:
        for line in input_file:
            for word in line.split():
                clean_word = unicodedata \
                    .normalize('NFD', word) \
                    .encode('ascii', 'ignore') \
                    .decode("utf-8")
                words.append(clean_word)
        input_file.close()

    return words


def edit_dist(str1, str2, len1, len2):
    """
        Edit distance algorithm aims to find minimum number
        operations to convert str1 to str2.
        Algorithm borrowed from:
        https://www.geeksforgeeks.org/edit-distance-dp-5/?ref=gcse
        Attributes:
            str1 - corrupted word
            str2 - dictionary word to compare
            len1, len2 - representative lengths of passed strings
    """
    dp = [[0 for i in range(len1 + 1)]
          for j in range(2)]

    for i in range(0, len1 + 1):
        dp[0][i] = i

    for i in range(1, len2 + 1):
        for j in range(0, len1 + 1):
            if j == 0:
                dp[i % 2][j] = i
            elif str1[j - 1] == str2[i - 1]:
                dp[i % 2][j] = dp[(i - 1) % 2][j - 1]
            else:
                dp[i % 2][j] = (1 + min(dp[(i - 1) % 2][j],
                                        min(dp[i % 2][j - 1],
                                            dp[(i - 1) % 2][j - 1])))

    return dp[len2 % 2][len1]


"""
    Main part of our experimentation which loads the
    dictionary of words to compare and then
    gets data from corrupted file for correction.
    It uses 2 blocks per grid with 32 threads
    in order to perform the comparison and
    correction of corrupted words.
"""
with open('slovnik.txt', 'r') as reader:
    dict_lines = [unicodedata.normalize('NFD', line.rstrip())
                  .encode('ascii', 'ignore')
                  .decode("utf-8") for line in
                  reader]
    reader.close()
data = np.asarray(load_data())
print(f'Data size: {data.size}')
tpb = 32
bpg = (data.size + (tpb - 1)) // tpb
start = time.perf_counter()
my_kernel[bpg, tpb](data)
end_time = time.perf_counter() - start
print(f'Elapsed time in seconds: {end_time}')
