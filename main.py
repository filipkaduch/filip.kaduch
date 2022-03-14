"""
    randint, sleep - required for simulation of storage operations
    Event, Mutex, print, Semaphore, Thread - synchronization objects
"""

from fei.ppds import Event, Mutex, print, Semaphore, Thread
from random import randint
from time import sleep

"""
    This code snippet displays the solution of powerplant monitoring problem
    with synchronization mechanisms
"""


class Lightswitch:
    """
        Class representation of synchronization mechanism working with
        mutex and counting the number of processed threads
        Attributes:
            mutex - Mutex object doing the synchronization between threads
            counter - number counter starting from 0 which represents
                number of awaited processes
            lock - method that locks current "value" in storage and returns number of stored processes
            unlock - calling this method unlocks one "value" currently "stored" in storage.
                If the storage is empty Semaphore sends signal
    """
    def __init__(self):
        self.mutex = Mutex()
        self.counter = 0

    def lock(self, sem):
        self.mutex.lock()
        counter = self.counter
        self.counter += 1
        if self.counter == 8:
            sem.wait()
        self.mutex.unlock()
        return counter

    def unlock(self, sem):
        self.mutex.lock()
        self.counter -= 1
        if self.counter == 0:
            sem.signal()
        self.mutex.unlock()


def monitor(monitor_id, valid_data, turnstile, ls_monitor, access_data):
    """
        Method that simulates monitor-like event in powerplant in way that it waits for all
        the "sensor" processes to be piled up in lightswitch and after that receives signal that
        "sensor's data" is valid for monitoring. And moves onto loop where it sleeps for the time
        of sensor actualisation and then blocks sensors from other actions with turnstile
        Semaphore and looks into "sensor data" for actualisations. After that sleeps for the
        purpose of reading process and sends signal through lightswitch to unlock accessed
        content for this monitoring instance.
        Attributes:
            monitor_id - id of current monitoring unit
            valid_data - event waiting for updated content to look in monitor
            turnstile - Semaphore
            ls_monitor - Lightswitch class object
            access_data - event signaling accessed/monitored data in monitor
    """
    valid_data.wait()

    while True:
        length_of_sensor_actualisation = randint(50, 60) / 1000
        sleep(length_of_sensor_actualisation)
        turnstile.wait()
        monitor_readers = ls_monitor.lock(access_data)
        turnstile.signal()

        length_of_reading = randint(40, 50) / 1000
        print(f'Monitor: "{monitor_id}",'
              f' Monitor readers count: "{monitor_readers}", Length of reading: "{length_of_reading}"\n')
        sleep(length_of_reading)
        ls_monitor.unlock(access_data)


def sensor(sensor_id, valid_data, turnstile, ls_sensor, access_data):
    """
    Method that simulates sensor-like event in powerplant in way that it first
    checks if the turnstile is awaited in monitor. If not it continues the operation
    of locking access data which represents measured data from current sensor.
    Based on type of sensor it performs it's measuring action either for 10-20 ms or
    20-25 ms for the last sensor. Then sleeps for the time of the action and sends
    the signal that there is valid data to monitor and unlocks the data for monitoring.
        Attributes:
            sensor_id - id of current sensoring unit
            valid_data - event signaling updated content to look in monitor
            turnstile - Semaphore to lock the process during monitoring
            ls_monitor - Lightswitch class object
            access_data - event signaling measured data in sensor
    """
    while True:
        turnstile.wait()
        turnstile.signal()
        sensor_writers = ls_sensor.lock(access_data)

        if sensor_id > 1:
            length_of_writing = randint(20, 25) / 1000
        else:
            length_of_writing = randint(10, 20) / 1000
        print(f'Sensor: "{sensor_id}", Writing sensors count: "{sensor_writers}",'
              f' Length of writing: "{length_of_writing:.3f}"\n')
        sleep(length_of_writing)
        valid_data.signal()
        ls_sensor.unlock(access_data)


def main():
    """
        Main part of our experimentation launching 3 sensors for 8 monitoring units.
    """
    access_data = Semaphore(1)
    turnstile = Semaphore(1)
    ls_monitor = Lightswitch()
    ls_sensor = Lightswitch()
    valid_data = Event()

    for sensor_id in range(3):
        Thread(sensor, sensor_id, valid_data, turnstile, ls_sensor, access_data)
    for monitor_id in range(8):
        Thread(monitor, monitor_id, valid_data, turnstile, ls_monitor, access_data)


if __name__ == '__main__':
    main()
