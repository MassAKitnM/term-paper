#! usr/bin/python3

from collections import defaultdict
import math
import tkinter
from tkinter.ttk import Combobox


class ClientNotFoundException(Exception):
    '''Клиент не найден'''


class Bank:
    '''Работа банка'''

    def __init__(self) -> None:
        self.clients = defaultdict(int)

    def deposit(self, name: str, money: int):
        '''Изменение баланса'''
        self.clients[name] += money

    def balance(self, name: str):
        '''Проверка баланса'''
        if name in self.clients:
            return self.clients[name]
        raise ClientNotFoundException()

    def transfer(self, name1: str, name2: str, money: int):
        '''Перевод денег между клиентами'''
        self.deposit(name1, -money)
        self.deposit(name2, money)

    def income(self, per: int):
        '''Начисления процента денег всем клиентам'''
        for name in self.clients:
            if self.clients[name] > 0:
                self.clients[name] = math.floor(
                    self.clients[name] * (1 + per / 100))


class IntEntry(tkinter.Entry):
    def __init__(self, parent, *args, width=20, ** kwargs):
        kwargs['validate'] = 'key'
        kwargs['validatecommand'] = (
            parent.register(self.validate_int), '%P')
        super().__init__(parent, *args, width=width, **kwargs)

    def validate_int(self, value):
        if value == '':
            return True
        try:
            int(value)
            return True
        except ValueError:
            return False

    def get(self):
        raw_value = super().get()
        if raw_value == '':
            return 0
        return int(raw_value)


class Gui:
    '''Gui'''

    def __init__(self, bank: Bank) -> None:
        self.bank = bank
        self.prev_text = []
        self.window = tkinter.Tk()
        self.window.geometry('400x250')
        self.window.title('Bank')
        self.options = Combobox(self.window)
        self.choose = tkinter.Label(text='Select an option')
        self.choose.grid(column=0, row=0)
        self.btn_accept = tkinter.Button(self.window, text='accept',
                                         font='Comic', command=self.accept_page)
        self.btn_accept.grid(column=2, row=0)
        self.page_handlers = {
            'DEPOSIT': self.deposit,
            'WITHDRAW': self.withdraw,
            'INCOME': self.income,
            'BALANCE': self.balance,
            'TRANSFER': self.transfer,
        }
        self.options['values'] = list(self.page_handlers.keys())
        self.options.grid(column=1, row=0)
        self.window.mainloop()

    def accept_page(self):
        '''Действие при выборе операции'''
        choose_page = self.options.get()
        self.choose.configure(text=choose_page)
        for value in self.prev_text:
            value.destroy()
        self.page_handlers[choose_page]()

    def deposit(self):
        text_name = tkinter.Label(self.window, text='Name')
        text_name.grid(column=0, row=1)
        input_name = tkinter.Entry(self.window, width=20)
        input_name.grid(column=1, row=1)
        text_money = tkinter.Label(text='Money')
        text_money.grid(column=0, row=2)
        input_money = IntEntry(self.window)
        input_money.grid(column=1, row=2)
        output_text = tkinter.Label(self.window)
        output_text.grid(row=3, column=1)
        btn_run = tkinter.Button(self.window, text='RESULT', font='Comic', command=lambda: (
            self.bank.deposit(input_name.get(), input_money.get()), output_text.configure(text='DONE')))
        btn_run.grid(row=3, column=0)
        self.prev_text = [text_name, input_name,
                          text_money, input_money, output_text, btn_run]

    def income(self):
        text_p = tkinter.Label(text='Percent')
        text_p.grid(column=0, row=1)
        input_p = IntEntry(self.window, width=20)
        input_p.grid(column=1, row=1)
        output_text = tkinter.Label(self.window)
        output_text.grid(row=2, column=1)
        btn_run = tkinter.Button(
            self.window, text='RESULT', font='Comic', command=lambda: (self.bank.income(int(input_p.get())), output_text.configure(text='DONE')))
        btn_run.grid(row=2, column=0)
        self.prev_text = [text_p, input_p, output_text, btn_run]

    def withdraw(self):
        text_name = tkinter.Label(text='Name')
        text_name.grid(column=0, row=1)
        input_name = tkinter.Entry(self.window, width=20)
        input_name.grid(column=1, row=1)
        text_money = tkinter.Label(text='Money')
        text_money.grid(column=0, row=2)
        input_money = IntEntry(self.window)
        input_money.grid(column=1, row=2)
        output_text = tkinter.Label(self.window)
        output_text.grid(row=3, column=1)
        btn_run = tkinter.Button(
            self.window, text='RESULT', font='Comic', command=lambda: (self.bank.deposit(input_name.get(), -input_money.get()), output_text.configure(text='DONE')))
        btn_run.grid(row=3, column=0)
        self.prev_text = [text_name, input_name,
                          text_money, input_money, output_text, btn_run]

    def balance(self):
        text_name = tkinter.Label(text='Name')
        text_name.grid(column=0, row=1)
        input_name = tkinter.Entry(self.window, width=20)
        input_name.grid(column=1, row=1)
        output_text = tkinter.Label(self.window)
        output_text.grid(row=2, column=1)

        def output_balance():
            try:
                output_text.configure(text=self.bank.balance(input_name.get()))
            except ClientNotFoundException:
                output_text.configure(text='NO CLIENT')

        btn_run = tkinter.Button(
            self.window, text='RESULT', font='Comic', command=output_balance)
        btn_run.grid(row=2, column=0)
        self.prev_text = [text_name, input_name, output_text, btn_run]

    def transfer(self):
        text_name_from = tkinter.Label(text='Name 1')
        text_name_from.grid(column=0, row=1)
        input_name_from = tkinter.Entry(self.window, width=20)
        input_name_from.grid(column=1, row=1)
        text_name_to = tkinter.Label(text='Name 2')
        text_name_to.grid(column=0, row=2)
        input_name_to = tkinter.Entry(self.window, width=20)
        input_name_to.grid(column=1, row=2)
        text_money = tkinter.Label(text='Money')
        text_money.grid(column=0, row=3)
        input_money = IntEntry(self.window)
        input_money.grid(column=1, row=3)
        output_text = tkinter.Label(self.window)
        output_text.grid(row=4, column=1)
        btn_run = tkinter.Button(
            self.window, text='RESULT', font='Comic', command=lambda: (self.bank.transfer(input_name_from.get(),
                                                                                          input_name_to.get(), input_money.get()), output_text.configure(text='DONE')))
        btn_run.grid(row=4, column=0)
        self.prev_text = [text_name_from, text_name_to, input_name_from,
                          input_name_to, text_money, input_money, output_text, btn_run]


bank = Bank()
bank.deposit('Sidorchuk', 61899)
gui = Gui(bank)
