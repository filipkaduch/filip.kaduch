# Filip Kadúch - parallel programming and distributed systems: Documentation

## Assignment 9

#### Python version:
  3.8
#### Modules:
    numba - JIT compiler that supports CUDA GPU
        programming by directly compiling a restricted subset of Python
        code into CUDA kernels and device functions following the CUDA execution model
    
    unicodedata - use for decoding of loaded corrupted text
    
    time - used for tracking of elapsed time of cuda processing the data
    
    numpy - library used for working with arrays
    
    fei.ppds - we are using print from this module to keep it synced

#### Task:
  Create a application which demonstrates usage of cuda within python and it's module numba.

#### Methods: 
##### 1. my_kernel(Array)
   This method gets word on current cuda position and starts
   the correction process through edit distance algorithm (ED). It
   iterates over dictionary of words to compare with loaded word
   and saves the result of ED algorithm into object with key being the word from
   dictionary and value being the result. Then the minimal is chosen from
   this dictionary which should represent the most probable correct word out of the original deformation.

##### 2. load_data()
  This method loads, cleans and saves data from corrupted file
  into array.
  
##### 3. edit_dist(string, string, int, int)
   Edit distance algorithm aims to find minimum number
   operations to convert str1 to str2. It takes 4 arguments: 
   corrupted word, dictionary word to compare and 2 representative lengths of passed strings.

### Experimentation:
Main part of our experimentation loads the
dictionary of words to compare and then
gets data from corrupted file for correction.
It uses 2 blocks per grid with 32 threads per grid
in order to perform the comparison and
correction of corrupted words. In each kernel we are printing the current word and current position in grid.

#### Output for our experimentation:

```
WORD PROCESSED: 7, by -> by
WORD PROCESSED: 12, view -> view
WORD PROCESSED: 16, at -> at
WORD PROCESSED: 15, down -> down
WORD PROCESSED: 22, and -> and
WORD PROCESSED: 24, then -> then
WORD PROCESSED: 19, sound -> sound
WORD PROCESSED: 18, swells -> swells
WORD PROCESSED: 13, looking -> looking
WORD PROCESSED: 17, rolling -> rolling
WORD PROCESSED: 31, teacups -> teacups
WORD PROCESSED: 20, f -> i
WORD PROCESSED: 25, h -> i
WORD PROCESSED: 1, OF -> of
WORD PROCESSED: 26, ld -> ad
WORD PROCESSED: 2, THE -> the
WORD PROCESSED: 8, Ted -> ted
WORD PROCESSED: 29, PORT -> port
WORD PROCESSED: 5, MANS -> mans
WORD PROCESSED: 28, Scen -> sen
WORD PROCESSED: 21, winyd -> wind
WORD PROCESSED: 4, DElAD -> dead
WORD PROCESSED: 30, ROYAL -> royal
WORD PROCESSED: 10, Terry -> terry
WORD PROCESSED: 6, CHEST -> chest
WORD PROCESSED: 11, Rossio -> ross
WORD PROCESSED: 9, Elliott -> allot
WORD PROCESSED: 23, hundlr -> under
WORD PROCESSED: 0, PIRATES -> pirates
WORD PROCESSED: 3, ARRIBEAN -> arian
WORD PROCESSED: 14, trafght -> taught
WORD PROCESSED: 27, heartbecat -> heartbeat
WORD PROCESSED: 35, in -> in
WORD PROCESSED: 36, the -> the
WORD PROCESSED: 37, rain -> rain
WORD PROCESSED: 40, on -> on
WORD PROCESSED: 43, in -> in
WORD PROCESSED: 44, the -> the
WORD PROCESSED: 34, table -> table
WORD PROCESSED: 45, rain -> rain
WORD PROCESSED: 39, music -> music
WORD PROCESSED: 41, music -> music
WORD PROCESSED: 48, white -> white
WORD PROCESSED: 42, stands -> stands
WORD PROCESSED: 46, bouquet -> bouquet
WORD PROCESSED: 49, orchids -> orchids
WORD PROCESSED: 33, a -> ia
WORD PROCESSED: 47, o -> i
WORD PROCESSED: 32, om -> am
WORD PROCESSED: 38, siheet -> sheet
Elapsed time in seconds: 259.0307177
```


### Outcome of comparison:
In the output we can see a clear indication of parallelisation in practice, each thread of block starts at the same time but the difference is that words which are correct or pretty short finish earlier (logically). We can see that behaviour in each of the blocks used. The number in the output represents current word which is being processed and we can see that the first block manages to correct first 0 - 31 words and second then starts from 32 and gets the remaining 18. We also track elapsed time for future optimalisations.

