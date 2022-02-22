from fei.ppds import Mutex, Thread


class Shared:
    def __init__(self, end_count):
        self.counter = 0
        self.end = end_count
        self.elms = [0] * end_count


# Borrowed from Nico Schlömer's answer:
# https://stackoverflow.com/questions/2600191/how-can-i-count-the-occurrences-of-a-list-item
def occur_dict(a):
    d = {}
    for i in a:
        if i in d:
            d[i] = d[i] + 1
        else:
            d[i] = 1
    return d


def function_test(shared_object, mutex_lock):
    while shared_object.counter < shared_object.end:
        if len(shared_object.elms) - 1 > shared_object.counter:
            shared_object.elms[shared_object.counter] += 1
        shared_object.counter += 1


if __name__ == '__main__':
    shared = Shared(50000000)
    mutex = Mutex()

    mutex.lock()
    t1 = Thread(function_test, shared, mutex)
    mutex.unlock()
    t2 = Thread(function_test, shared, mutex)
    t1.join()
    t2.join()

    print(f'Occurances: {occur_dict(shared.elms)}')
