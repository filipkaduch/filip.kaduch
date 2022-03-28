"""
    randint, sleep - required for simulation of molecule operations
    Mutex, print, Semaphore, Thread - synchronization objects
"""

from fei.ppds import Mutex, print, Semaphore, Thread
from random import randint
# from time import sleep

"""
    This code snippet displays the solution of H2O molecules forming problem
    with synchronization mechanisms
"""

O_count = 1
H = 2


class SimpleBarrier:
    """
        This class represents SimpleBarrier synchronisation mechanism used in
        order to await specific number of molecule processes and only then
        perform bonding of the molecules.
        Attributes:
            N - number to await
            count - counter for ready in queue hydrogen/oxygen
            mutex - Mutex object locking of processes between
                threads to keep integrity
            barrier - Semaphore for full queue of molecules ready to perform
            wait - method preforming the waiting action of hydrogen/oxygen
                in ready state, if the last one hydrogen/oxygen
                needed for formation comes, then it sends signal to
                continue with code.
    """

    def __init__(self, number):
        self.N = number
        self.count = 0
        self.mutex = Mutex()
        self.barrier = Semaphore(0)

    def wait(self, mol_type=None):
        self.mutex.lock()
        self.count += 1
        if self.count == self.N:
            if mol_type:
                print(mol_type)
            self.count = 0
            self.barrier.signal(self.N)

        self.mutex.unlock()
        self.barrier.wait()


class Shared:
    """
        Class representation of shared object between threads controlling the
        flow of the molecule transformation.
        Attributes:
            mutex - Mutex object doing the synchronization between threads
            oxy, hydro - Signaling objects for the state of hydrogen/oxygen
            oxygen, hydrogen - number of hydrogen/oxygen
            oxygen_barrier, hydrogen_barrier - Barriers controlling the state
                of oxygen and hydrogen
    """

    def __init__(self):
        self.oxygen = 0
        self.hydrogen = 0
        self.mutex = Mutex()
        self.oxy = Semaphore(0)
        self.hydro = Semaphore(0)

        self.oxygen_barrier = SimpleBarrier(O_count)
        self.hydrogen_barrier = SimpleBarrier(H)


def hydrogen(shared):
    """
        This methods simulates the hydrogen molecule process.
        In the beginning we lock our process because we are going to modify
        our shared object hydrogen counter and then check whether we can start formation
        or we have to wait for other molecules to appear.
        Attributes:
            shared - object of type Shared which is modified between Threads
    """
    print('Hydrogen molecule')
    # sleep(randint(1, 100) / 100)
    shared.mutex.lock()
    shared.hydrogen += 1
    if shared.hydrogen < 2 or shared.oxygen < 1:
        print('Current hydrogen number: ', shared.hydrogen)
        print('Current oxygen number: ', shared.hydrogen)
        shared.mutex.unlock()
    else:
        shared.oxygen -= 1
        shared.hydrogen -= 2
        print('Removing hydrogen number: ', shared.hydrogen)
        print('Removing oxygen number: ', shared.hydrogen)
        shared.oxy.signal()
        shared.hydro.signal(2)

    shared.hydro.wait()
    bond()
    shared.hydrogen_barrier.wait(mol_type=f'Hydrogen')


def bond():
    print('Bonding')
    # sleep(randint(1, 100) / 100)


def oxygen(shared):
    """
        This methods simulates the oxygen molecule process.
        In the beginning we lock our process because we are going to modify
        our shared object oxygen counter and then check whether we can start formation
        or we have to wait for other molecules to appear. We only have one awaited oxygen
        molecule during bonding so we can use this as mutex unlocker which is absent in
        else branch.
        Attributes:
            shared - object of type Shared which is modified between Threads
    """
    print('Oxygen molecule')
    # sleep(randint(1, 100) / 100)
    shared.mutex.lock()
    shared.oxygen += 1
    if shared.hydrogen < 2:
        print('Current hydrogen number: ', shared.hydrogen)
        print('Current oxygen number: ', shared.hydrogen)
        shared.mutex.unlock()
    else:
        shared.oxygen -= 1
        shared.hydrogen -= 2
        print('Removing hydrogen number: ', shared.hydrogen)
        print('Removing oxygen number: ', shared.hydrogen)
        shared.oxy.signal()
        shared.hydro.signal(2)

    shared.oxy.wait()
    bond()
    shared.oxygen_barrier.wait(mol_type=f'Oxygen')
    shared.mutex.unlock()


def main():
    """
        Main part of our experimentation generating hydrogen and oxygen infinitely.
    """
    shared = Shared()

    while True:
        if randint(1, 2) == 1:
            Thread(hydrogen, shared)
        else:
            Thread(oxygen, shared)


if __name__ == '__main__':
    main()
