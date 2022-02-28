# Filip Kadúch - parallel programming and distributed systems: Documentation

## Assignment 2

#### Python version:
  3.8
#### Modules:
  from fei.ppds import Event, Mutex, Semaphore, Thread


#### Tasks:
  1. Implement the Barrier synchronisation object and test the possible signaling objects for this purpose - main.py
  2. Test the reusability solutions for Barrier - main_2.py
  3. Ensure correct synchronization during calculation of fibonacci sequence - main_3.py
  
#### Classes:
##### 1. SimpleBarrier
  ###### Attributes:
    n - number of threads to await
    counter - current index of thread
    mutex - Mutex object doing the synchronization
    semaphore/event - signaling object
    wait - method that iterates over 'threads' and locks
      the process of each thread before execution and unlocking after.
      Then we tell our SignalingObject to await for signal which comes
      after full iteration cycle.
        
#### Methods: 
##### 1. barrier_example(SimpleBarrier, thread_id)
  - demonstrates the usage of barrier implemented with event/semaphore
  which allows correct awaiting in code of processes launched in different threads.
  This feature is displayed in the output that shows the barrier holds the threads
  running this method until all of them reach this point.
  
##### 2. barrier_cycle(SimpleBarrier, thread_id)
  - barrier used in this method ensures that all threads
  await each other before the execution of ko method and
  also before calling of method rendezvous

##### 3. compute_fibonacci(index, Mutex, SignalingObject)
  - method that expect index of first element in equation, Mutex and Semaphore/Event
  Starts with sleep to demonstrate the de-sync of processes and then unlocks the Mutex
  and tells the signaling object to await others in this point to ensure that the element
  values assignment is finished and only then continue


### Task 1:

The implementation of Barrier synchronisation object is described in Classes section and
the main difference is that Event signaling object can be manually set to clean state by calling it's clear method.
In this case we clear events after the signal unlocks all awaited code. In the outputs below we can see that all threads are
awaited before entering execution of code after barrier.wait() method call.

#### Output for default implementation of SimpleBarrier with Semaphore:

```
thread 0 before barrier
thread 3 before barrier
thread 2 before barrier
thread 4 before barrier
thread 1 before barrier
thread 1 after barrier
thread 4 after barrier
thread 0 after barrier
thread 2 after barrier
thread 3 after barrier
```

#### Output for implementation of SimpleBarrier with Event:

```
thread 0 before barrier
thread 3 before barrier
thread 4 before barrier
thread 1 before barrier
thread 2 before barrier
thread 2 after barrier
thread 0 after barrier
thread 4 after barrier
thread 1 after barrier
thread 3 after barrier
```

### Task 2:

Here we are challenged to use the Sempahore/Barrier mechanism in order to achieve synchronized 
execution of code in multiple threads running in infinite while loop. The solution can be, in case of
SimpleBarrier with Event used as signaling object, pretty easy because this implementation clears the event state
after iterating all over the threads and checking their state. We only call the barrier.wait() method before each test method.
In the output we can see synchronised execution of code between threads and also a small optimalisation in the moment where the 
thread which ends up calling event.signal() starts first with code execution because it is the currently active thread.

#### Output for implementation of reusable SimpleBarrier with Event:

```
ko: Thread 4
ko: Thread 3
ko: Thread 0
ko: Thread 1
ko: Thread 2
rendezvous: Thread 2
rendezvous: Thread 3
rendezvous: Thread 0
rendezvous: Thread 1
rendezvous: Thread 4
ko: Thread 4
ko: Thread 2
ko: Thread 3
ko: Thread 0
ko: Thread 1
```

### Task 3:

In this task we create array for our fibonacci sequence
and then start by locking before the process of creating Threads calling fibonacci_compute
function on current element. The call of the function starts with sleep to demonstrate the de-sync of processes, performs computation and then unlocks the Mutex
and tells the signaling object to await others in this point to ensure that the element values assignment is finished and only then continue the code execution.

#### Desynchronised output of fibonacci computation between threads:

```
thread: 6
thread: 3
thread: 2
thread: 0
thread: 9
thread: 5
thread: 7
thread: 8
thread: 4
thread: 1
[0, 1, 1, 1, 1, 2, 3, 0, 0, 0, 0, 0]
```

#### Output for implementation of synchronised fibonacci computation:

```
thread: 0
thread: 1
thread: 2
thread: 3
thread: 4
thread: 5
thread: 6
thread: 7
thread: 8
thread: 9
[0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89]
```
