from time import sleep
from random import randint
from fei.ppds import Event, Mutex, Semaphore, Thread

from main import SimpleBarrier

"""
    Awaited print from module fei.ppds
"""
from fei.ppds import print

THREADS = 10


"""
    This code snippet displays how to ensure that the fibonacii calculation
    of elements on index i and i + 1 are already calculated
    and assigned in the moment of the
    current i + 2 indexed element calculation
"""


def compute_fibonacci(i, mut, sema):
    """
        Method that expect index of first element in equation, Mutex
        and Semaphore/Event starts with sleep to demonstrate the de-sync
        of processes and then unlocks the Mutex and tells the signaling
        object to await others in this point to ensure that the element
        values assignment is finished and only then continue
    """
    sleep(randint(1, 10) / 10)
    print('thread: %s' % i)
    fib_seq[i + 2] = fib_seq[i] + fib_seq[i + 1]
    mut.unlock()
    sema.wait()


if __name__ == '__main__':
    """
        In the main part of this snippet we create array for our
        fibonacci sequence and then start locked process of
        creating Threads calling fibonacci_compute
        function on current element. After the call is
        finished we signal other processes that they can continue
    """
    fib_seq = [0] * (THREADS + 2)
    fib_seq[1] = 1
    sb = SimpleBarrier(THREADS)
    threads = list()
    sem = Event()
    # sem = Semaphore()
    mutex = Mutex()
    for i in range(THREADS):
        mutex.lock()
        t = Thread(compute_fibonacci, i, mutex, sem)
        threads.append(t)
        sem.signal()

    for t in threads:
        t.join()
    print(fib_seq)
