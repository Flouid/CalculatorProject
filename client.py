import calculator
import pyautogui

print('debugging mode? (y/n)')
verbose_string = input()
if (verbose_string == 'y') | (verbose_string == 'Y'):
    test = calculator.Calculator(angle_measure='degrees', verbose=True)
else:
    test = calculator.Calculator(angle_measure='radians')

old_statement = ''
result = ''
while True:
        statement = input()
        if statement == '':
            if old_statement == '':
                continue
        else:
            try:
                result = test.parse(statement)
                old_statement = statement
            except NameError:
                result = "Invalid Statement"
            except SyntaxError:
                result = "Invalid Syntax"
        print(result)


