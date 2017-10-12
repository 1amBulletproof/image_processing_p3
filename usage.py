#!/usr/local/bin/python2

# @Author: Brandon Tarney
# @Date: 10/2017

# Usage class is for encapsulating the usage of a program and displaying it appropriately

import sys

class Usage:
    def __init__(self, input_str):
        self.usage = list()
        self.usage.append(input_str)

    def add(self, input_str):
        self.usage.append(input_str)

    def show(self):
        for line in self.usage:
            print(line)


def main():
    test_usage = Usage("Test")
    test_usage.show()
    test_usage.add("Also test like this")
    test_usage.show()
    test_usage = Usage("Usage: python2 %s " % (sys.argv[0]))
    test_usage.show()


if __name__ == "__main__":
    main()


