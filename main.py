"""
    randint, sleep - required for simulation of storage operations
    Mutex, print, Semaphore, Thread - synchronization objects
"""

from fei.ppds import Mutex, print, Semaphore, Thread
from random import randint
from time import sleep

"""
    This code snippet displays the solution of dining savages problem
    with synchronization mechanisms
"""


M = 3
N = 10
C = 6


class SimpleBarrier:
    """
        This class represents SimpleBarrier synchronisation mechanism used in
        order to await specific number of cooking processes and only then
        perform serving of the dinner.
        Attributes:
            count - counter for ready in queue savages/cooks
            mutex - Mutex object locking of processes between
                threads to keep integrity
            barrier - Semaphore for full queue ready to perform
            wait - method preforming the waiting action of savage/cook
                in ready state, if the last one comes/finishes cooking,
                then it sends signal to continue with code.
    """
    def __init__(self, number):
        self.N = number
        self.count = 0
        self.mutex = Mutex()
        self.barrier = Semaphore(0)

    def wait(self, each=None, last=None, empty_pot=None, shared=None):
        self.mutex.lock()
        self.count += 1
        if each:
            print(each)
        if self.count == self.N:
            if shared:
                shared.servings += M
                shared.full_pot.signal()
            if last:
                print(last)
            self.count = 0
            self.barrier.signal(self.N)
        if empty_pot:
            empty_pot.signal()
        self.mutex.unlock()
        self.barrier.wait()


class Shared:
    """
        Class representation of shared object between threads controlling the
        flow of the dinner.
        Attributes:
            mutex - Mutex object doing the synchronization between threads
            empty_pot, full_pot - Signaling objects for the state of pot
            servings - number of servings served after an order
            cook_barrier1, cook_barrier2 - Barriers controlling the state
                of savages and cooks
    """
    def __init__(self, m):
        self.servings = m
        self.mutex = Mutex()
        self.empty_pot = Semaphore(0)
        self.full_pot = Semaphore(0)

        self.cook_barrier1 = SimpleBarrier(C)
        self.cook_barrier2 = SimpleBarrier(C)


def savage(i, shared):
    """
        This methods simulates the dinning process of one savage.
        In the beginning we check if the pot is empty. In this
        case we signal cooks to start cooking and wait.
        Otherwise we move onto eating (removing resource from storage)
        Attributes:
            i - id of current savage and his dinning process
            shared - object of type Shared which is modified between Threads
    """
    sleep(randint(1, 100) / 100)
    while True:
        shared.mutex.lock()
        if shared.servings == 0:
            print(f'Savage "{i}": empty pot')
            shared.empty_pot.signal()
            shared.full_pot.wait()

        print(f'Savage "{i}": take from pot')
        shared.servings -= 1
        shared.mutex.unlock()
        print(f'Savage "{i}": eating')
        sleep(randint(50, 200) / 100)


def cook(i, shared):
    """
        This method simulates the process of cooking where we first wait
        for all cooks to get ready and start cooking the meals all at
        once and keep until all 5 of them finishes.
        After that only one cook serves the dinner to savages and by that
        sends signal that pot is full.
        Attributes:
            i - id of current savage and his cooking process
            shared - object of type Shared which is modified between Threads
    """
    sleep(randint(1, 100) / 100)
    while True:
        shared.empty_pot.wait()
        shared.cook_barrier1.wait(each=f'Cook "{i}": cooking',
                                  empty_pot=shared.empty_pot)
        shared.cook_barrier2.wait(last=f'Cook "{i}": servings --> pot',
                                  shared=shared)


def main():
    """
        Main part of our experimentation.
    """
    shared = Shared(0)
    savages = []

    for n in range(N):
        savages.append(Thread(savage, n, shared))

    for i in range(C):
        savages.append(Thread(cook, i, shared))

    for t in savages:
        t.join()


if __name__ == '__main__':
    main()
