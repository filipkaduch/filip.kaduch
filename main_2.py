"""
    randint, sleep - required for simulation of operations
    Mutex, print, Semaphore, Thread - synchronization objects
"""

from fei.ppds import Mutex, print, Semaphore, Thread
from random import randint
from time import sleep


class Shared:
    """
        Class representation of shared object between threads controlling the
        flow of consumption-production.
        Attributes:
            mutex - Mutex object doing the synchronization between threads
            pusher_match, pusher_paper, pusher_tobacco - Signaling objects
                which for specific resource type signal appearance on 'table'
            tobacco, paper, match - Signaling objects
                for specific resource type
            is_tobacco, is_paper, is_match - counters for
                specific resource type
            agent_sem - global Semaphore signaling to start with supply
    """
    def __init__(self):
        self.tobacco = Semaphore(0)
        self.paper = Semaphore(0)
        self.match = Semaphore(0)

        self.pusher_tobacco = Semaphore(0)
        self.pusher_paper = Semaphore(0)
        self.pusher_match = Semaphore(0)

        self.mutex = Mutex()
        self.is_tobacco = 0
        self.is_match = 0
        self.is_paper = 0

        self.agent_sem = Semaphore(1)


def make_cigarette(cig_id):
    """
        Simulation of assembling of product.
        Attributes:
            id - current smoker
    """
    print(f'"{cig_id}": makes cig')
    sleep(randint(1, 10) / 100)


def smoke(smoke_id):
    """
        Simulation of consumption of product.
        Attributes:
            id - current smoker
    """
    print(f'"{smoke_id}": smokes"')
    sleep(randint(1, 10) / 100)


def smoker_match(shared):
    """
        Smoker type method in this context waits for signal that it's required
        missing resource (match in this case, can be also paper or tobacco)
        appeared on the 'table' and then moves to the usage of
        resource and then signals consumption of resource. After that it
        starts it's process with the build up of product
        e.g. smoke the cigarette.
        Attributes:
            shared - object of type Shared which is modified between Threads
    """
    while True:
        sleep(randint(1, 10) / 100)
        shared.pusher_match.wait()
        # shared.paper.wait()
        # print('paper: smoker_match')
        # shared.tobacco.wait()
        # print('tobacco: smoker_match')
        make_cigarette("match")
        shared.agent_sem.signal()
        smoke("match")


def smoker_tobacco(shared):
    while True:
        sleep(randint(1, 10) / 100)
        shared.pusher_tobacco.wait()
        # shared.paper.wait()
        # print('paper: smoker_tobacco')
        # shared.match.wait()
        # print('match: smoker_tobacco')
        make_cigarette("tobacco")
        shared.agent_sem.signal()
        smoke("tobacco")


def smoker_paper(shared):
    while True:
        sleep(randint(1, 10) / 100)
        shared.pusher_paper.wait()
        # print('match: smoker_paper')
        # shared.tobacco.wait()
        # print('tobacco: smoker_paper')
        make_cigarette("paper")
        shared.agent_sem.signal()
        smoke("paper")


def agent_1(shared):
    """
        Agent type methods in this context starts with simulation
        of production of it's resource type (tobacco, paper, match)
        and then waits for the global
        signal of shortage which launches process in which smoker
        who currently has specific combination of resources
        can ask for agent-specific produced
        resource, In case of first agent it produces match so it sends
        signal to part of code which handles business with match.
        That means it provides match to smoker who currently has
        paper and tobacco ready.
        Attributes:
            shared - object of type Shared which is passed between Threads
    """
    while True:
        sleep(randint(1, 10) / 100)
        shared.agent_sem.wait()
        print('agent: tobacco, paper --> match')
        shared.tobacco.signal()
        shared.paper.signal()


def agent_2(shared):
    while True:
        sleep(randint(1, 10) / 100)
        shared.agent_sem.wait()
        print('agent: paper, match --> tobacco')
        shared.paper.signal()
        shared.match.signal()


def agent_3(shared):
    while True:
        sleep(randint(1, 10) / 100)
        shared.agent_sem.wait()
        print('agent: tobacco, match --> paper')
        shared.tobacco.signal()
        shared.match.signal()


def pusher_match(shared):
    """
        Pusher type methods in this context waits for it's type of
        resource to be produced then checks what content is
        available and lastly who should be able to take it.
        In case of no suitable smoker it just leaves the product
        on the 'table'. In our assignment we have 3 types of
        content to be produced and 3 different type of consumers
        with different requirements.
        Attributes:
            shared - object of type Shared which is passed between Threads
    """
    while True:
        shared.match.wait()
        shared.mutex.lock()
        if shared.is_tobacco > 0:
            shared.is_tobacco -= 1
            shared.pusher_paper.signal()
        elif shared.is_paper > 0:
            shared.is_paper -= 1
            shared.pusher_tobacco.signal()
        else:
            shared.is_match += 1
        shared.mutex.unlock()


def pusher_paper(shared):
    while True:
        shared.paper.wait()
        shared.mutex.lock()
        if shared.is_tobacco > 0:
            shared.is_tobacco -= 1
            shared.pusher_match.signal()
        elif shared.is_match > 0:
            shared.is_match -= 1
            shared.pusher_tobacco.signal()
        else:
            shared.is_paper += 1
        shared.mutex.unlock()


def pusher_tobacco(shared):
    while True:
        shared.tobacco.wait()
        shared.mutex.lock()
        if shared.is_match > 0:
            shared.is_match -= 1
            shared.pusher_paper.signal()
        elif shared.is_paper > 0:
            shared.is_paper -= 1
            shared.pusher_match.signal()
        else:
            shared.is_tobacco += 1
        shared.mutex.unlock()


def main():
    """
        Main part of our experimentation where we create smokers,
        agents and pushers and let them cooperate.
    """
    shared = Shared()

    smokers = []
    smokers.append(Thread(smoker_match, shared))
    smokers.append(Thread(smoker_tobacco, shared))
    smokers.append(Thread(smoker_paper, shared))

    pushers = []
    pushers.append(Thread(pusher_match, shared))
    pushers.append(Thread(pusher_paper, shared))
    pushers.append(Thread(pusher_tobacco, shared))

    agents = []
    agents.append(Thread(agent_1, shared))
    agents.append(Thread(agent_2, shared))
    agents.append(Thread(agent_3, shared))

    for t in smokers+agents:
        t.join()


if __name__ == '__main__':
    main()
