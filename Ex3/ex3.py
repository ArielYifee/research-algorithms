from functools import reduce
import re
import doctest


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


"""
question 1
helped by:
https://www.geeksforgeeks.org/check-if-email-address-valid-or-not-in-python/
https://www.w3schools.com/python/python_regex.asp
"""


def check_email(path):
    try:
        if not isinstance(path, str) or not path:
            raise TypeError("There's an issue with file path.")
        with open(path, 'r') as file:
            regex = r'^[a-z0-9]+[\._-]?[a-z0-9]+[@][a-z0-9]+[\._-]?[a-z0-9]+[.]\w{2,}$'
            valid = []
            invalid = []
            lines = file.read().splitlines()
            for line in lines:
                if line:
                    valid.append(line) if (re.fullmatch(
                        regex, line)) else invalid.append(line)
            print(
                f"{bcolors.HEADER}The valid emails are:\n{bcolors.OKBLUE}{valid}{bcolors.ENDC}\n")
            print(
                f"{bcolors.HEADER}The invalid emails are:\n{bcolors.WARNING}{invalid}{bcolors.ENDC}")
    except Exception as error:
        print('Caught this error: ' + repr(error))


"""
question 2
helped by the summery.
"""


def lastcall(func):
    """
    >>> f(2)
    4
    >>> f(2)
    I already told you that the answer is 4
    >>> f(x=2)
    I already told you that the answer is 4
    >>> f(x=10)
    100
    >>> f(x=10)
    I already told you that the answer is 100
    >>> f(10)
    I already told you that the answer is 100
    >>> fun(x="hello")
    hello Ariel!
    >>> fun(x="hello")
    I already told you that the answer is hello Ariel!
    """
    calls = {}

    def wrapper(*args, **kwargs):
        if len(args) + len(kwargs) != 1:
            raise TypeError(
                "lastcall wrapper support only one parameter functions.")
        param = None
        if len(args) == 1:
            param = args[0]
        else:
            param = next(iter(kwargs.values()))
        if param in calls:
            print(f'I already told you that the answer is {calls[param]}')
        else:
            res = func(param)
            calls[param] = res
            print(res)
    return wrapper


"""
question 3

https://stackoverflow.com/questions/34884567/python-multiple-inheritance-passing-arguments-to-constructors-using-super
https://holycoders.com/python-dunder-special-methods/
https://www.scaler.com/topics/reduce-function-in-python/
"""


class List(list):
    def __init__(self, *args, **kwargs):
        '''
        >>> print(mylist)
        [[[1, 2, 3, 33], [4, 5, 6, 66]], [[7, 8, 9, 99], [10, 11, 12, 122]], [[13, 14, 15, 155], [16, 17, 18, 188]]]
        >>> print(mylist[0,1,3])
        66
        >>> print(mylist[0])
        [[1, 2, 3, 33], [4, 5, 6, 66]]
        >>> print(mylist + mylist2)
        [[[1, 2, 3, 33], [4, 5, 6, 66]], [[7, 8, 9, 99], [10, 11, 12, 122]], [[13, 14, 15, 155], [16, 17, 18, 188]], [[1, 2, 3, 33], [4, 5, 6, 66]], [[7, 8, 9, 99], [10, 11, 12, 122]], [[13, 14, 15, 155], [16, 17, 18, 188]]]
        >>> print(mylist == mylist2)
        True
        '''
        super().__init__(*args, **kwargs)

    def __delitem__(self, pos):
        if isinstance(pos, tuple):
            reduce(lambda x, y: x[y], pos[:-1], self).__delitem__(pos[-1])
        else:
            super().__delitem__(pos)

    def __getitem__(self, pos):
        if isinstance(pos, tuple):
            return reduce(lambda x, y: x[y], pos, self)
        else:
            return super().__getitem__(pos)

    def __setitem__(self, pos, val):
        if isinstance(pos, tuple):
            reduce(lambda x, y: x[y], pos[:-1], self)[pos[-1]] = val
        else:
            super().__setitem__(pos, val)

"""
question 4
https://www.codingame.com/training/medium/stock-exchange-losses
"""


@lastcall
def f(x: int):
    return pow(x, 2)


@lastcall
def fun(x: str):
    return x + " Ariel!"


mylist = List([
    [[1, 2, 3, 33], [4, 5, 6, 66]],
    [[7, 8, 9, 99], [10, 11, 12, 122]],
    [[13, 14, 15, 155], [16, 17, 18, 188]],
]
)

mylist2 = List([
    [[1, 2, 3, 33], [4, 5, 6, 66]],
    [[7, 8, 9, 99], [10, 11, 12, 122]],
    [[13, 14, 15, 155], [16, 17, 18, 188]],
]
)

choies = int(input(f'{bcolors.HEADER}Pick an option:\n1 - run question 1\n2 - run question\'s 2,3 tests: {bcolors.ENDC}'))
if choies == 1:
    path = str(input(f'{bcolors.OKGREEN}Enter the path: {bcolors.ENDC}'))
    check_email(path)
elif choies == 2:
    doctest.testmod(verbose=True)
else:
    print(f'{bcolors.FAIL}You did\'t pick right!{bcolors.ENDC}')
