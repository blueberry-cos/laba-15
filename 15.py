from tkinter import *
from tkinter import messagebox
import urllib.request
import json
class Calculator:
    def __init__(self, root):
        self.root = root
        self.root['bg'] = '#f0f0f0'
        self.root.title('Калькулятор - 15.1')
        self.root.geometry('300x400')
        self.root.resizable(width=False, height=False)
        self.display = Entry(self.root, font=('Arial', 20), justify='right', bg='white', relief='ridge', bd=10)
        self.display.pack(fill=BOTH, padx=10, pady=10)
        self.display.insert(0, '0')
        self.first_number = None
        self.operation = None
        self.waiting_for_second = False
        frame = Frame(self.root, bg='#e0e0e0', bd=3)
        frame.pack(expand=True, fill=BOTH, padx=10, pady=10)
        buttons = [['7', '8', '9', '/'],['4', '5', '6', '*'],['1', '2', '3', '-'],['0', 'C', '=', '+']]
        for i, row in enumerate(buttons):
            for j, text in enumerate(row):
                btn = Button(frame, text=text, font=('Arial', 14), command=lambda t=text: self.click(t), bg='#f0f0f0', relief=RAISED, bd=3)
                btn.grid(row=i, column=j, sticky='nsew', padx=3, pady=3)
        for i in range(4):
            frame.grid_columnconfigure(i, weight=1)
            frame.grid_rowconfigure(i, weight=1)
        for child in frame.winfo_children():
            if child.cget('text') == 'C':
                child.config(bg='#ff6b6b', fg='white')
            elif child.cget('text') == '=':
                child.config(bg='#4CAF50', fg='white')
    def click(self, key):
        if key.isdigit():
            if self.waiting_for_second:
                self.display.delete(0, END)
                self.waiting_for_second = False
            current = self.display.get()
            if current == '0':
                self.display.delete(0, END)
            self.display.insert(END, key)
        elif key in ['+', '-', '*', '/']:
            self.first_number = float(self.display.get())
            self.operation = key
            self.waiting_for_second = True
        elif key == '=':
            if self.first_number is not None and self.operation:
                second_number = float(self.display.get())
                if self.operation == '+':
                    result = self.first_number + second_number
                elif self.operation == '-':
                    result = self.first_number - second_number
                elif self.operation == '*':
                    result = self.first_number * second_number
                elif self.operation == '/':
                    if second_number == 0:
                        messagebox.showerror(title='Ошибка', message='На ноль делить нельзя!')
                        self.clear()
                        return
                    result = self.first_number / second_number
                self.display.delete(0, END)
                if result == int(result):
                    self.display.insert(0, str(int(result)))
                else:
                    self.display.insert(0, str(round(result, 10)))
                self.first_number = None
                self.operation = None
                self.waiting_for_second = False
        elif key == 'C':
            self.clear()
    def clear(self):
        self.display.delete(0, END)
        self.display.insert(0, '0')
        self.first_number = None
        self.operation = None
        self.waiting_for_second = False
