"""
    randint, sleep - required for simulation of storage operations
    Mutex, print, Semaphore, Thread - synchronization objects
    matplotlib.pyplot - graph plotting
    numpy - array for graph plotting
"""
from fei.ppds import Mutex, print, Semaphore, Thread
import matplotlib.pyplot as plt
import numpy as np
from random import randint
from time import sleep


"""
    This code snippet displays the usage of Producer-Consumer
    synchronization pattern
"""


class Shared(object):
    """
        Class representation of shared object between threads.
        Initialization requires integer value N to declare storage limit

        Attributes:
            finished - Boolean value representing end of the process
            mutex - Mutex object doing the synchronization between threads
            free - Semaphore representation of free space
                in our "storage" starting on N
            items - Semaphore representation of occupied
                space in our "storage" starting on 0
            counter - number counter starting from 0 which represents
            save_item - method that represents incrementation
                of number of saved items in object
    """
    def __init__(self, n):
        self.finished = False
        self.mutex = Mutex()
        self.counter = 0
        self.free = Semaphore(n)
        self.items = Semaphore(0)

    def save_item(self):
        self.mutex.lock()
        self.counter += 1
        self.mutex.unlock()


def producer(shared, production_time):
    """
        First part of our synchronization pattern - Producer, starts with
        simulation of production, then moves to a control segment of free space
        which awaits signal about current free space from Consumer.
        After that we move onto locking our code in order to perform
        safe way of manipulation with product in storage.
        We unlock the code and let the 'items' semaphore know that
        the storage count is incremented.
        At the end we are checking global finished state of the process and in
        case of not finished process.
        Producer gets blocked when the storage (free) is full.

        :param production_time: time for production simulation
        :param shared: Shared object between threads
    """
    while True:
        sleep(production_time / 25)
        print('P')
        shared.free.wait()
        shared.save_item()
        shared.items.signal()
        if shared.finished:
            break


def consumer(shared):
    """
        Second part of our synchronization pattern - Consumer, starts with
        the control segment of items space which awaits signal about current
        items production from producer. After that we unlock the code and
        signal consumption to Shared object and simulate the process of product
        consumption. Consumer gets blocked when the storage (items) is empty.

        :param shared: Shared object between threads
    """
    while True:
        shared.items.wait()
        print('C')
        shared.free.signal()
        sleep(randint(0, 10) / 25)
        if shared.finished:
            break


# Borrowed and modified from matplotlib's documentation:
# https://matplotlib.org/stable/gallery/mplot3d/trisurf3d.html
def plot_graph(matrix):
    """
        Method for displaying results of observation of number of products
        produced per unit of time

        :param matrix: array of arrays with length 3,
        index 0 - production time,
        index 1 - consumption number,
        index 2 - average items produced per iteration
    """
    x = []
    for item in matrix:
        x.append(item[0])
    y = []
    for item in matrix:
        y.append(item[1])
    z = []
    for item in matrix:
        z.append(item[2])
    axes = plt.figure().add_subplot(projection='3d')
    axes.set_xlabel('Time')
    axes.set_ylabel('Consumers')
    axes.set_zlabel('Products')
    axes.plot_trisurf(np.array(x), np.array(y), np.array(z),
                      cmap='viridis', edgecolor='none')
    plt.show()


def main():
    """
        Main part of our experimentation.
    """
    matrix = []
    for production_time in range(10):
        for consume in range(1, 11):
            items_sum = 0
            iters = 10
            for i in range(iters):
                s = Shared(10)
                c = [Thread(consumer, s) for _ in range(4)]
                p = [Thread(producer, s, production_time) for _ in range(4)]
                sleep(0.5)
                s.finished = True
                print(f'MAIN THREAD {i}: AWAITING FINISH')
                s.items.signal(100)
                s.free.signal(100)
                [t.join() for t in c + p]
                print(f'MAIN THREAD {i}: PROGRAM FINISHED')
                print(matrix)
                items_time = s.counter / 0.5
                items_sum += items_time
            avg_items = items_sum / iters
            matrix.append([production_time / 25, consume, avg_items])

    plot_graph(matrix)


if __name__ == '__main__':
    main()
