import math
import operator
from tkinter import E
from PyQt6 import QtCore, QtGui, QtWidgets, uic


class WrongCalculatorValue(Exception):
    '''Неправильная операция'''


class Calculator():
    '''Действия калькулятора'''

    def __init__(self) -> None:
        self.cells = {
            'm_1': 0,
            'm_2': 0,
            'm_3': 0,
            'm_4': 0,
            'm_5': 0,
            'm_6': 0,
            'm_7': 0,
            'm_8': 0,
        }
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


class Ui(QtWidgets.QMainWindow):
    def __init__(self, calculator: Calculator) -> None:
        super().__init__()
        uic.loadUi('Gui.ui', self)
        self.current_text = ''
        self.dot_status = False
        self.fist_num = ''
        self.current_operator = ''
        self.result.setText(self.current_text)

        # buttoms num
        self.b_0.pressed.connect(lambda: self.num_clicked(self.b_0.text()))
        self.b_1.pressed.connect(lambda: self.num_clicked(self.b_1.text()))
        self.b_2.pressed.connect(lambda: self.num_clicked(self.b_2.text()))
        self.b_3.pressed.connect(lambda: self.num_clicked(self.b_3.text()))
        self.b_4.pressed.connect(lambda: self.num_clicked(self.b_4.text()))
        self.b_5.pressed.connect(lambda: self.num_clicked(self.b_5.text()))
        self.b_6.pressed.connect(lambda: self.num_clicked(self.b_6.text()))
        self.b_7.pressed.connect(lambda: self.num_clicked(self.b_7.text()))
        self.b_8.pressed.connect(lambda: self.num_clicked(self.b_8.text()))
        self.b_9.pressed.connect(lambda: self.num_clicked(self.b_9.text()))
        self.b_dot.pressed.connect(lambda: self.dot())

        # buttoms memory
        self.b_c.pressed.connect(self.clear)
        self.b_delete.pressed.connect(self.ui_delete)
        self.b_m_c_1.pressed.connect(lambda: self.memory('mc', 'm_1'))
        self.b_m_r_1.pressed.connect(lambda: self.memory('mr', 'm_1'))
        self.b_m_s_1.pressed.connect(lambda: self.memory('ms', 'm_1'))
        self.b_m_plus_1.pressed.connect(lambda: self.memory('m+', 'm_1'))
        self.b_m_minus_1.pressed.connect(lambda: self.memory('m-', 'm_1'))

        # buttoms operations
        self.b_slash.pressed.connect(lambda: self.set_operation('/'))
        self.b_starcitizen.pressed.connect(lambda: self.set_operation('*'))
        self.b_minus.pressed.connect(lambda: self.set_operation('-'))
        self.b_plus.pressed.connect(lambda: self.set_operation('+'))
        self.b_deg.pressed.connect(lambda: self.set_operation('**'))
        self.b_sqrt.pressed.connect(lambda: self.solo_operations('sqrt'))
        self.b_plus_minus.pressed.connect(lambda: self.solo_operations('+/-'))
        self.b_equal.pressed.connect(self.operations)

    def ui_value(self, text: str):
        if text == '':
            return 0
        elif text.find(".") > 0:
            if text[-1] != '.':
                return float(text)
            else:
                return int(text[:-1])
        else:
            return int(text)

    def num_clicked(self, num: str):
        self.current_text += num
        self.result.setText(self.current_text)

    def dot(self):
        if self.current_text.find('.') == -1:
            self.num_clicked('.')

    def clear(self):
        self.current_text = ''
        self.result.setText(self.current_text)

    def ui_delete(self):
        if len(self.current_text) > 1:
            self.current_text = self.current_text[:-1]
        else:
            self.current_text = ''
        self.result.setText(self.current_text)

    def memory(self, mod: str, slot: str):
        if mod == 'mc':
            calculator.cells[slot] = 0
        elif mod == 'm+':
            calculator.cells[slot] += self.ui_value(self.result.text())
        elif mod == 'm-':
            calculator.cells[slot] -= self.ui_value(self.result.text())
        elif mod == 'ms':
            calculator.cells[slot] = self.ui_value(self.result.text())
        self.result.setText(str(calculator.cells[slot]))
        if mod == 'mr':
            self.current_text = str(calculator.cells[slot])
        else:
            self.current_text = ''

    def set_operation(self, op: str):
        self.fist_num = self.current_text
        self.current_text = ''
        self.current_operator = op

    def operations(self):
        try:
            if self.current_operator == '':
                return
            self.current_text = str(calculator.ops_two_elements[self.current_operator](
                self.ui_value(self.fist_num), self.ui_value(self.current_text)))
            self.fist_num = self.current_text
            self.result.setText(self.fist_num)
            self.current_operator = ''
        except (WrongCalculatorValue, ZeroDivisionError):
            print('Test commit')
            return

    def solo_operations(self, op: str):
        self.current_operator = op
        self.current_text = str(calculator.ops_one_element[self.current_operator](
            self.ui_value(self.current_text)))
        self.result.setText(self.current_text)
        self.current_operator = ''


if __name__ == '__main__':
    calculator = Calculator()
    app = QtWidgets.QApplication([])
    window = Ui(calculator)
    window.show()
    app.exec()