class NumberFactsApp:
    def __init__(self, root):
        self.root = root
        self.root['bg'] = '#f0f0f0'
        self.root.title('Факты о числах и курсы валют - 15.2')
        self.root.geometry('550x600')
        self.root.resizable(width=False, height=False)
        self.number_facts = {1: 'Единица - самое маленькое натуральное число.',2: 'Двойка - единственное чётное простое число.',3: 'Тройка - первое нечётное простое число.',
            4: 'Четвёрка - самое маленькое составное число.',5: 'Пятёрка - число пальцев на руке человека.',7: 'Семёрка - самое популярное "магическое" число.',
            8: 'Восьмёрка - символ бесконечности, если повернуть.',9: 'Девятка - при умножении на любое число даёт сумму цифр 9.',10: 'Десятка - основание десятичной системы счисления.',
            12: 'Дюжина - традиционная мера счёта.',13: 'Тринадцать - "чёртова дюжина", считается несчастливым.',42: '42 - ответ на главный вопрос жизни, вселенной и всего такого.'}
        title = Label(self.root, text='ИНТЕРЕСНЫЕ ФАКТЫ О ЧИСЛАХ', font=('Arial', 14, 'bold'), bg='#f0f0f0', fg='#2c3e50')
        title.pack(pady=10)
        subtitle = Label(self.root, text='Источник: собранная база фактов + API курсов валют', font=('Arial', 9), bg='#f0f0f0', fg='gray')
        subtitle.pack()
        frame1 = LabelFrame(self.root, text='ФАКТ О ЧИСЛЕ', font=('Arial', 10, 'bold'), bg='white', fg='#2196F3', padx=10, pady=10)
        frame1.pack(padx=20, pady=10, fill=X)
        Label(frame1, text='Введите число:', font=('Arial', 11), bg='white').pack(anchor=W)
        self.number_entry = Entry(frame1, font=('Arial', 12), width=15, bg='white')
        self.number_entry.pack(anchor=W, pady=5)
        self.number_entry.insert(0, '42')
        self.fact_btn = Button(frame1, text='УЗНАТЬ ФАКТ О ЧИСЛЕ', command=self.get_number_fact, bg='#4CAF50', fg='white', font=('Arial', 10, 'bold'))
        self.fact_btn.pack(pady=5)
        self.number_fact_label = Label(frame1, text='', font=('Arial', 10), bg='white', fg='#333', wraplength=450, justify=LEFT)
        self.number_fact_label.pack(pady=5, fill=X)
        frame2 = LabelFrame(self.root, text='КУРСЫ ВАЛЮТ (API)', font=('Arial', 10, 'bold'), bg='white', fg='#FF9800', padx=10, pady=10)
        frame2.pack(padx=20, pady=10, fill=X)
        Label(frame2, text='Актуальные курсы валют к доллару США', font=('Arial', 9), bg='white', fg='gray').pack()
        self.update_btn = Button(frame2, text='ОБНОВИТЬ КУРСЫ ВАЛЮТ', command=self.get_exchange_rates, bg='#FF9800', fg='white', font=('Arial', 10, 'bold'))
        self.update_btn.pack(pady=5)
        self.rates_text = Text(frame2, height=6, width=50, font=('Arial', 10), wrap=WORD, bg='#fafafa')
        self.rates_text.pack(pady=5, fill=X)
        self.status = Label(self.root, text='Готов', fg='gray', bg='#f0f0f0')
        self.status.pack(pady=5)
        popular_frame = Frame(self.root, bg='#f0f0f0')
        popular_frame.pack(pady=5)
        Label(popular_frame, text='Популярные числа: ', font=('Arial', 9), bg='#f0f0f0').pack(side=LEFT)
        for num in [7, 13, 42, 100, 365, 666]:
            btn = Button(popular_frame, text=str(num), command=lambda n=num: self.set_number(n), font=('Arial', 9), bg='#e0e0e0', relief=FLAT)
            btn.pack(side=LEFT, padx=3)
    def set_number(self, num):
        self.number_entry.delete(0, END)
        self.number_entry.insert(0, str(num))
        self.get_number_fact()
    def get_number_fact(self):
        try:
            num = int(self.number_entry.get())
            if num in self.number_facts:
                fact = self.number_facts[num]
            else:
                if num % 2 == 0:
                    parity = 'чётное'
                else:
                    parity = 'нечётное'
                is_prime = True
                if num < 2:
                    is_prime = False
                else:
                    for i in range(2, int(num ** 0.5) + 1):
                        if num % i == 0:
                            is_prime = False
                            break
                if is_prime and num > 1:
                    prime_text = 'Простое число.'
                else:
                    prime_text = 'Составное число.'
                fact = f'{num} - {parity} число. {prime_text}'
            self.number_fact_label.config(text=f'{fact}')
            self.status.config(text=f'Факт о числе {num} получен', fg='green')
        except ValueError:
            messagebox.showerror(title='Ошибка', message='Введите целое число!')
    def get_exchange_rates(self):
        self.update_btn.config(state=DISABLED, text='Загрузка...')
        self.status.config(text='Загрузка курсов валют...', fg='orange')
        self.root.update()
        try:
            url = 'https://www.floatrates.com/daily/usd.json'
            req = urllib.request.Request(
                url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=10) as response:
                data = json.loads(response.read().decode())
            self.rates_text.delete(1.0, END)
            currencies = {
                'eur': 'Евро (EUR)',
                'rub': 'Российский рубль (RUB)',
                'gbp': 'Фунт стерлингов (GBP)',
                'cny': 'Китайский юань (CNY)'}
            result = '1 USD = \n'
            for code, name in currencies.items():
                if code in data:
                    rate = data[code]['rate']
                    result += f'  • {rate:.4f} {name}\n'
            result += '\nДанные: floatrates.com'
            self.rates_text.insert(1.0, result)
            self.status.config(text='Курсы валют обновлены', fg='green')
        except Exception as e:
            self.rates_text.delete(1.0, END)
            self.rates_text.insert(1.0, 'Ошибка загрузки курсов.\nПроверьте интернет-соединение.')
            self.status.config(text='Ошибка загрузки курсов', fg='red')
        finally:
            self.update_btn.config(state=NORMAL, text='ОБНОВИТЬ КУРСЫ ВАЛЮТ')
class MainMenu:
    def __init__(self):
        self.root = Tk()
        self.root['bg'] = '#2c3e50'
        self.root.title('Практическая работа 15')
        self.root.geometry('400x350')
        self.root.resizable(width=False, height=False)
        title = Label(self.root, text='Практическая работа 15', font=('Arial', 18, 'bold'), bg='#2c3e50', fg='white')
        title.pack(pady=30)
        subtitle = Label(self.root, text='Создание приложений с GUI. TKinter', font=('Arial', 10), bg='#2c3e50', fg='#bdc3c7')
        subtitle.pack()
        btn_frame = Frame(self.root, bg='#2c3e50')
        btn_frame.pack(pady=40)
        btn1 = Button(btn_frame, text='15.1 - Калькулятор', command=self.open_calculator, width=28, height=2, bg='#4CAF50', fg='white', font=('Arial', 11, 'bold'), relief=RAISED, bd=3)
        btn1.pack(pady=8)
        btn2 = Button(btn_frame, text='15.2 - Факты о числах + Курсы валют', command=self.open_facts, width=28, height=2, bg='#2196F3', fg='white', font=('Arial', 11, 'bold'), relief=RAISED, bd=3)
        btn2.pack(pady=8)
        exit_btn = Button(btn_frame, text='Выход', command=self.root.quit, width=28, height=1, bg='#e74c3c', fg='white', font=('Arial', 10), relief=RAISED, bd=3)
        exit_btn.pack(pady=20)
        self.root.mainloop()
    def open_calculator(self):
        new_window = Toplevel(self.root)
        Calculator(new_window)
    def open_facts(self):
        new_window = Toplevel(self.root)
        NumberFactsApp(new_window)
if __name__ == '__main__':
    app = MainMenu()