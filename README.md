# Filip Kadúch - parallel programming and distributed systems: Documentation

## Assignment 4

#### Python version:
  3.8
#### Modules:
  - from random import randint
  - from time import sleep
  - from fei.ppds import Event, Mutex, print, Semaphore, Thread

#### Tasks:
  There is a task with powerplant monitoring of sensors synchronization (3 sensors, 8 monitors) which solution needs to contain following:
  1. Analyze what types of synchronization tasks (or their modifications or combinations) are involved in this task.
  2. Exactly map the selected synchronization tasks (primitives) to the individual parts of the assignment.
  3. Write the pseudocode of the problem solution.
  4. Write a program that will be suitable for modeling this synchronization task.
  5. Add output before simulation of update and during reading phase
  Monitors can only work if they have already delivered all the valid data to the storage. 
  
#### Classes:
##### 1. Lightswitch
  Class representation of synchronization mechanism working with mutex and counting the number of processings
  ###### Attributes:
        mutex - Mutex object doing the synchronization between threads
        counter - counter starting from 0 which represents number of processes in storage
        lock(Semaphore) - method that locks current "value" in storage and returns number of stored processes
        unlock(Semaphore) - calling this method unlocks one "value" currently "stored" in storage. If the storage is empty Semaphore sends signal
        
#### Methods: 
##### 1. monitor(monitor_id, Event, Semaphore, Lightswitch, Semaphore)
  - Method that simulates monitor-like event in powerplant in way that it waits for all the "sensor" processes to be piled up in lightswitch and after that receives signal that "sensor's data" is valid for monitoring. And moves onto loop where it sleeps for the time of sensor actualisation and then blocks sensors from other actions with turnstile Semaphore and looks into "sensor data" for actualisations. After that sleeps for the purpose of reading process and sends signal through lightswitch to unlock accessed content for this monitoring instance.
  
##### 2. sensor(sensor_id, Event, Semaphore, Lightswitch, Semaphore)
  - Method that simulates sensor-like event in powerplant in way that it first checks if the turnstile is awaited in monitor. If not it continues the operation of locking access data which represents measured data from current sensor. Based on type of sensor it performs it's measuring action either for 10-20 ms or 20-25 ms for the last sensor. Then sleeps for the time of the action and sends the signal that there is valid data to monitor and unlocks the data for monitoring.

#### Synchronization mechanisms fitting our solution: 
  - Semaphore: we need to control code execution in two places which are at the beginning of sensoring process where we need to stop when there is ongoing monitoring and in our lightswitch class object which helps us with counting of processed threads and only then moves to other code
  - Mutex: our data writing/reading process has to locked up until the situation is safe to continue, mutex can help with that
  - Event: a plain signal that something basic happend can be useful in situation where we need to announce finalisation of sensoring and allow the launch of monitoring
  - Lightswitch: is a combination of Mutex and Semaphore synchronisation objects. Allows us to track number of proccessed threads and act like a countup/countdown emitter of signal. If specific number of times something happens it sends signal back to the Semaphore which can be used in code to execute/puase code.
#### Mapping of synchronization mechanisms to parts of assignment:
  - accessData: in order to represent signal after specific number of times the execution of code has been completed for either piled up data for monitoring or for the data that is accessed we will use Semaphore
  - turnstile: again Semaphore to control execution of code in sensors from monitoring unit. This will be checked at the beginning of each iteration
  - ls_monitor, ls_sensor: in order to abstract and watch specific number of units/processes for either monitoring or sensoring we need to use our class Lightswitch 
  - validData: valid data represents that there is some data measured and ready for monitoring so we can keep running some other code in monitor method in order to process it
#### Pseudocode: 

```
accessData = Semaphore(1)
turnstile = Semaphore(1)
ls_monitor = Lightswitch()
ls_sensor = Lightswitch()
validData = Event()
 
    for monitor_id in 0,7;:
        create_and_run_thread(monitor, monitor_id)
    for cidlo_id in 0,2:
        create_and_run_thread(sensor, sensor_id)
 
def monitor(monitor_id):
    validData.wait()
 
    while True:
        sleep(50-60 ms)
 
        turnstile.wait()
        monitor_readers = ls_monitor.lock(access_data)
        turnstile.signal()

        length_of_reading = 40 - 50 ms
        print(f'Monitor: "{monitor_id}",'
              f' Monitor readers count: "{monitor_readers}", Length of reading: "{length_of_reading}"\n')
              
        sleep(length_of_reading)
        ls_monitor.unlock(accessData)
 
def sensor(sensor_id):
    while True:
        turnstile.wait()
        turnstile.signal()
        sensor_writers = ls_sensor.lock(access_data)

        if sensor == P/T
            length_of_writing = 20 - 25 ms
        else
            length_of_writing = 10 - 20 ms
            
        print(f'Sensor: "{sensor_id}", Writing sensors count: "{sensor_writers}",'
              f' Length of writing: "{length_of_writing:.3f}"\n')
              
        sleep(length_of_writing)
        
        validData.signal()
        ls_sensor.unlock(accessData)
```

#### Actual code implementation:
[Code](main.py)

#### Output for our solution:

```
Sensor: "0", Writing sensors count: "0", Length of writing: "0.019"
Sensor: "1", Writing sensors count: "1", Length of writing: "0.018"
Sensor: "2", Writing sensors count: "2", Length of writing: "0.024"
Sensor: "0", Writing sensors count: "2", Length of writing: "0.012"
Sensor: "1", Writing sensors count: "2", Length of writing: "0.017"
Sensor: "0", Writing sensors count: "2", Length of writing: "0.017"
Sensor: "2", Writing sensors count: "2", Length of writing: "0.022"
Sensor: "1", Writing sensors count: "2", Length of writing: "0.010"
Sensor: "1", Writing sensors count: "2", Length of writing: "0.015"
Sensor: "2", Writing sensors count: "2", Length of writing: "0.025"
Sensor: "0", Writing sensors count: "2", Length of writing: "0.019"
Monitor: "5", Monitor readers count: "0", Length of reading: "0.052"
Monitor: "7", Monitor readers count: "1", Length of reading: "0.055"
Monitor: "1", Monitor readers count: "2", Length of reading: "0.051"
Monitor: "0", Monitor readers count: "3", Length of reading: "0.059"
Monitor: "6", Monitor readers count: "4", Length of reading: "0.058"
Monitor: "4", Monitor readers count: "5", Length of reading: "0.058"
Monitor: "3", Monitor readers count: "6", Length of reading: "0.058"
Monitor: "2", Monitor readers count: "7", Length of reading: "0.052"
Sensor: "2", Writing sensors count: "2", Length of writing: "0.020"
Sensor: "0", Writing sensors count: "2", Length of writing: "0.014"
Sensor: "1", Writing sensors count: "2", Length of writing: "0.016"
Sensor: "0", Writing sensors count: "2", Length of writing: "0.012"
Sensor: "0", Writing sensors count: "2", Length of writing: "0.020"
Sensor: "2", Writing sensors count: "2", Length of writing: "0.022"
Sensor: "1", Writing sensors count: "2", Length of writing: "0.017"
Sensor: "0", Writing sensors count: "2", Length of writing: "0.019"
Sensor: "1", Writing sensors count: "2", Length of writing: "0.010"
Sensor: "2", Writing sensors count: "2", Length of writing: "0.024"
Sensor: "1", Writing sensors count: "2", Length of writing: "0.011"
Sensor: "1", Writing sensors count: "2", Length of writing: "0.016"
Sensor: "2", Writing sensors count: "2", Length of writing: "0.020"
```
