# Filip Kadúch - parallel programming and distributed systems: Documentation

## Assignment 10

#### Python version:
  3.8
#### Modules:
    numba - JIT compiler that supports CUDA GPU
        programming by directly compiling a restricted subset of Python
        code into CUDA kernels and device functions following the CUDA execution model

    unicodedata - use for decoding of loaded corrupted text

    time - used for tracking of elapsed time of cuda processing the data

    numpy - library used for working with arrays


#### Task:
  Rework your previous solution with cuda streams and events.

#### Methods: 

##### 1. load_data()
  This method loads, cleans and saves data from corrupted file
  into array.

##### 2. edit_dist(string, string, int, int)
  This method gets word on current cuda position and we have a list of values filled up
  and here we use cuda to choose the minimal value from list of ordinals
  ASCII values.
  Attributes:
      pass_data - array of ASCII values from loaded corrupted words

### Experimentation:
  Main part of our experimentation which loads the
  dictionary of words to compare and then
  gets data from corrupted file for correction.
  It uses 50 streams with 100 events to track and
  speed up the process

#### Output for our experimentation:

```
WORD PROCESSED: 0, PIRATES
WORD PROCESSED: 1, OF
WORD PROCESSED: 2, THE
WORD PROCESSED: 3, ARRIBEAN
WORD PROCESSED: 4, DElAD
WORD PROCESSED: 5, MANS
WORD PROCESSED: 6, CHEST
WORD PROCESSED: 7, by
WORD PROCESSED: 8, Ted
WORD PROCESSED: 9, Elliott
WORD PROCESSED: 10, Terry
WORD PROCESSED: 11, Rossio
WORD PROCESSED: 12, view
WORD PROCESSED: 13, looking
WORD PROCESSED: 14, trafght
WORD PROCESSED: 15, down
WORD PROCESSED: 16, at
WORD PROCESSED: 17, rolling
WORD PROCESSED: 18, swells
WORD PROCESSED: 19, sound
WORD PROCESSED: 20, f
WORD PROCESSED: 21, winyd
WORD PROCESSED: 22, and
WORD PROCESSED: 23, hundlr
WORD PROCESSED: 24, then
WORD PROCESSED: 25, h
WORD PROCESSED: 26, ld
WORD PROCESSED: 27, heartbecat
WORD PROCESSED: 28, Scen
WORD PROCESSED: 29, PORT
WORD PROCESSED: 30, ROYAL
WORD PROCESSED: 31, teacups
WORD PROCESSED: 32, om
WORD PROCESSED: 33, a
WORD PROCESSED: 34, table
WORD PROCESSED: 35, in
WORD PROCESSED: 36, the
WORD PROCESSED: 37, rain
WORD PROCESSED: 38, siheet
WORD PROCESSED: 39, music
WORD PROCESSED: 40, on
WORD PROCESSED: 41, music
WORD PROCESSED: 42, stands
WORD PROCESSED: 43, in
WORD PROCESSED: 44, the
WORD PROCESSED: 45, rain
WORD PROCESSED: 46, bouquet
WORD PROCESSED: 47, o
WORD PROCESSED: 48, white
WORD PROCESSED: 49, orchids

Elapsed time in seconds: 359.0307177
```


### Outcome of comparison:
In the output we can see that in a simulation mode we can't really reach the potential of CUDA and the whole optimalisation process with streams and events in this case took longer than before with this architecture. Maybe a solution where we would split our data to different grid e.g.(50{corrupted text length} x 20 000 + 1 {words in dictionary to compare}) with each element being array of ASCII values from string to compare. 0th index would be used for corrupted word array of ASCII values)
