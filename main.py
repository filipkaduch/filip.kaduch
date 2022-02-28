from random import randint
from time import sleep
from fei.ppds import Event, Mutex, Semaphore, Thread

"""
    Awaited print from module fei.ppds
"""
from fei.ppds import print


THREADS = 5

"""
    This code snippet displays 2 of possible implementations of
    Barrier - process synchronization mechanism
"""


class SimpleBarrier:
    """
        SimpleBarrier:
            n - number of threads to await
            counter - current index of thread
            mutex - Mutex object doing the synchronization
            event - signaling object
    """
    def __init__(self, n):
        self.n = n
        self.counter = 0
        self.mutex = Mutex()
        self.event = Event()

    def wait(self):
        """
            Method that iterates over 'threads' and locks
            the process of each thread before execution and unlocking after.
            Then we tell our SignalingObject to await for signal which comes
            after full iteration cycle. In this case
            we clear events after the signal unlocks all of the awaited
        """
        self.mutex.lock()
        self.counter += 1
        if self.counter == self.n:
            self.counter = 0
            self.event.signal()
        self.mutex.unlock()
        self.event.wait()
        self.event.clear()


class SimpleBarrierWithSemaphore:
    """
        SimpleBarrierWithSemaphore:
            n - number of threads to await
            counter - current index of thread
            mutex - Mutex object doing the synchronization
            semaphore - signaling object
    """
    def __init__(self, n):
        self.n = n
        self.counter = 0
        self.mutex = Mutex()
        self.semaphore = Semaphore(0)

    def wait(self):
        self.mutex.lock()
        self.counter += 1
        if self.counter == self.n:
            self.counter = 0
            self.semaphore.signal(self.n)
        self.mutex.unlock()
        self.semaphore.wait()


def barrier_example(barrier, thread_id):
    """
        This method demonstrates the usage of barrier implemented
        with event/semaphore which allows correct awaiting in code
        of processes launched in different threads.
        This feature is displayed in the output that shows the barrier
        holds the threads running this method until
        all of them reach this point.
    """
    sleep(randint(1, 10) / 10)
    print("thread %d before barrier" % thread_id)
    barrier.wait()
    print("thread %d after barrier" % thread_id)


if __name__ == '__main__':
    sb = SimpleBarrier(THREADS)

    threads = [Thread(barrier_example, sb, i) for i in range(THREADS)]
    [t.join() for t in threads]
