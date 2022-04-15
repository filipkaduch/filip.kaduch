# Filip Kadúch - parallel programming and distributed systems: Documentation

## Assignment 8

#### Python version:
  3.8
#### Modules:
  asyncio - required for async/await syntax
  
  aiohttp - asynchronous HTTP client/server requests
  
  urllib.request - handler for opening URLs
  
  queue - multi-producer, multi-consumer queues
  
  time - used for tracking of elapsed time in task
  
  json - load response as dictionary
  
  os.path - check for todos.txt file existence


#### Task:
  Write your own (any) single-threaded application in two versions: synchronous and asynchronous (using native routines). Explain the purpose of the application in the enclosed documentation and make a performance comparison of the synchronous and asynchronous versions.
For this purpose we will use demonstrative code snippet that displays the implementation of basic/asynchronous versions of response text title's getter service from placeholder server and writing the title to file todos.txt conditionally.

#### Methods: 
##### 1. main()
  Main part of our experimentation with basic execution of tasks.
  We fill our async Queue with id's to fetch data from server and
  then proceed to asynchronously launch the tasks with
  list of id's to process all together.

##### 2. task(Queue, string)
  This methods first checks the multi-producer/consumer Queue state and
  then proceeds to iterate over queue content. During this loop
  we are getting data from placeholder server and then try to write
  placeholder title to file if it's not already gathered by previous
  task run.
  
##### 3. check(string)
  This methods checks for the existence of title in
  todos.txt file.

### Synchronous:
This implementation is based on our added 'scheduler' which handles lanuch and removal of tasks. The very own task is then required to yield it's execution to get back to this scheduler and remove the task after finish and launch the next one to handle next Queue item. We also have to check for the tasks array state during the whole process.

#### Output for our synchronous solution:

```
Task One running https://jsonplaceholder.typicode.com/todos/1
Task One elapsed time 0.063101
Task Two running https://jsonplaceholder.typicode.com/todos/2
Task Two elapsed time 0.057737
Task One running https://jsonplaceholder.typicode.com/todos/3
Task One elapsed time 0.073073
Task Two running https://jsonplaceholder.typicode.com/todos/4
Task Two elapsed time 0.052291
Task One running https://jsonplaceholder.typicode.com/todos/5
Task One elapsed time 0.070617
Task Two running https://jsonplaceholder.typicode.com/todos/6
Task Two elapsed time 0.073868
Task One running https://jsonplaceholder.typicode.com/todos/7
Task One elapsed time 0.083964
Task Two running https://jsonplaceholder.typicode.com/todos/8
Task Two elapsed time 0.052532
Task One running https://jsonplaceholder.typicode.com/todos/9
Task One elapsed time 0.056972
Total elapsed time 0.585106
```

#### Titles gathered in todos.txt:

```
Title: delectus aut autem, Task: One
Title: quis ut nam facilis et officia qui, Task: Two
Title: fugiat veniam minus, Task: One
Title: et porro tempora, Task: Two
Title: laboriosam mollitia et enim quasi adipisci quia provident illum, Task: One
Title: qui ullam ratione quibusdam voluptatem quia omnis, Task: Two
Title: illo expedita consequatur quia in, Task: One
Title: quo adipisci enim quam ut ab, Task: Two
Title: molestiae perspiciatis ipsa, Task: One
```

### Asynchronous:
In order to execute these tasks asynchronously we have to first let asyncio run our main operation and which has to be labeled async. We also need to use asyncio.Queue and await all operations related to this type of Queue. We don't need any scheduler because async/await syntax will manage the flow of launched
tasks through asyncio.gather. Task needs to be async as well and the client/server communication have to be managed in aiohttp.ClientSession() scope, again with all related operations awaited. Aiohttp allows us to run multiple asynchronous HTTP client/server requests because there is a session context for each one of them available.

#### Output for our asynchronous solution:

```
Task One running https://jsonplaceholder.typicode.com/todos/1
Task Two running https://jsonplaceholder.typicode.com/todos/2
Task Two elapsed time 0.065884
Task Two running https://jsonplaceholder.typicode.com/todos/3
Task One elapsed time 0.088094
Task One running https://jsonplaceholder.typicode.com/todos/4
Task Two elapsed time 0.024591
Task Two running https://jsonplaceholder.typicode.com/todos/5
Task One elapsed time 0.023242
Task One running https://jsonplaceholder.typicode.com/todos/6
Task Two elapsed time 0.024516
Task Two running https://jsonplaceholder.typicode.com/todos/7
Task One elapsed time 0.023898
Task One running https://jsonplaceholder.typicode.com/todos/8
Task Two elapsed time 0.055312
Task Two running https://jsonplaceholder.typicode.com/todos/9
Task One elapsed time 0.053351
Task Two elapsed time 0.027888
Total elapsed time 0.211651
```

#### Titles gathered in todos.txt:

```
Title: delectus aut autem, Task: One
Title: quis ut nam facilis et officia qui, Task: Two
Title: fugiat veniam minus, Task: One
Title: et porro tempora, Task: Two
Title: laboriosam mollitia et enim quasi adipisci quia provident illum, Task: One
Title: qui ullam ratione quibusdam voluptatem quia omnis, Task: Two
Title: illo expedita consequatur quia in, Task: One
Title: quo adipisci enim quam ut ab, Task: Two
Title: molestiae perspiciatis ipsa, Task: One
```

### Outcome of comparison:
We can see few important differences between these two implementation's execution, outcome and performance. First of all the basic version executes tasks one by one but actually launches the next task after the code completion. In this moment we are basically not saving any time with the usage of two tasks. The asynchronous version actually does save time in a way that it uses cooperative thread switching and the look-a-like multitasking. Task starts to gather data which takes specific amount of time but if previous one already gathered data on this url it can freely move to the next one because it has the information to do so (Elapsed time with higher difference then 40ms between basic/async version display this exact moment). In case of larger scale of urls and more tasks to process the requests the difference would be even bigger because the more tasks the bigger jump between proccessed url's.
