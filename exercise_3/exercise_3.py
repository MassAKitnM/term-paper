#! usr/bin/python3

import math
import operator
import tkinter
from tkinter.ttk import Combobox


class Calculator():
    '''Действия калькулятора'''

    def __init__(self) -> None:
        self.cells = {}
        self.ops_two_elements = {
            '+': operator.add,
            '-': operator.sub,
            '*': operator.mul,
            '/': operator.truediv,
            '%': operator.mod,
            '**': operator.pow,
        }

        def ten_xor(number):
            return operator.xor(10, number)

        def plus_minus(number):
            return - number
        # TODO

        def dms(number):
            pass

        self.ops_one_element = {
            'sqrt': math.sqrt,
            '10^': ten_xor,
            'tanh': math.tanh,
            'Ln': math.log,
            'Dms': None,  # TODO
            '+/-': plus_minus
        }

    def operations(self, operation: str, num):
        if operation in self.ops_two_elements:
            prev_num = self.cells['prev_num']
            result = self.ops_two_elements[operation](prev_num, num)
            self.cells['prev_num'] = result
            return result
        elif operation in self.ops_one_element:
            result = self.ops_one_element[operation](num)
            self.cells['prev_num'] = result
            return result

    def new_memory(self, cell: str, number):
        self.cells[cell] = number

    def memory_full_clear(self):
        self.cells.clear()

    def memory_clear_numbers(self, cells_name):
        del self.cells[cells_name]
