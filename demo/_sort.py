import logging

import conf

my_alphabet = ['a', 'b', 'c']


def test_1():
    def length(item):
        return len(item)

    data = ['a', 'aaa', 'aa']
    logging.info(data)
    data.sort(key=length)
    logging.info(data)


def test_2():
    data = [('a', 3), ('b', 2), ('c', 1)]
    logging.info(data)
    data = sorted(data, key=lambda x: x[1])
    logging.info(data)


def test_3():
    # False=0 < True=1
    data = [True, False]
    logging.info(data)
    data = sorted(data)
    logging.info(data)


def test_4():
    def cmp(item: str):
        if not item.isdigit():
            if item.isupper():
                return 3
            else:
                return 2
        else:
            return 1

    data = list('qwerQWER1234')
    logging.info(data)
    data.sort(key=cmp)
    logging.info(data)


test_1()
test_2()
test_3()
test_4()
