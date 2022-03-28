# Filip Kadúch - parallel programming and distributed systems: Documentation

## Assignment 6

#### Python version:
  3.8
#### Modules:
  from fei.ppds import Mutex, print, Semaphore, Thread
  from random import randint
  from time import sleep


#### Tasks:
  Formation of water molecules:
  1. correct timing of model activities
  2. verification (for example, by checking suitably located statements)

#### Classes:
##### 1. SimpleBarrier
  This class represents SimpleBarrier synchronisation mechanism used in
  order to await specific number of molecule processes and only then
  perform bonding of the molecules.
  ###### Attributes:
      N - number to await
      count - counter for ready in queue hydrogen/oxygen
      mutex - Mutex object locking of processes between
          threads to keep integrity
      barrier - Semaphore for full queue of molecules ready to perform
      wait - method preforming the waiting action of hydrogen/oxygen
          in ready state, if the last one hydrogen/oxygen
          needed for formation comes, then it sends signal to
          continue with code.
          
##### 1. Shared
  Class representation of shared object between threads controlling the
  flow of the molecule transformation.
  ###### Attributes:
    mutex - Mutex object doing the synchronization between threads
    oxy, hydro - Signaling objects for the state of hydrogen/oxygen
    oxygen, hydrogen - number of hydrogen/oxygen
    oxygen_barrier, hydrogen_barrier - Barriers controlling the state
        of oxygen and hydrogen

#### Methods: 
##### 1. hydrogen(Shared)
  This methods simulates the hydrogen molecule process.
  In the beginning we lock our process because we are going to modify
  our shared object hydrogen counter and then check whether we can start formation
  or we have to wait for other molecules to appear.

##### 2. oxygen(Shared)
  This methods simulates the oxygen molecule process.
  In the beginning we lock our process because we are going to modify
  our shared object oxygen counter and then check whether we can start formation
  or we have to wait for other molecules to appear. We only have one awaited oxygen
  molecule during bonding so we can use this as mutex unlocker which is absent in
  else branch.


### Task:

We have placed outputs 'Hydrogen/Oxygen molecule' at the beginning of the each molecule process, then we output current count of molecules in that current process. If we have enough molecules to start bonding we output 'Removing hydrogen/oxygen' count. After that all 3 molecules needed start to bond together with output 'Bonding' and then move to output each passed molecule process name 'Hydrogen/Oxygen'.

#### Output for our solution:

```
Hydrogen molecule
Current hydrogen number:  1
Current oxygen number:  1
Oxygen molecule
Current hydrogen number:  1
Current oxygen number:  1
Hydrogen molecule
Removing hydrogen number:  0
Removing oxygen number:  0
Bonding
Bonding
Bonding
Hydrogen
Hydrogen
Oxygen
```

