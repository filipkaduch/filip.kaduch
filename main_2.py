"""
    urllib.request - handler for opening URLs
    queue - multi-producer, multi-consumer queues
    time - used for tracking of elapsed time in task
    json - load response as dictionary
    os.path - check for todos.txt file existence
"""
import queue
import time
import json
import os.path
import urllib.request

"""
    This code snippet displays the implementation of basic
    version of response text title's getter service.
"""


def check(title):
    """
        This methods checks for the existence of title in
        todos.txt file.
        Attributes:
            title - string value to check in file
    """
    if os.path.exists("todos.txt"):
        with open("todos.txt") as f:
            datafile = f.readlines()
        for line in datafile:
            if title in line:
                return True
        return False
    return False


def task(que, index):
    """
        This methods first checks the multi-producer/consumer queue state and
        then proceeds to iterate over queue content. During this loop
        we are getting data from placeholder server and then try to write
        placeholder title to file if it's not already gathered by previous
        task run.
        Attributes:
            que - multi-producer/consumer Queue
            index - current task index
    """

    if que.empty():
        print(f'Task {index} out of work')

    while not que.empty():
        todo_id = que.get()
        url = "https://jsonplaceholder.typicode.com/todos/" + str(todo_id)
        print(f'Task {index} running {url}')
        start_t = time.perf_counter()

        data = urllib.request.urlopen(url).read().decode('utf-8')
        title = json.loads(data)["title"]
        if not check(title):
            f = open("todos.txt", "a")
            f.write(f'Title: {title}, Task: {index}\n')
            f.close()

        elapsed = time.perf_counter() - start_t
        print(f'Task {index} elapsed time {elapsed:2f}')
        yield


def main():
    """
        Main part of our experimentation with basic execution of tasks.
        We fill our async Queue with id's to fetch data from server and
        then proceed to asynchronously launch the tasks with
        list of id's to process all together.
    """

    wq = queue.Queue()

    for todo_id in range(1, 10):
        wq.put(todo_id)

    tasks = [
        task(wq, "One"),
        task(wq, "Two")
    ]
    start = time.perf_counter()
    done = False
    while not done:
        for t in tasks:
            try:
                next(t)
            except StopIteration:
                tasks.remove(t)
            if not tasks:
                done = True

    elapsed = time.perf_counter() - start
    print(f'Total elapsed time {elapsed:2f}')


if __name__ == '__main__':
    main()
