# Filip Kadúch - parallel programming and distributed systems: Documentation

## Assignment 5

#### Python version:
  3.8
#### Modules:
  from fei.ppds import Mutex, print, Semaphore, Thread
  
  from random import randint
  
  from time import sleep  

### Task 1. Smokers-Agents synchronization problem:
  In the case of a modification in which the agent is not waiting for signaling of resource allocation, solve the problem of favoring smokers and describe this solution in   the documentation in an appropriate manner. 

#### Classes:

##### 1. Shared
  ###### Attributes:
      mutex - Mutex object doing the synchronization between threads
      pusher_match, pusher_paper, pusher_tobacco - Signaling objects which for specific resource type signal appearance on 'table'
      tobacco, paper, match - Signaling objects for specific resource type
      is_tobacco, is_paper, is_match - counters for specific resource type
      agent_sem - global Semaphore signaling to start with supply

#### Methods: 
##### 1. smoker_match/paper/tobacco(Shared)
    Smoker type methods in this context waits for signal that it's required
    missing resource (match in this case, can be also paper or tobacco)
    appeared on the 'table' and then moves to the usage of
    resource and then signals consumption of resource. After that it starts it's
    process with the build up of product e.g. smoke the cigarette.

##### 2. agent_1/2/3(Shared)
    Agent type methods in this context starts with simulation of production of
    it's resource type (tobacco, paper, match) and then waits for the global signal of shortage
    which launches process in which smoker who currently has specific combination of resources can
    ask for agent-specific produced resource, In case of first agent it produces match so it sends
    signal to part of code which handles business with match. That means it provides match
    to smoker who currently has paper and tobacco ready.

##### 3. pusher_match/tobacco/paper(Shared)
    Pusher type methods in this context waits for it's type of resource to be
    produced then checks what content is available and lastly who
    should be able to take it.
    In case of no suitable smoker it just leaves the product on the 'table'.
    In our assignment we have 3 types of content to be produced and 3 different
    type of consumers with different requirements.
    
#### Output for our implementation:

```
agent: tobacco, paper --> match
"match": makes cig
"match": smokes"
agent: tobacco, match --> paper
"paper": makes cig
"paper": smokes"
agent: tobacco, paper --> match
"match": makes cig
"match": smokes"
agent: tobacco, match --> paper
"paper": makes cig
"paper": smokes"
agent: tobacco, paper --> match
"match": makes cig
"match": smokes"
agent: paper, match --> tobacco
"tobacco": makes cig
"tobacco": smokes"
agent: tobacco, match --> paper
"paper": makes cig
"paper": smokes"
agent: tobacco, match --> paper
"paper": makes cig
"paper": smokes"
agent: tobacco, match --> paper
"paper": makes cig
"paper": smokes"
agent: tobacco, paper --> match
"match": makes cig
"match": smokes"
agent: paper, match --> tobacco
"tobacco": makes cig
"tobacco": smokes"
agent: tobacco, match --> paper
"paper": makes cig
"paper": smokes"
```

### Task 2. Dinning savages synchronization problem:
  There are several chefs in the tribe. When the savage finds out that the pot is empty, he wakes up ALL the chefs who can help each other cook and cook together. ONLY ONE chef will tell the waiting savage that he is cooked. The chef puts portions into the pot, not savages! 
  1. Find out what combination of sync issues this is
  2. Write the pseudocode of the solution
  3. Place suitable statements to verify the functionality of the model
  4. Choose the appropriate characteristics on which the model is based 

#### Classes:
##### 1. SimpleBarrier
    This class represents SimpleBarrier synchronisation mechanism used in order to await specific number of
    cooking processes and only then perform serving of the dinner.
  ###### Attributes:
    count - counter for ready in queue savages/cooks
    mutex - Mutex object locking of processes between threads to keep integrity
    barrier - Semaphore for full queue ready to perform
    wait - method preforming the waiting action of savage/cook in ready state, if the last
    one comes/finishes cooking, then it sends signal to continue with code.
      
##### 2. Shared
  Class representation of shared object between threads controlling the flow of the dinner.
  ###### Attributes:
    mutex - Mutex object doing the synchronization between threads
    empty_pot, full_pot - Signaling objects for the state of pot
    servings - number of servings served per cook and order
    cook_barrier1, cook_barrier2 - Barriers controlling the state of savages and cooks
      
#### Methods: 
##### 1. savage(i, Shared)
  - This methods simulates the dinning process of one savage. In the beginning we
  check if the pot is empty. In this case we signal cooks to start cooking and wait.
  Otherwise we move onto eating (removing resource from storage)

##### 2. cook(i, Shared)
  -  This method simulates the process of cooking where we first wait for all cooks
  to get ready and start cooking the meals all at once and keep until all 5 of them finishes.
  After that only one cook serves the dinner to savages and by that sends signal that pot is full.

#### Pseudocode: 

```
def main():
    servings = 0
    shared = Shared(servings)
    full_pot = Semaphore(0)
    empty_pot = Semaphore(0)
    mutex = Mutex()
 
    barrier1 = SimpleBarrier()
    barrier2 = SimpleBarrier()
 
    for savage_id in 0, number_of_savages:
        create_and_run_thread(savage, savage_id)
       
    for savage_id in 0, number_of_cooks:
        create_and_run_thread(cook, cook_id)
 
def savage(savage_id):
    while True:
        mutex.lock()
        if servings == 0:
            empty_pot.signal()
            full_pot.wait()
        servings -= 1
        mutex.unlock()
 
def cook():
    while True:
        empty_pot.wait()
        barrier1.wait("Cooking",
                      cook_id,
                      print_each_thread = True
                      empty_pot)
        barrier2.wait("Cooking done",
                      savage_id,
                      print_last_thread = True
                      full_pot)
        servings += number_of_meals
        full_pot.signal()
```


#### Print outputs on reasonable places:
Actual lines of outputs printing can be seen in code.
[Code](main.py)

```Savage "{i}": empty pot``` print in savage() if the number of servings is 0

```Savage "{i}": take from pot``` print in savage() if there is meal he can take

```Savage "{i}": eating``` print in savage() at the end to simulate eating process

```Cook "{i}": cooking``` print in SimpleBarrier called from cook() after signal for empty pot and if they aren't all ready yet

```Cook "{i}": servings --> pot``` print  in SimpleBarrier called from cook() 

#### Model characteristics:
As described above in methods and classes section, but notable thing is time of cooking is the same as time of eating process in savage.

#### Output for our implementation:

As we can see our synchronization pattern produces output where ONE Savage announces empty state of pot and then cooks awake and begin to cook. If all of them finish this process then the last ONE who sees that the pot is full serves the dinner to savages. Savages then iterate over themselves and take/eat portions of food until the pot is empty. And this process repeats infinitly.

```
Savage "8": empty pot
Cook "5": cooking
Cook "2": cooking
Cook "3": cooking
Cook "0": cooking
Cook "1": cooking
Cook "4": cooking
Cook "0": servings --> pot
Savage "8": take from pot
Cook "0": cooking
Savage "8": eating
Savage "4": take from pot
Cook "3": cooking
Savage "4": eating
Savage "1": take from pot
Cook "5": cooking
Savage "1": eating
Savage "0": empty pot
Cook "1": cooking
Cook "2": cooking
Cook "4": cooking
Cook "0": servings --> pot
Savage "0": take from pot
Cook "0": cooking
Savage "0": eating
Savage "6": take from pot
Cook "5": cooking
Savage "6": eating
Savage "9": take from pot
Cook "3": cooking
Savage "9": eating
Savage "3": empty pot
```
