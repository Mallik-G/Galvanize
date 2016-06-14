'''
Miniquiz

Include your code and answers in python_coin.py.

Given an infinite number of US coins (coins = [1, 5, 10, 25]) and an
amount value in cents, what are minimum number of coins needed to make
change for value? Write a function find_change that takes as input the
coin denominations coins, and value as the amount in cents. Your function
should return the minimum amount of coins necessary to make change for the
specified value as an integer.

Example

coins = [1, 5, 10, 25]

In [23]: find_change(coins, 100)
4

In [24]: find_change(coins, 74)
8
'''



def find_change(coins, value):
    coin_count = 0
    coins.sort(reverse=True)
    for coin in coins:
        while value-coin>-1:
            value-=coin
            coin_count+=1
    return coin_count
