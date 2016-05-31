"""
Miniquiz: Appreciating Numpy

Include your code and answers in numpy_quiz.py.

Write a python function to find the value in a list that's closest to a given value.

e.g. closest([10, 17, 2, 29, 16], 14) should return 16.

Instead let's start with a numpy array. How can we do the same thing in one line using numpy magic?

Hint: Use np.abs and np.argmin.

My favorite numpy trick is masking. Say you have a feature matrix X
(2d numpy array) and with labels y (1d numpy array). I would like to get a
feature matrix of only the positive cases, i.e. get the rows from X where y
is positive.

How can you do this in one line?

Create example X and y to verify your code.
"""

import numpy as np

def closest(lst, num):
     return lst[np.argmin(list(abs(np.array(lst) - num)))]


def closest_long(lst, num):
    min_value = 10000
    low_item = 100000
    for item in lst:
        if abs(item - num) < min_value:
            min_value = abs(item-num)
            low_item = item

    return item


#  x.T[:,y>0]
