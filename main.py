from fei.ppds import Thread


class Shared:
    """
        Representation of object holding observed data and its parameters

        Arguments:
        counter -- array index
        end -- array length
        elms -- array the size of end value filled with 0's

    """

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


def function_test(shared_object):
    """
        Increment each element in the elms array .

        Arguments:
        shared -- Shared class object passed between threads

    """
    while shared_object.counter < shared_object.end:
        if len(shared_object.elms) > shared_object.counter:
            shared_object.elms[shared_object.counter] += 1
        shared_object.counter += 1


if __name__ == '__main__':
    shared = Shared(50000000)

    t1 = Thread(function_test, shared)
    t2 = Thread(function_test, shared)
    t1.join()
    t2.join()

    print(f'Occurances: {occur_dict(shared.elms)}')
