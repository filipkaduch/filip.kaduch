# Filip Kadúch - parallel programming and distributed systems: Documentation

## Assignment 1

#### Python version:
  3.8
#### Modules:
  from fei.ppds import Mutex, Thread


#### Classes:
##### 1. Shared
  ###### Attributes:
        counter - Integer initialized to 0
        end - passed Integer argument during init
        elms - array of 0's with length of end


#### Methods: 
##### 1. function_test(Shared, Mutex)
  - iterates while the Shared counter is less than
  end and increments the value of element on counter index of array elms


#### Task:
  Test the occurance of values in elms array after launching two threads with function_test.
  Try to create two/three variations of using the lock in the code in different places.


#### Few experiments with end_count value:

- 100 - Occurances: {1: 100},
- 100 000 - Occurances: {1: 100000},
- 1 000 000 - - Occurances: {1: 100000},
- 10 000 000 - Occurances: {1: 8282815, 2: 1682083, 0: 39, 3: 35063}
- 50 000 000 - Occurances: {1: 41461371, 2: 8448124, 0: 186, 3: 90319}

We can see that in case of higher end_count value the second thread starts to increment the values in shared class at some point which is
the issue that we are going to solve with Mutex class from module fei.ppds. The module awaits code between locked and unlocked state.


#### Solutions:


1. Locking Mutex before while loop and unlocking after the loop condition Shared.counter < Shared.end break. The solution is based on the
   fact that this is the actual code that leads to correct incrementation of the field after finishing. It means that in the moment of
   first call of the method function_test from Thread instance is awaited and only then the second thread starts with the work:  
    - 50 000 000 - Occurances: {1: 50000000}
    - 10 000 000 - Occurances: {1: 10000000}
    - 1 000 000 - Occurances: {1: 1000000}

  We can see that this solution actually helps with keeping only one thread active at the same time while iterating.
  
  
  
2. Locking Mutex before creating the Thread calling function_test and unlocking after the Thread ID assingment:
   - 50 000 000 - Occurances: {1: 43493587, 0: 225, 2: 6465745, 3: 40443}
 
 This solution doesn't seem to work because I am locking only the creation of Thread and not the actual Thread call of function_test
 which keeps running and the code continues to second Thread.
 
 
 
3. Locking Mutex at the beginning of the iteration of while loop in function_test()
  and unlocking after the incrementation of currently pointed element in elms array:
    - 50 000 000 - Occurances: {1: 50000000}
    - 10 000 000 - Occurances: {1: 10000000}
    - 1 000 000 - Occurances: {1: 1000000}
    - 500 - Occurances: {1: 500}
    
  Solution seems to always allow correct thread to assign correct value before finishing it's code and entering the process of second Thread. 

    
