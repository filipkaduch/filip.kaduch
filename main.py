"""
    This code snippet displays the implementation of Scheduler in order
    to manage 'tasks' execution and it's data flow.
"""


def find_dmg(data, index):
    """
        This methods finds the highest value in line of data.
        Attributes:
            data - list of int values from 1 - 9
            index - current line index
    """
    highest = 0
    for j in range(len(data)):
        if data[j] > highest:
            highest = data[j]
    print(f'HIGHEST number in line: {index}:', highest)
    yield


def find_low(data, index):
    """
        This methods finds the lowest value in line of data.
        Attributes:
            data - list of int values from 1 - 9
            index - current line index
    """
    highest_current = 10
    for j in range(len(data)):
        if data[j] < highest_current:
            highest_current = data[j]
    print(f'LOWEST number in line: {index}:', highest_current)
    yield


class Dispatcher:
    """
        This class represents manager for co - programs working and
        running with same data and in the same time. It provides
        one mode to run tasks in loop.

        Attributes:
            tasks - list of tasks to process
            loop - managing method for launching the tasks in rotating loop
            new - adds task to list
            schedule - launches task generator
            remove - close the generator and remove it from list
    """
    def __init__(self):
        self.tasks = []

    def new(self, task):
        self.tasks.append(task)

    def schedule(self, index):
        next(self.tasks[index])

    def loop(self):
        cur_index = 0
        while self.tasks:
            try:
                if cur_index < len(self.tasks):
                    self.schedule(cur_index)
                else:
                    yield
                cur_index += 1
            except StopIteration:
                self.remove(cur_index)

    def remove(self, index):
        self.tasks[index].close()
        del self.tasks[index]


def main():
    """
        Main part of our experimentation with expanded generators used
        with planned execution through dispatcher. We load our entry file
        and for each line data we alternatively call find_low and find_dmg
        methods printing relevant information on current line.
    """

    dispatcher = Dispatcher()
    line_indexer = 0
    with open('entry.txt', 'r') as f:
        for line in f:
            line_data = []
            for num in line.split(' '):
                line_data.append(int(num))
            fl = find_low(line_data, line_indexer)
            fd = find_dmg(line_data, line_indexer)
            line_indexer += 1
            dispatcher.new(fd)
            dispatcher.new(fl)

        next(dispatcher.loop())


if __name__ == '__main__':
    main()
