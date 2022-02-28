from time import sleep
from random import randint
from fei.ppds import Thread

"""
    Awaited print from module fei.ppds
"""
from fei.ppds import print
from main import SimpleBarrier, SimpleBarrierWithSemaphore

THREADS = 5

"""
    This code snippet displays the reusability of barrier object in
    synchronization tasks
"""


def rendezvous(thread_name):
    """
        Demonstrates after event call
    """
    sleep(randint(1, 10) / 10)
    print('rendezvous: %s' % thread_name)


def ko(thread_name):
    """
        Demonstrates before event call
    """
    print('ko: %s' % thread_name)
    sleep(randint(1, 10) / 10)


def barrier_cycle(barrier1, thread_name):
    """
        Barrier used in this method ensures that all threads
        await each other before the execution of ko method and
        also before calling of method rendezvous
    """
    while True:
        barrier1.wait()
        rendezvous(thread_name)
        barrier1.wait()
        ko(thread_name)


if __name__ == '__main__':
    """
        Here we create Threads calling barrier_cycle method and pass them
        our synchronisation object Barrier which can let itself know when to
        continue execution of code.
    """
    sb1 = SimpleBarrierWithSemaphore(THREADS)
    threads = list()
    for i in range(THREADS):
        t = Thread(barrier_cycle, sb1, 'Thread %d' % i)
        threads.append(t)

    for t in threads:
        t.join()
